project (Demo)
cmake_minimum_required(VERSION 3.5)

add_subdirectory(shared)

get_target_property(SHARED_MODULE_INCLUDE_DIR shared_module INCLUDE_DIRECTORIES)

include_directories(${SHARED_MODULE_INCLUDE_DIR} ${CMAKE_CURRENT_BINARY_DIR})
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} ${CMAKE_CURRENT_LIST_DIR}/lib/shared_module.lib) # we use the .lib copied in custom_command below

# copy linker file to certain place where the Demo can link
add_custom_command(
    TARGET ${PROJECT_NAME}
    PRE_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_LINKER_FILE:shared_module> ${CMAKE_CURRENT_LIST_DIR}/lib/$<TARGET_LINKER_FILE_NAME:shared_module>
    COMMAND ${CMAKE_COMMAND} -E echo "copied lib to ${CMAKE_CURRENT_LIST_DIR}/lib"
    VERBATIM
)

# copy dll to exe path
add_custom_command(
    TARGET ${PROJECT_NAME}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:shared_module> $<TARGET_FILE_DIR:${PROJECT_NAME}>
    COMMAND ${CMAKE_COMMAND} -E echo "copied dll to $<TARGET_FILE_DIR:${PROJECT_NAME}>"
    VERBATIM
)