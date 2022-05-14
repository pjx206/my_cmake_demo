# Method 1
add_llvm_library(HelloWorld MODULE Pass.cpp)


# Method 2
# if(NOT LLVM_ENABLE_RTTI)
#     set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-rtti")
# endif()

# add_library(HelloWorld MODULE Pass.cpp)