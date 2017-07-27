#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <errno.h>
#include "profile.h"
#include "util.h"

#define CONS_MAX_LEN 31

#define RED     "\x1b[31m"
#define GREEN   "\x1b[32m"
#define YELLOW  "\x1b[33m"
#define BLUE    "\x1b[34m"
#define MAGENTA "\x1b[35m"
#define CYAN    "\x1b[36m"
#define RESET   "\x1b[0m"

static const char *colors[] = {RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN};

static const char *banner = "\n\n\n\
$$$$$$$$\\  $$$$$$\\  $$$$$$\\ $$\\       $$$$$$$$\\ $$$$$$$$\\ \n\
\\__$$  __|$$  __$$\\ \\_$$  _|$$ |      $$  _____|\\__$$  __| \n\
   $$ |   $$ /  $$ |  $$ |  $$ |      $$ |         $$ |    \n\
   $$ |   $$ |  $$ |  $$ |  $$ |      $$$$$\\       $$ |    \n\
   $$ |   $$ |  $$ |  $$ |  $$ |      $$  __|      $$ |    \n\
   $$ |   $$ |  $$ |  $$ |  $$ |      $$ |         $$ |    \n\
   $$ |    $$$$$$  |$$$$$$\\ $$$$$$$$\\ $$$$$$$$\\    $$ |    \n\
   \\__|    \\______/ \\______|\\________|\\________|   \\__|    \n\
                                                           \n\
                                                           \n\
                                                           \n\
";

/* Welcome message */
static const char *welcome = "Welcome to the our new smart toilet!\n\
It's the best experience you'll get since your change from diaper to potty!\n\
Try our note feature to keep track of your bowel movement!\n\
Even better, in our next update we'll add a twitter sharing option!\n";

static const char *godbye = "Goodbye!";

static const char *menu = "\
1. Login \n\
2. Change the seat temperature \n\
3. Change the flush function \n\
4. Show current settings \n\
5. Drop a load \n\
6. Show latest notes \n\
7. Flush \n\
8. Show Log \n\
9. Logout \n\
10. Exit \n\
";

void printWelcome(void) {
    int color;

    srand (time(NULL));
    color = rand () % 6;
    printf ("%s%s%s", colors[color], banner, RESET);
    puts (welcome);
}

void printGoodbye(void) {
   puts (godbye);
}

void printError(void) {
   puts ("Something went wrong, please try again!");
}

static void printMissingLogin(void) {
   puts ("You have to be logged in!");
}

static void printMissingSL(void) {
   puts ("Seems like you're cheating on me, I can't find any load from you");
}

static void printMissingFlush(void) {
   puts ("Hey! You have to flush before you leave!\
This already smells unbearable!\n\
In fact, do you have to carry a gun license for such bombs?\n");
}

void printMenu(void) {
    puts (menu);
}

long getChoice(void) {
    char input[10];
    long choice;
    char *endptr;
    char *newline;
    printf ("%s", "Your choice: ");
    if (fgets (input, 8, stdin) == NULL) {
       if (ferror (stdin)) {
          die ("fgets", FGETS_ERROR);
       }
       if (feof (stdin)) {
          exit(0);
       }
    }
    newline = strchr(input, '\n');
    if (newline != NULL) {
       *newline = '\0';
    }
    errno = 0;
    choice = strtol (input, &endptr, 10);
    if (errno != 0 || *endptr != '\0') {
       die  ("strtol", STRTOL_ERROR);
    }
    putchar ('\n');
    return choice;
}

Profile *login(void) {
    char name[MAX_NAME_LEN+1];
    char *newline;
    char filename[SHA256_DIGEST_LENGTH*2+1];

    printf ("%s", "Please give me your name: ");
    if ((fgets (name, sizeof(name), stdin)) == NULL) {
        if (feof(stdin)) {
           return NULL;
        }
        die ("fgets", FGETS_ERROR);
    }
    newline = strchr (name, '\n');
    if (newline != NULL) {
        *newline = 0;
    }
    calcSHA256(name, filename);
    if ((checkProfile (filename)) == 1) {
       return loadProfileWrapper (filename);
    }
    return createProfile (name);
}

int logout(Profile *user) {
    int choice;
    if (!user) {
       printMissingLogin ();
       return -1;
    }
    puts("Store profile? (y/n)");
    choice = getc(stdin);
    getc(stdin); // newline
    if (choice == 'y') {
       if ((storeProfile (user)) == -1) {
          printMissingFlush ();
          return -1;
       } else {
          puts ("Hope you feel relieved now! Come back soon!");
          free (user);
          return 0;
      }
   }
   /*
    * VULN: user isn't freed here so a re-login will malloc another heap-chunk
    */
   return 0;
}

