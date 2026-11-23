cmake_minimum_required(VERSION 3.20)
project(b0_ident C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_library(b0_ident STATIC
    b0_ident.c
    b0_ident_wrap.c)

target_include_directories(b0_ident PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}")

add_executable(test_b0 test_b0.c)
target_link_libraries(test_b0 PRIVATE b0_ident)
if(NOT MSVC)
    target_link_libraries(test_b0 PRIVATE m)
endif()

# 便于在 VS 里直接 F5 调试
set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
             PROPERTY VS_STARTUP_PROJECT test_b0)
