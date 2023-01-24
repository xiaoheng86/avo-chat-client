#include "io_utils.h"
#include <stdlib.h>
#include "select_base.h"
#include <sys/epoll.h>
#include <unistd.h>
#include <signal.h>
#include "log.h"
#include "str_utils.h"
#include "socket_base.h"
#include "global.h"
#include "protocol.h"
#include "initialize.h"
#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 5000

void sigchld_handler(int sig);
char TOKEN[2048] = {'\0'};


void load_token();

int main(int argc, char *argv[]) {
    log_debug("pid %ld", getpid());
    signal(SIGUSR1, SIGUSR1_handler);
    signal(SIGUSR2, SIGUSR2_handler);
    signal(SIGPIPE, SIG_IGN);
    signal(SIGCHLD, sigchld_handler);

    init_gtk_client();
    load_token();

    log_debug("TOKEN: %s", TOKEN);
    log_debug("-------------------------");
    connect_to_server(&HEARTBEAT_FD, SERVER_IP, SERVER_PORT, T_HEARTBEAT, TOKEN);
    connect_to_server(&NOTIFY_FD, SERVER_IP, SERVER_PORT, T_NOTIFY, TOKEN);
    connect_to_server(&FILE_FD, SERVER_IP, SERVER_PORT, T_FILE, TOKEN);

    arm_select();
    for (;;) {
        select(MAX_EVENTS, &SOCK_FDS, NULL, NULL, NULL);
        for (int i = 0; i < MAX_EVENTS; ++i) {
            if (FD_ISSET(i, &SOCK_FDS)) {
                if (i == HEARTBEAT_FD) {
                    handle_heartbeat(TOKEN);
                } else if (i == NOTIFY_FD) {
                    handle_notify();
                } else if (i == FILE_FD) {
                    //handle_file();
                } else {
                    log_warn("unknown fd");
                }
            }
        }
        arm_select();
    }
}

void load_token() {
    log_debug("loading token from local file: %s", TOKEN_PATH);
    FILE *fp = fopen(TOKEN_PATH, "r");
    if (fp == NULL) {
        log_error("fopen");
        exit(1);
    }
    log_debug("file opened");
    char token_buffer[2048];
    fgets(token_buffer, 2048, fp);
    strncpy(TOKEN, token_buffer, 2048);
    fclose(fp);
}

void sigchld_handler(int sig){
    log_info("child process exited unexpectedly");
    exit(-1);
}
