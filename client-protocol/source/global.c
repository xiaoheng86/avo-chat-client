//
// Created by xiaoheng on 22-12-19.
//

#include <sys/select.h>

char* LOG_PATH = "/home/xiaoheng/Desktop/avo-demonstrate/client_c/avo.log";
char* GTK_SCRIPT_PATH = "/home/xiaoheng/Desktop/avo-demonstrate/client_c/python_resources/";
char* GTK_LOG_PATH = "/home/xiaoheng/Desktop/avo-demonstrate/client_c/avo_gtk.log";
char* TOKEN_PATH = "/home/xiaoheng/Desktop/avo-demonstrate/client_c/python_resources/storage/token.txt";
fd_set SOCK_FDS;
int HEARTBEAT_FD;
int NOTIFY_FD;
int FILE_FD;
