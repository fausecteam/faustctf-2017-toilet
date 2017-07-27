#ifndef PROFILE_H
#define PROFILE_H
#include <inttypes.h>
#include <time.h>
#include <openssl/sha.h>

#define MAX_NAME_LEN 64
#define MAX_WEIGHT 65535 // 2**16-1
#define BASEDIR "data"

typedef void (*flushFunc)(char *buf);

struct profile {
    char name[MAX_NAME_LEN];
    flushFunc ffunc;
    int16_t seatTemp;
    uint16_t weight;
    char *notes;
    time_t lastVisit;
    uint64_t id;
};
typedef struct profile Profile;

/*
 * Ugly hack here, but allows the exploit to work as expected
 */
Profile *global_user;


struct log {
    uint64_t id;
    char name[SHA256_DIGEST_LENGTH*2+1];
    time_t lastVisit;
    struct log *next;
};
typedef struct log Log;

/* Global log */
Log *logList;

/* Profile managment functions */

/*
 * Create a new profile
 * name: String with max. length of MAX_NAME_LEN
 * Returns the new profile or NULL if an error occurred
 */
Profile *createProfile(char *name);

/*
 * Write profile to filesystem
 * user: Particular user
 * Returns 0 if the profile was stored succesfully, -1 otherwise
 */
int storeProfile(Profile *user);

/*
 * Load profile from filesystem
 * name: Name of the profile
 * Returns the loaded profile or NULL if the profile wasn't found
 */
Profile *loadProfile(char *name);

/*
 * Check if a profile exists filesystem
 * name: Name of the profile
 * Returns 1 if the profile exists 0, otherwise
 */
int checkProfile(char *name);

/*
 *  Flush Functions
 */
void quickFlush(char *buf);

void longFlush(char *buf);

Profile *loadProfileWrapper(char *name);

/*
 * Get max. weight stored in profile
 * user: Particular profile
 * Returns the max. weight or -1 if an error occurred
 */
uint16_t getMaxWeight(Profile *user);

/*
 * Set max. weight in profile
 * user: Particular profile
 * weight: Weight to be set as maximum
 * Returns 0 if the weight was set succesfully, -1 otherwise
 */
int setMaxWeight(Profile *user, uint16_t weight);

/*
 * Get seat temperature stored in profile
 * user: Particular profile
 * Returns the seat temp or -1 if an error occurred
 */
int16_t getSeatTemp(Profile *user);

/*
 * Set seat temperature in profile
 * user: Particular profile
 * temp: Temperature to be set, has to be between 10 and 60
 * Returns 0 if the weight was set succesfully, -1 otherwise
 */
int setSeatTemp(Profile *user, int16_t temp);

/*
 * Set flush function in profile
 * user: Particular profile
 * choice: Flush function to be set; 0:quickflush, 1:longflush
 * Returns 0 if the function was set succesfully, -1 otherwise
 */
int setFlushFunc(Profile *user, uint8_t choice);

/*
 * Creates a buffer for a note in the particular profile
 * user: Particular profile
 * weight: Weight of the load
 * consistency: Number describing the consistency
 * Returns the address of the buffer or NULL if an error occurred
 */
char *createNoteBuffer(Profile *user, uint16_t weight, uint16_t consistency);

/*
 * Frees the notes buffer in the particular profile
 * user: Particular profile
 * Returns 0 if successfull or -1 otherwise
 */
int flushLoad (Profile *user);

/*
 * Generate a higscore element
 * Returns a pointer to log element or NULL if an error occurred
 */
Log *genLogElem(Profile *user);

/*
 * Load logs
 * Returns 0 if successfull or -1 if an error occurred
 */
int loadLog(void);

/*
 * Sort Log by timestamp value
 */
Log *sortLog(Log *list);

/*
 * Remove user from Log
 * log: Head element of log
 * id: ID of the particular user
 */
Log *removeUserFromLog(Log *log, uint64_t id);

/*
 * Free Log
 * log: Head element of log
 */
void freeLog(Log *log);

#endif
