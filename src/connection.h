#ifndef CONNECTION_H
#define CONNECTION_H
#include <inttypes.h>
#include "profile.h"

void printWelcome(void);
void printGoodbye(void);
void printError(void);
void printMenu(void);
long getChoice(void);
Profile *login(void);
int logout(Profile *user);
int printNotes(Profile *user);
int dumpLoad(Profile *user);
int flush(Profile *user);
int changeSeatTemp(Profile *user);
int changeFlushFunc(Profile *user);
int showSettings(Profile *user);
void printLog(void);

#endif
