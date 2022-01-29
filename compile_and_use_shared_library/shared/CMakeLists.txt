project(shared_module)
cmake_minimum_required(VERSION 3.5)

add_library(${PROJECT_NAME} SHARED dll.c)

target_include_directories(${PROJECT_NAME} PUBLIC ${PROJECT_SOURCE_DIR}/include)