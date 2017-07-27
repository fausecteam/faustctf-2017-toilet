#ifndef UTIL_H
#include <inttypes.h>

#define MALLOC_ERROR 2
#define OPEN_ERROR 4
#define WRITE_ERROR 8
#define READ_ERROR 16
#define CLOSE_ERROR 32
#define FGETS_ERROR 64
#define OPENDIR_ERROR 128
#define STRFTIME_ERROR 256
#define STRTOL_ERROR 512
#define SCANF_ERROR 1024

/* Function for exiting the program with an error state */
void die(char *message, uint16_t code);

/* Calculates a consistency value from a given string */
uint16_t consistencyCalc(char *msg);

/* Calculates the SHA256 value from a given string */
void calcSHA256(char *name, char *hash);
#endif
