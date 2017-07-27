#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include "util.h"
#include "profile.h"

void die(char *message, uint16_t code) {
    fprintf(stderr, "ERROR: %s", message);
    exit(code);
}

uint16_t consistencyCalc(char *msg) {
    uint16_t cons = 0;
    int i;

    for (i=0; i<strlen(msg); ++i) {
        cons += msg[i] % 0x100;
    }
    return cons;
}

void calcSHA256(char *name, char *hash) {
    SHA256_CTX sha256;
    unsigned char c[SHA256_DIGEST_LENGTH];
    int i;

    SHA256_Init (&sha256);
    SHA256_Update (&sha256, name, strnlen(name, MAX_NAME_LEN));
    SHA256_Final (c,&sha256);
    for(i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        sprintf (hash+(i*2), "%02x", c[i]);
    }
}
