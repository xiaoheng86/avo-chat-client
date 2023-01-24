//
// Created by xiaoheng on 22-12-7.
//
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <malloc.h>
#include "str_utils.h"
#include "cJSON.h"
#include "log.h"

bool str_starts_with(const char *str, const char *prefix) {
    if (str == NULL || prefix == NULL) {
        return false;
    }
    while (*prefix != '\0') {
        if (*str++ != *prefix++) {
            return false;
        }
    }
    return true;
}

bool str_ends_with(const char *str, const char *suffix) {
    if (str == NULL || suffix == NULL) {
        return false;
    }
    size_t str_len = strlen(str);
    size_t suffix_len = strlen(suffix);
    if (str_len < suffix_len) {
        return false;
    }
    return strcmp(str + str_len - suffix_len, suffix) == 0;
}


bool str_contains(const char *str, const char *substr) {
    if (str == NULL || substr == NULL) {
        return false;
    }
    return strstr(str, substr) != NULL;
}

bool str_equals(const char *str1, const char *str2) {
    if (str1 == NULL || str2 == NULL) {
        return false;
    }
    return strcmp(str1, str2) == 0;
}


bool str_equals_ignore_case(const char *str1, const char *str2) {
    if (str1 == NULL || str2 == NULL) {
        return false;
    }
    return strcasecmp(str1, str2) == 0;
}

bool str_is_empty(const char *str) {
    return str == NULL || *str == '\0';
}

bool str_is_blank(const char *str) {
    if (str == NULL) {
        return true;
    }
    while (*str != '\0') {
        if (!isspace(*str++)) {
            return false;
        }
    }
    return true;
}

void str_trim(char *str) {
    if (str == NULL) {
        return;
    }
    char *start = str;
    while (*start != '\0' && isspace(*start)) {
        start++;
    }
    char *end = start;
    while (*end != '\0') {
        end++;
    }
    end--;
    while (end > start && isspace(*end)) {
        end--;
    }
    end++;
    *end = '\0';
    if (start != str) {
        while ((*str++ = *start++) != '\0');
    }
}

void str_trim_left(char *str) {
    if (str == NULL) {
        return;
    }
    char *start = str;
    while (*start != '\0' && isspace(*start)) {
        start++;
    }
    if (start != str) {
        while ((*str++ = *start++) != '\0');
    }
}

void str_trim_right(char *str) {
    if (str == NULL) {
        return;
    }
    char *end = str;
    while (*end != '\0') {
        end++;
    }
    end--;
    while (end > str && isspace(*end)) {
        end--;
    }
    end++;
    *end = '\0';
}

void str_replace(char *str, char old_char, char new_char) {
    if (str == NULL) {
        return;
    }
    while (*str != '\0') {
        if (*str == old_char) {
            *str = new_char;
        }
        str++;
    }
}

int str_split(const char *str, char delimiter, char **tokens, int max_token_count) {
    if (str == NULL || tokens == NULL || max_token_count == 0) {
        return -1;
    }
    size_t token_count = 0;
    while (*str != '\0') {
        if (token_count >= max_token_count) {
            break;
        }
        tokens[token_count++] = (char *) str;
        while (*str != '\0' && *str != delimiter) {
            str++;
        }
        if (*str == '\0') {
            break;
        }
        *(char *) str++ = '\0';
    }
    return (int) token_count;
}

void create_heartbeat_json(char* json_buffer, const char* token){
    log_debug("token is %s", token);
    cJSON* heartbeat_json = NULL;
    heartbeat_json =cJSON_CreateObject();
    if (heartbeat_json == NULL){
        log_error("create heartbeat json error");
        return;
    }
    cJSON_AddStringToObject(heartbeat_json, "token", token);
    char* json = cJSON_Print(heartbeat_json);
    strncpy(json_buffer, json, strlen(json));
    cJSON_Delete(heartbeat_json);
}

void create_connection_json(char* json_buffer, char* token, int type){
    cJSON* connection_json = NULL;
    connection_json =cJSON_CreateObject();
    if (connection_json == NULL){
        log_error("create connection json error");
        return;
    }
    cJSON_AddStringToObject(connection_json, "token", token);
    cJSON_AddNumberToObject(connection_json, "type", type);
    char* json = cJSON_Print(connection_json);
    strncpy(json_buffer, json, strlen(json));
    free(json);
    cJSON_Delete(connection_json);
}


