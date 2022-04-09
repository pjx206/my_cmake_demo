cmake_minimum_required(VERSION 3.10)

project(cython_demo)

if (NOT python_interpreter)
    find_program(python_interpreter "python")
endif()
message(STATUS "Using python: ${python_interpreter}")

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
      COMMAND ${python_interpreter} "${CMAKE_CURRENT_LIST_DIR}/py_config.py"
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


execute_process(COMMAND ${cython}
    "-3"
    ${CMAKE_CURRENT_LIST_DIR}/main.pyx)


py_config(--python-include-path python_include_dir)
py_config(--python-link-flags-cmake python_linking_data 0)

set(GENERATED_C "${CMAKE_CURRENT_LIST_DIR}/main.c")
set(GENERATED_LIB main)

include_directories(${python_include_dir})
add_library(${GENERATED_LIB} SHARED ${GENERATED_C})

if (WIN32)
    message(STATUS "building on WIN32")
    list(GET python_linking_data 0 python_libdir)
    list(GET python_linking_data 1 python_lib)
    find_library(python_link_flags ${python_lib} PATHS ${python_libdir} HINTS ${python_libdir})
    target_link_libraries(${GENERATED_LIB} PRIVATE ${python_link_flags})
endif()

if(WIN32)
    set_property(TARGET ${GENERATED_LIB} PROPERTY SUFFIX ".pyd")
endif()
