#ifndef SERVER_PROTOCOL_SOCKET_BASE_H
#define SERVER_PROTOCOL_SOCKET_BASE_H
int connect_to_server(int *connfd, char *addr, int port, int type, char *token);
#endif
