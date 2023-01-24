//
// Created by xiaoheng on 22-12-20.
//
#include <sys/select.h>
#include "global.h"
#include "stddef.h"

void arm_select(){
    FD_ZERO(&SOCK_FDS);
    FD_SET(HEARTBEAT_FD, &SOCK_FDS);
    FD_SET(NOTIFY_FD, &SOCK_FDS);
    FD_SET(FILE_FD, &SOCK_FDS);
}