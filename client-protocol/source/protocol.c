#include <bits/types/FILE.h>
#include <stdio.h>
#include <unistd.h>
#include "global.h"
#include "io_utils.h"
#include "str_utils.h"
#include "log.h"
extern char* TOKEN;
//
// Created by xiaoheng on 22-12-19.
//

void SIGUSR1_handler(int sig){
    log_debug("SIGUSR1_handler");
}

void SIGUSR2_handler(int sig){
    log_debug("SIGUSR2_handler");
    char buffer[16];
    while(read(HEARTBEAT_FD, buffer, 1024) == 0){
        log_info("close client success");
        exit(0);
    }
}

void handle_heartbeat(const char* token){
    char json_buffer[65536];
    get_json_string_from_socket(json_buffer, HEARTBEAT_FD);
    log_debug("heartbeat received", json_buffer);
    log_debug("json: %s", json_buffer);
    log_trace("token is %s", token);
    create_heartbeat_json(json_buffer, token);
    send_json_string_to_socket(json_buffer, HEARTBEAT_FD);
    log_debug("heartbeat json sent");
    log_debug("json: %s", json_buffer);
}

void handle_notify(){
    char json_buffer[65536];
    get_json_string_from_socket(json_buffer, NOTIFY_FD);
    log_debug("notify received", json_buffer);
    log_debug("json: %s", json_buffer);
    send_json_string_to_pipe(json_buffer);
    log_debug("json sent through pipe");
}