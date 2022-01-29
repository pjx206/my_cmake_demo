project (Demo)
cmake_minimum_required(VERSION 3.5)

add_subdirectory(shared)


include_directories(shared/include)
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} ${CMAKE_CURRENT_LIST_DIR}/lib/shared_module.lib)


add_custom_command(
    TARGET ${PROJECT_NAME}
    PRE_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:shared_module> ${CMAKE_CURRENT_LIST_DIR}/lib/$<TARGET_FILE_NAME:shared_module>
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_LINKER_FILE:shared_module> ${CMAKE_CURRENT_LIST_DIR}/lib/$<TARGET_LINKER_FILE_NAME:shared_module>
    COMMAND ${CMAKE_COMMAND} -E echo "copied lib to ${CMAKE_CURRENT_LIST_DIR}/lib"
    VERBATIM
)

add_custom_command(
    TARGET ${PROJECT_NAME}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:shared_module> $<TARGET_FILE_DIR:${PROJECT_NAME}>
    COMMAND ${CMAKE_COMMAND} -E echo "copied dll to $<TARGET_FILE_DIR:${PROJECT_NAME}>"
    VERBATIM
)