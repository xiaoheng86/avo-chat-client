//
// Created by xiaoheng on 22-12-14.
//
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "log.h"
#include "global.h"
#include "sys/epoll.h"
#include "initialize.h"

#define EVENT_MAX  1024
int PIPE_FDS[2];



void daemonize()
{
    // 使当前进程成为守护进程
    pid_t pid = fork();
    if (pid < 0) {
        log_fatal_with_errno("fork error");
        exit(-1);
    }
    if (pid > 0) {
        exit(0);
    }
    if (setsid() < 0) {
        log_fatal_with_errno("setsid error");
        exit(-1);
    }
    pid = fork();
    if (pid < 0) {
        log_fatal_with_errno("fork");
        exit(-1);
    }
    if (pid > 0) {
        exit(0);
    }
    umask(0);
    chdir("/");
    // 关闭标准输入输出
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);
    // 将标准输入输出重定向到 /dev/null和 LOG文件
    open("/dev/null", O_RDONLY);
    open(LOG_PATH, O_WRONLY | O_CREAT | O_APPEND, 0644);
    open(LOG_PATH, O_WRONLY | O_CREAT | O_APPEND, 0644);
}


void init_gtk_client(){
    // 初始化gtk客户端

    /** Generates two pipe file descriptors **/
    pipe(PIPE_FDS);
    pid_t _parent_pid = getpid();
    /** run spring boot server **/
    if (!fork()) {
        /**close parent process's log file, open new log file for electron**/
        close(0);
        close(1);
        close(2);
        open("/dev/null", O_RDONLY);
        open(GTK_LOG_PATH, O_WRONLY | O_CREAT | O_APPEND, 0644);
        open(GTK_LOG_PATH, O_WRONLY | O_CREAT | O_APPEND, 0644);
        char parent_pid[16];
        sprintf(parent_pid, "%d", _parent_pid);
        char pipe_fd[16];
        sprintf(pipe_fd, "%d", PIPE_FDS[0]);
        if(chdir(GTK_SCRIPT_PATH) == -1){
            log_fatal_with_errno("chdir");
            exit(-1);
        }
        if(execl("/home/xiaoheng/Desktop/projects/Python_projects/virtual_env/avo-API/bin/python3.7",
                 "/home/xiaoheng/Desktop/projects/Python_projects/virtual_env/avo-API/bin/python3.7", "./main.py", parent_pid, pipe_fd, NULL) == -1){
            log_fatal_with_errno("execl error");
            exit(-1);
        }
    }else{
        log_debug("waiting for SIGUSR1");
        pause();
        log_debug("SIGUSR1 received");
        close(PIPE_FDS[0]);
    }
}
