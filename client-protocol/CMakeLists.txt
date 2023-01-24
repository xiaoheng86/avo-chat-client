cmake_minimum_required(VERSION 3.23)
project(client_protocol C)

set(CMAKE_C_STANDARD 99)


set(
        SRC
        ${CMAKE_SOURCE_DIR}/source/base/socket_base.c
        ${CMAKE_SOURCE_DIR}/source/utils/log.c
        ${CMAKE_SOURCE_DIR}/source/utils/str_utils.c
        ${CMAKE_SOURCE_DIR}/source/utils/io_utils.c
        ${CMAKE_SOURCE_DIR}/source/base/initialize.c
        ${CMAKE_SOURCE_DIR}/source/protocol.c
        ${CMAKE_SOURCE_DIR}/source/global.c
        source/base/select_base.c include/base/select_base.h)

set(
        INCLUDE
        ${CMAKE_SOURCE_DIR}/include/base/
        ${CMAKE_SOURCE_DIR}/include/utils/
        ${CMAKE_SOURCE_DIR}/include/cJSON/
        ${CMAKE_SOURCE_DIR}/include/
)

add_executable(client_protocol ${SRC} main.c)

target_include_directories(client_protocol PUBLIC ${INCLUDE})

target_link_libraries(client_protocol PUBLIC pthread ${CMAKE_SOURCE_DIR}/lib/libcJSON.a)
