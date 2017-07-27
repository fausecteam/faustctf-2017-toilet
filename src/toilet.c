#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include "profile.h"
#include "connection.h"

void checkDataDir(void) {
    struct stat stat_buf;
    if (stat (BASEDIR, &stat_buf) == -1) {
        if (errno != ENOENT) {
            printError ();
            exit (EXIT_FAILURE);
        } else {
            mkdir(BASEDIR, 0700);
        }
    } else {
        if (!S_ISDIR(stat_buf.st_mode)) {
            mkdir(BASEDIR, 0700);
        }
    }
}

int main(int argc, char *argv[]) {
    long choice;

    setvbuf(stdout, NULL, _IONBF, 0);
    checkDataDir();

    if (loadLog () == -1) {
        printError ();
        exit (EXIT_FAILURE);
    }
    logList = sortLog (logList);
    printWelcome ();
    while (1) {
        printMenu ();
        choice = getChoice ();
        switch (choice) {
            case 1:
                if (global_user != NULL) {
                    puts ("You're already logged in.");
                    break;
                }
                if ((login ()) == NULL) {
                    printError ();
                }
                break;
            case 2:
                if (changeSeatTemp (global_user) == -1) {
                    printError ();
                }
                break;
            case 3:
                if (changeFlushFunc (global_user) == -1) {
                    printError ();
                }
                break;

            case 4:
                if (showSettings (global_user) == -1) {
                    printError ();
                }
                break;
            case 5:
                if (dumpLoad (global_user) == -1) {
                    printError ();
                }
                break;
            case 6:
                if (printNotes (global_user) == -1) {
                    printError ();
                }
                break;
            case 7:
                if (flush (global_user) == -1) {
                    printError ();
                }
                break;
            case 8:
                printLog ();
                break;
            case 9:
                if (logout (global_user) == -1) {
                    printError ();
                    break;
                }
                global_user = NULL;
                break;
            case 10:
                printGoodbye ();
                exit (EXIT_SUCCESS);
                break;
        }
    }
    return 0;
}
