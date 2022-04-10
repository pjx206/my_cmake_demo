cmake_minimum_required(VERSION 3.12)

project(cython_demo)

if (NOT Python3_FOUND)
    find_package(Python3 COMPONENTS Interpreter)
endif()
message(STATUS "Using python: ${Python3_EXECUTABLE}")

if (NOT cython)
    find_program(cython "cython")
endif()
message(STATUS "Using cython: ${cython}")


macro(py_config option output_var)
    if(${ARGC} GREATER 2)
        set(is_list ${ARGV2})
    else()
        set(is_list "")
    endif()

    execute_process(
      COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_LIST_DIR}/py_config.py"
              ${option}
      OUTPUT_VARIABLE ${output_var}
      OUTPUT_STRIP_TRAILING_WHITESPACE)

    if ("${${output_var}}" STREQUAL "")
        message(FATAL_ERROR "Error: Calling py_config.py ${option} returned no output.")
    endif()
    if(is_list)
        string (REPLACE " " ";" ${output_var} "${${output_var}}")
    endif()
endmacro()


py_config(--python-include-path python_include_dir)
py_config(--python-link-flags-cmake python_linking_data 0)

set(GENERATED_C "${CMAKE_CURRENT_LIST_DIR}/main.c")
set(PY_MOD_NAME main)

add_custom_command(
    OUTPUT ${GENERATED_C}
    PRE_BUILD
    COMMAND ${cython} "-3" ${CMAKE_CURRENT_LIST_DIR}/main.pyx
    VERBATIM
    DEPENDS ${CMAKE_CURRENT_LIST_DIR}/main.pyx  # so that the C file will be regenerated when changes are applied to pyx
)

include_directories(${python_include_dir})
add_library(${PY_MOD_NAME} SHARED ${GENERATED_C})


if (WIN32)
    message(STATUS "building on WIN32")
    list(GET python_linking_data 0 python_libdir)
    list(GET python_linking_data 1 python_lib)
    find_library(python_link_flags ${python_lib} PATHS ${python_libdir} HINTS ${python_libdir})
    target_link_libraries(${PY_MOD_NAME} PRIVATE ${python_link_flags})
endif()

if(WIN32)
    set_property(TARGET ${PY_MOD_NAME} PROPERTY SUFFIX ".pyd")
endif()

if(UNIX)
    set_property(TARGET ${PY_MOD_NAME} PROPERTY PREFIX "")
endif()