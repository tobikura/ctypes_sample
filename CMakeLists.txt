cmake_minimum_required(VERSION 3.26)
enable_testing()

project(ctypes_sample)

add_library(sample SHARED
    src/sample.c
)
target_compile_definitions(sample PRIVATE
)
target_include_directories(sample PUBLIC
    include
)
target_link_libraries(sample
)
set_target_properties(sample PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)
add_custom_command(TARGET sample POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:sample> ${CMAKE_SOURCE_DIR}/ctypes_sample)
set_property(TARGET sample APPEND PROPERTY ADDITIONAL_CLEAN_FILES ${CMAKE_SOURCE_DIR}/ctypes_sample/$<TARGET_FILE_NAME:sample>)

# target_compile_definitions(sample
# PUBLIC SPDLOG_TRACE_ON SPDLOG_DEBUG_ON
# )
# # statically link the runtime libraries (/MT, /MTd)
# set_property(TARGET sample PROPERTY MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
# target_compile_options(sample PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/source-charset:utf-8>)
# target_compile_options(sample PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/D_WIN32_WINNT=0x0601>)
# # Add _DEBUG for macOS With Debug build
target_compile_options(sample PRIVATE $<$<AND:$<CXX_COMPILER_ID:AppleClang>,$<CONFIG:Debug>>:-D_DEBUG>)

# # Unsafe math optimization
# target_compile_options(sample PRIVATE $<$<CXX_COMPILER_ID:GNU,AppleClang,Clang>:-funsafe-math-optimizations>)
