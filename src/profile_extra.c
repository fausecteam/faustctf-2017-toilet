#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "profile.h"

__attribute__((aligned(0x1000)))
Profile *loadProfileWrapper(char *name) {
    if (!name) {
        return NULL;
    }
    return loadProfile(name);
}

void quickFlush(char *buf) {
    printf ("%s\n\n", buf);
    free (buf);
}

void longFlush(char *buf) {
    char *curr = buf;
    struct timespec time1, time2;
    time1.tv_sec = 0;
    time1.tv_nsec = 100000000;

    while (*curr != 0x00) {
        putc (*curr, stdout);
        curr++;
        nanosleep(&time1, &time2);
    }
    puts("\n");
    free (buf);
}
