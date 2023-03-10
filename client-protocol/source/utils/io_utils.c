#include<stddef.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include "log.h"
#include "cJSON.h"
extern int PIPE_FDS[2];
#define SOCKET_MSG_DIGIT_NUM 6
#define SOCKET_BUFSIZE 65536
#define PIPE_MSG_DIGIT_NUM 4
#define PIPE_MSG_BUFSIZE 1024



/** read n bytes from a file descriptor
 *
 * @param fd the file descriptor
 * @param vptr the buffer to store the data
 * @param n the number of bytes to read
 * @return -1 indicates error, 0 indicates connection closed, >=0 indicates bytes read.
 * Note: this function will block until all n bytes are read,
 *       when peer closed the connection, the process will deal with the TCP closing routine then return number of bytes read.
 *       The reason to close the connection in this reading function other than defer it in signal handler
 *       is to avoid that the peer closed the connection but the process still try to write to the peer. It may cause problems
 *       like SIGPIPE and TCP RESET which could be very tricky.
 */

int readn(int fd, void *vptr, int n)
{

    int  nleft = n;
    int nread = 0;
    char   *ptr;

    ptr = vptr;
    nleft = n;
    while (nleft > 0) {
        if ( (nread = (int)read(fd, ptr, nleft)) < 0) {
            if (errno == EINTR) {
                nread = 0;
            }/* and call read() again */
        } else if(errno == EWOULDBLOCK || errno == EAGAIN){
            nread = 0;
        }
        nleft -= nread;
        ptr += nread;
    }
    return n - nleft;         /* return >= 0*/
}


// write n bytes from a file descriptor
int writen(int fd, const void *vptr, int n)
{
    int nleft;
    int nwritten = 0;
    const char *ptr;

    ptr = vptr;
    nleft = n;
    while (nleft > 0) {
        if ( (nwritten = (int)write(fd, ptr, nleft)) <= 0) {
            if (nwritten < 0&& errno == EINTR){
                    nwritten = 0;
                }
            /* and call write() again */
            else{
                log_error_with_errno("writen error");
                return (-1);    /* error */
            }
        }
        nleft -= nwritten;
        ptr += nwritten;
    }
    return n;
}

// read a line from a file descriptor
ssize_t readline(int fd, void *vptr, size_t maxlen)
{
    ssize_t n, rc;
    char    c, *ptr;

    ptr = vptr;
    for (n = 1; n < maxlen; n++) {
again:
        if ( (rc = read(fd, &c, 1)) == 1) {
            *ptr++ = c;
            if (c == '\n')
                break;          /* newline is stored, like fgets() */
        } else if (rc == 0) {
            *ptr = 0;
            return (n - 1);     /* EOF, n - 1 bytes were read */
        } else {
            if (errno == EINTR)
                goto again;
            return (-1);        /* error, errno set by read() */
        }
    }
    *ptr = 0;                   /* null terminate like fgets() */
    return (n);
}



int get_json_string_from_socket(char* json_buffer, int socket_fd){
    char message_size[SOCKET_MSG_DIGIT_NUM+1] = {'\0'};
    int read_fd = socket_fd;
    int read_size = readn(read_fd, message_size, SOCKET_MSG_DIGIT_NUM);
    if(read_size != SOCKET_MSG_DIGIT_NUM){
        log_error("read size error");
        return -1;
    }
    log_trace("message size: %s", message_size);

    int json_size = atoi(message_size);
    if(json_size > SOCKET_BUFSIZE){
        log_error("json size error");
        return -1;
    }

    read_size = readn(read_fd, json_buffer, json_size);
    if(read_size != json_size){
        log_error("read size error");
        return -1;
    }else if (read_size == 0){
        log_error("socket closed %d", read_fd);
        return -1;
    }
    json_buffer[read_size] = '\0';
    return 0;
}


int send_json_string_to_socket(char* json_buffer, int socket_fd){
    int json_size = (int)strlen(json_buffer);
    if(json_size > SOCKET_BUFSIZE){
        log_error("json size error");
        return -1;
    }
    char message_size[SOCKET_MSG_DIGIT_NUM+1] = {'\0'};
    sprintf(message_size, "%06d", json_size);
    int write_fd = socket_fd;
    int write_size = writen(write_fd, message_size, SOCKET_MSG_DIGIT_NUM);
    if(write_size != SOCKET_MSG_DIGIT_NUM){
        log_error("write size error");
        return -1;
    }
    write_size = writen(write_fd, json_buffer, json_size);
    if(write_size != json_size){
        log_error("write size error");
        return -1;
    }
    return 0;
}



//send a json string to pipe
int send_json_string_to_pipe(char* json_buffer){
    int json_size = (int)strlen(json_buffer);
    if(json_size > PIPE_MSG_BUFSIZE){
        log_error("json size error");
        return -1;
    }
    char message_size[PIPE_MSG_DIGIT_NUM+1] = {'\0'};
    sprintf(message_size, "%04d", json_size);
    int write_fd = PIPE_FDS[1];
    int write_size = writen(write_fd, message_size, PIPE_MSG_DIGIT_NUM);
    if(write_size != PIPE_MSG_DIGIT_NUM){
        log_error("write size error");
        return -1;
    }
    write_size = writen(write_fd, json_buffer, json_size);
    if(write_size != json_size){
        log_error("write size error");
        return -1;
    }
    return 0;
}



// get a json string from pipe
int get_json_string_from_pipe(char* json_buffer){
    char message_size[PIPE_MSG_DIGIT_NUM+1] = {'\0'};
    int read_fd = PIPE_FDS[0];
    int read_size = readn(read_fd, message_size, PIPE_MSG_DIGIT_NUM);
    if(read_size != PIPE_MSG_DIGIT_NUM){
        log_error("read size error");
        return -1;
    }else if (read_size == 0){
        log_error("socket closed %d", read_fd);
        return -1;
    }

    int json_size = atoi(message_size);
    if(json_size > PIPE_MSG_BUFSIZE){
        log_error("json size error");
        return -1;
    }
    read_size = readn(read_fd, json_buffer, json_size);
    if(read_size != json_size){
        log_error("read size error");
        return -1;
    }else if (read_size == 0){
        log_error("socket closed %d", read_fd);
        return -1;
    }
    json_buffer[json_size] = '\0';
    return 0;
}




int set_nonblocking(int fd){
    int old_option = fcntl(fd, F_GETFL);
    int new_option = old_option | O_NONBLOCK;
    fcntl(fd, F_SETFL, new_option);
    return old_option;
}

