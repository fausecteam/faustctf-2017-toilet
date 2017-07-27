#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <openssl/sha.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/types.h>
#include <dirent.h>
#include "profile.h"
#include "util.h"

Log *logList = NULL;

/* Profile managment functions */
Profile *createProfile(char *name) {
    struct timeval time_buf;
    /*
     * Valgrind is crying about uninitialised bytes
     * but I don't want to give a hint by using
     * calloc here and maybe people get on the
     * false track this way:->
     */
    global_user = malloc (sizeof(Profile));
    if (!global_user) {
        die ("malloc", MALLOC_ERROR);
    }
    gettimeofday(&time_buf, NULL);
    srand ((time_buf.tv_sec * 1000) + (time_buf.tv_usec / 1000));
    global_user->id = rand ();
    global_user->ffunc = quickFlush;
    /* VULN: Off-by one vuln here */
    sprintf (global_user->name, "%s", name);
    time (&(global_user->lastVisit));
    global_user->seatTemp = 20;
    global_user->weight = 0;
    global_user->notes = NULL;
    return global_user;
}

int storeProfile(Profile *user) {
    char filename[SHA256_DIGEST_LENGTH*2+1];
    char path[strlen(BASEDIR)+SHA256_DIGEST_LENGTH*2+2];
    int out, ret;

    if (!user) {
        return -1;
    }
    /* Check that the notes buffer has been freed */
    if (user->notes != NULL) {
        return -1;
    }
    calcSHA256(user->name, filename);
    sprintf (path, "%s/%s", BASEDIR, filename);
    out = open (path, O_WRONLY|O_CREAT, S_IRUSR | S_IWUSR);

    if (out == -1) {
        fprintf (stderr, "%s can't be opened.\n", path);
        die ("open", OPEN_ERROR);
        return -1;
    }
    ret = write (out, user, sizeof(Profile));
    if (ret != sizeof (Profile)) {
        die ("write", WRITE_ERROR);
    }
    ret = close (out);
    if (ret != 0) {
        die ("close", CLOSE_ERROR);
    }
    return 0;
}

Profile *loadProfile(char *filename) {
    char path[strlen(BASEDIR)+SHA256_DIGEST_LENGTH*2+2];
    int in, ret;

    global_user = malloc (sizeof (Profile));
    if (global_user == NULL) {
        die ("malloc", MALLOC_ERROR);
    }
    sprintf (path, "%s/%s", BASEDIR, filename);
    in = open (path, O_RDONLY);
    if (in == -1) {
        fprintf (stderr, "%s can't be opened.\n", path);
        die ("open", OPEN_ERROR);
        return NULL;
    }
    ret = read (in, global_user, sizeof (Profile));
    if (ret != sizeof (Profile)) {
        die ("read", READ_ERROR);
    }
    ret = close (in);
    if (ret != 0) {
        die ("close", CLOSE_ERROR);
    }
    time (&(global_user->lastVisit));
    global_user->notes = NULL;
    return global_user;
}

int checkProfile(char *filename) {
    char path[strlen(BASEDIR)+SHA256_DIGEST_LENGTH*2+2];
    struct stat statbuf;

    snprintf (path, sizeof (path), "%s/%s", BASEDIR, filename);
    if (stat (path, &statbuf) != 0) {
        return 0;
    } else {
        return 1;
    }
}

uint16_t getMaxWeight(Profile *user) {
    if (!user) {
        return -1;
    }
    return user->weight;
}

int setMaxWeight(Profile *user, uint16_t weight) {
    if (!user) {
        return -1;
    }
    user->weight = weight;
    return 0;
}

int16_t getSeatTemp(Profile *user) {
    if (!user) {
        return 0;
    }
    return user->seatTemp;
}

int setSeatTemp(Profile *user, int16_t temp) {
    if (!user) {
        return -1;
    }
    user->seatTemp = temp;
    return 0;
}

int setFlushFunc(Profile *user, uint8_t choice) {
    if (!user) {
        return -1;
    }
    switch (choice) {
        case 0:
            user->ffunc = quickFlush;
            break;
        case 1:
            user->ffunc = longFlush;
            break;
        default:
            return -1;
    }
    return 0;
}


char *createNoteBuffer(Profile *user, uint16_t weight, uint16_t consistency) {
    uint16_t currentMax;
    uint16_t bufSize;
    char *noteBuf;
    if (!user) {
        return NULL;
    }
    currentMax = getMaxWeight (user);
    if (currentMax < weight) {
        if ((setMaxWeight (user, weight)) == -1) {
            return NULL;
        }
    }

    /*
     * VULN:
     * Multiplication Bug
     */
    //printf("consistency: %hu, weight: %hu, totalSize: %hu\n", consistency, weight, consistency*10+weight*10));
    bufSize = weight*100 + consistency*10;
    noteBuf = malloc (bufSize);
    if (noteBuf == NULL) {
        die ("malloc", MALLOC_ERROR);
    }
    user->notes = noteBuf;
    return noteBuf;
}