int dumpLoad(Profile *user) {
    char *buf;
    char cons[CONS_MAX_LEN];
    uint16_t weight, consistency;
    uint32_t totalLoad;
    char *newline;
    Log *newLog;
    struct timespec time1, time2;
    time1.tv_sec = 0;
    time1.tv_nsec = 500000000;

    if (user == NULL) {
        printMissingLogin ();
        return -1;
    }
    if (user->notes != NULL) {
       puts ("Holy moly you're already back to fire again? Please flush once.");
       return -1;
    }
    puts ("Alright here we go!");
    puts ("Don't hold back, give me everything you got!");
    nanosleep(&time1, &time2);
    puts ("You've landed the jumbo! Nice work!");
    srand (time(NULL));
    weight = (rand () % 100) + 300;
    printf ("Your load weights %08ug \n", weight);
    printf ("\n%s", "Please describe the consistency: ");
    if ((fgets (cons, sizeof(cons), stdin)) == NULL) {
        if (feof(stdin)) {
           return -1;
        }
        die ("fgets", FGETS_ERROR);
    }
    newline = strchr(cons, '\n');
    if (newline != NULL) {
        *newline = 0;
    }

    consistency = consistencyCalc(cons);
    buf = createNoteBuffer (user, weight, consistency);
    totalLoad = weight*100 + consistency*10;
    /*
     * VULN: deadcode to allow patching
     */
    if (!buf) {
       return -1;
    }
    puts ("Please leave a note about your gorgeous work:");
    if ((fgets (buf, totalLoad, stdin)) == NULL) {
        if (feof(stdin)) {
           return -1;
        }
        die ("fgets", FGETS_ERROR);
    }
    newline = strchr(buf, '\n');
    if (newline != NULL) {
        *newline = 0;
    }
    logList = removeUserFromLog(logList, user->id);
    newLog = genLogElem (user);
    newLog->next = logList;
    logList = newLog;

    return 0;
}

int printNotes(Profile *user) {
    if (!user) {
        printMissingLogin ();
        return -1;
    }
    if (user->notes == NULL) {
        printMissingSL ();
        return -1;
    }
    puts ("Here are your notes: ");
    puts (user->notes);
    return 0;
}

int flush(Profile *user) {
    int ret;
    if (!user) {
        printMissingLogin ();
        return -1;
    }
    if (user->notes == NULL) {
        printMissingSL ();
        return -1;
    }
    puts ("Going to flush now");
    ret = flushLoad (user);
    if (ret == 0) {
       puts ("Aaaand it's gone!");
    }
    return ret;
}

int changeSeatTemp(Profile *user) {
    int16_t temp;
    char newline;
    int ret;

    if (!user) {
        printMissingLogin ();
        return -1;
    }
    printf ("%s", "Please give me the new temperature: ");
    if ((ret = scanf ("%hd%c", &temp, &newline)) != 2) {
        if (ret == EOF) {
           die ("scanf", SCANF_ERROR);
        }
        return -1;
    }
    putchar ('\n');
    if (temp > 60) {
        puts ("Do you want to burn your ass?");
        return -1;
    } else if (temp < 10) {
         puts ("Damn, you're ass isn't that hot...");
         return -1;
    } else {
         puts ("Alright, let me arrange that for you.");
         setSeatTemp(user, temp);
         return 0;
    }

}

int changeFlushFunc(Profile *user) {
    uint8_t choice;
    char newline;
    int ret;

    if (!user) {
        printMissingLogin ();
        return -1;
    }
    puts ("0: QuickFlush");
    puts ("1: LongFlush");
    printf ("%s", "Your choice: ");
    if ((ret = scanf ("%hhu%c", &choice, &newline)) != 2) {
        if (ret == EOF) {
           die ("scanf", SCANF_ERROR);
        }
        return -1;
    }
    putchar ('\n');
    return setFlushFunc (user, choice);
}

int showSettings(Profile *user) {
    const char format[] = "%H:%M:%S";
    struct tm localTime;
    char res[32];

    if (!user) {
        printMissingLogin ();
        return -1;
    }

    printf ("ID: %lu\n", user->id);
    printf ("Name: %s\n", user->name);
    printf ("Seat temperature: %hd\n", getSeatTemp(user));
    printf ("Max. weight: %hu\n", getMaxWeight(user));

    localtime_r (&user->lastVisit, &localTime);
    if (strftime (res, sizeof (res), format, &localTime) == 0) {
         die ("strftime", STRFTIME_ERROR);
    }
    printf ("Last visit: %s\n", res);
    return 0;
}

static void printLogElement(Log *elem) {
    const char format[] = "%H:%M:%S";
    struct tm localTime;
    char res[32];
    if (elem == NULL) {
       return;
    }
    localtime_r (&elem->lastVisit, &localTime);
    if (strftime (res, sizeof (res), format, &localTime) == 0) {
         die ("strftime", STRFTIME_ERROR);
    }
    printf ("#==== %s ==== | ==== %s ====#\n", elem->name, res);
}

void printLog(void) {
    Log *current = logList;

    puts("This is highly sensitive information and we respect your privacy!");
    puts("Therefore, we anonymize the names in this log.");
    puts("But be aware that we are forced by law to hand out any data in case of a government agencies request.\n");

    puts ("#################################################################################################");
    puts ("#=========================================  Log  ===============================================#");
    puts ("#===============================================================================================#");
    puts ("#====                         Name (anonymized)                        ==== | ====   Date   ====#");
    puts ("#========================================================================== | ==================#");
    while (current != NULL) {
       printLogElement (current);
       current = current->next;
    }
    puts ("#################################################################################################");
}
