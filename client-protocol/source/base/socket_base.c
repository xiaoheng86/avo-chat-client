#include "log.h"
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "str_utils.h"
#include "io_utils.h"
#include "global.h"
#include "protocol.h"

static int try_connect_to_server(int *connfd, char *addr, int port, int type, char* token)
{
    struct sockaddr_in server_addr;
    *connfd = socket(AF_INET, SOCK_STREAM, 0);
    if (*connfd == -1) {
        log_error("socket");
        exit(1);
    }
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = inet_addr(addr);
    if (connect(*connfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        log_error("connect");
        return -1;
    }
    char json_buffer[2048];
    create_connection_json(json_buffer, token, type);
    log_info("json: %s", json_buffer);
    send_json_string_to_socket(json_buffer, *connfd);
    return 1;
}

void connect_to_server(int* connfd, char* addr, int port, int type, char *token){
    int ret = try_connect_to_server(connfd, addr, port, type, token);
    while(ret == -1){
        log_info("retrying...");
        sleep(2);
        ret = try_connect_to_server(connfd, addr, port, type, token);
    }
    switch (type) {
        case T_HEARTBEAT:
            log_info("connected to server, heartbeat fd");
            break;
        case T_NOTIFY:
            log_info("connected to server, notify fd");
            break;
        case T_FILE:
            log_info("connected to server, file fd");
            break;
        default:
            log_warn("unknown type");
    }
}