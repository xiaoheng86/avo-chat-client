//
// Created by xiaoheng on 22-12-19.
//

#ifndef CLIENT_PROTOCOL_GLOBAL_H
#define CLIENT_PROTOCOL_GLOBAL_H
#include <bits/types/FILE.h>
#include <sys/select.h>
#include "signal.h"
#define MAX_EVENTS 128

extern char* LOG_PATH;
extern char* GTK_SCRIPT_PATH;
extern char* GTK_LOG_PATH;
extern char* TOKEN_PATH;
extern pid_t CHILD_PID;
extern fd_set SOCK_FDS;
extern int HEARTBEAT_FD;
extern int NOTIFY_FD;
extern int FILE_FD;
#endif //CLIENT_PROTOCOL_GLOBAL_H
