//
// Created by xiaoheng on 22-12-7.
//

#ifndef SERVER_PROTOCOL_STR_UTILS_H
#define SERVER_PROTOCOL_STR_UTILS_H
#include "stdbool.h"
void print_logo();
void str_trim(char *str);
bool str_equals(const char *str1, const char *str2);
bool str_contains(const char *str, const char *substr);
bool str_starts_with(const char *str, const char *prefix);
bool str_ends_with(const char *str, const char *suffix);
void create_heartbeat_json(char* json_buffer, const char* token);
void create_connection_json(char* json_buffer, char* token, int type);
#endif //SERVER_PROTOCOL_STR_UTILS_H