int flushLoad(Profile *user) {
    if (!user || !(user->notes)) {
        return -1;
    }
    user->ffunc (user->notes);
    user->notes = NULL;
    return 0;
}

Log *genLogElem(Profile *user) {
    Log *logEntry;

    if (!user) {
        return NULL;
    }
    logEntry = malloc (sizeof (Log));
    if (logEntry == NULL) {
        die ("malloc", MALLOC_ERROR);
    }
    calcSHA256(user->name, logEntry->name);
    logEntry->id = user->id;
    logEntry->lastVisit = user->lastVisit;
    logEntry->next = NULL;
    return logEntry;
}

int loadLog(void) {
    char path[strlen(BASEDIR)+SHA256_DIGEST_LENGTH*2+2];
    DIR* dirPtr;
    struct dirent* currFile;
    int in;
    Profile *profileEntry;
    Log *logEntry;

    if ((dirPtr = opendir (BASEDIR)) == NULL) {
        die("opendir", OPENDIR_ERROR);
    }
    while ((currFile = readdir (dirPtr))) {
        if (!strcmp (currFile->d_name, ".")) {
            continue;
        }
        if (!strcmp (currFile->d_name, "..")) {
            continue;
        }
        sprintf (path, "%s/%s", BASEDIR, currFile->d_name);
        in = open (path, O_RDONLY);
        if (in == -1) {
            fprintf (stderr, "%s can't be opened.\n", path);
            die ("open", OPEN_ERROR);
            return -1;
        }
        profileEntry = malloc (sizeof (Profile));
        if (!profileEntry) {
            die ("malloc", MALLOC_ERROR);
        }
        if (read (in, profileEntry, sizeof (Profile)) != sizeof (Profile)) {
            die ("read", READ_ERROR);
        }
        if (close (in) == -1) {
            die ("close", CLOSE_ERROR);
        }
        logEntry = genLogElem (profileEntry);
        free (profileEntry);
        if (!logEntry) {
            return -1;
        }
        logEntry->next = logList;
        logList = logEntry;
    }
    closedir(dirPtr);
    return 0;
}

static int cmp(Log *a, Log *b) {
    return b->lastVisit - a->lastVisit;
}

Log *sortLog(Log *list) {
    Log *first, *second, *current, *tail;
    int insize, nmerges, firstSize, secondSize, i;

    if (!list) {
        return NULL;
    }

    insize = 1;

    while (1) {
        first = list;
        list = NULL;
        tail = NULL;

        nmerges = 0;  /* count number of merges we do in this firstass */

        while (first) {
            nmerges++;  /* there exists a merge to be done */
            /* step `insize' firstlaces along from first */
            second = first;
            firstSize = 0;
            for (i = 0; i < insize; i++) {
                firstSize++;
                second = second->next;
                if (!second) {
                    break;
                }
            }

            /* if second hasn't fallen off end, we have two lists to merge */
            secondSize = insize;

            /* now we have two lists; merge them */
            while (firstSize > 0 || (secondSize > 0 && second)) {

                /* decide whether next element of merge comes from first or second */
                if (firstSize == 0) {
                    /* first is empty; current must come from second. */
                    current = second;
                    second = second->next;
                    secondSize--;
                } else if (secondSize == 0 || !second) {
                    /* second is empty; current must come from first. */
                    current = first;
                    first = first->next;
                    firstSize--;
                } else if (cmp(first,second) <= 0) {
                    /* First element of first is lower (or same);
                     * current must come from first.
                     */
                    current = first;
                    first = first->next;
                    firstSize--;
                } else {
                    /* First element of second is lower; current must come from second. */
                    current = second;
                    second = second->next;
                    secondSize--;
                }

                /* add the next element to the merged list */
                if (tail) {
                    tail->next = current;
                } else {
                    list = current;
                }
                tail = current;
            }

            /* now first has stepped `insize' places along, and second has too */
            first = second;
        }
        tail->next = NULL;

        /* If we have done only one merge, we're finished. */
        if (nmerges <= 1) {
            return list;
        }

        /* Otherwise repeat, merging lists twice the size */
        insize *= 2;
    }
}

Log *removeUserFromLog(Log *log, uint64_t id) {
    Log *element = logList;
    Log *drag = element;

    while (element != NULL) {
        if (element->id == id) {
            if (element == logList) {
                logList = element->next;
            } else {
                drag->next = element->next;
            }
            free(element);
            break;
        }
        drag = element;
        element = element->next;
    }
    return logList;
}

void freeLog(Log *log) {
    Log *element = logList;
    Log *drag = element;

    while (element != NULL) {
        drag = element;
        element = element->next;
        free(drag);
    }
}
