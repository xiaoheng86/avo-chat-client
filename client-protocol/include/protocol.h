//
// Created by xiaoheng on 22-12-19.
//

#ifndef CLIENT_PROTOCOL_PROTOCOL_H
#define CLIENT_PROTOCOL_PROTOCOL_H
#define T_HEARTBEAT 1
#define T_NOTIFY 2
#define T_FILE 3

void SIGUSR1_handler(int sig);
void handle_heartbeat(const char *token);
void handle_notify();
void SIGUSR2_handler(int sig);

#endif //CLIENT_PROTOCOL_PROTOCOL_H
