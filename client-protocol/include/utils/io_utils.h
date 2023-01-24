#ifndef _UTILS_
#define _UTILS_
int readn(int fd, void *vptr, int n);
int writen(int fd, const void *vptr, int n);
int get_json_string_from_socket(char* json_buffer, int socket_fd);
int send_json_string_to_socket(char* json_buffer, int socket_fd);
int set_nonblocking(int fd);
int get_json_string_from_pipe(char* json_buffer);
int send_json_string_to_pipe(char* json_buffer);
#endif