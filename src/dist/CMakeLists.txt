cmake_minimum_required(VERSION 3.10)
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)

project(nb_plot_streamlit CXX)
set(CMAKE_CXX_STANDARD 14)

# Use Python
find_package(Python 3.9 REQUIRED)
find_package(PythonLibs 3.9 REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

# Use Boost C++ libraries
set(Boost_NO_SYSTEM_PATHS TRUE)
set(BOOST_ROOT "/opt/boost")
set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
find_package(Boost 1.77 COMPONENTS python)
include_directories(${Boost_INCLUDE_DIRS})

# Use Google Test
# Based on
# https://mola1129.dev/cmakegoogletest
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download)

if(result)
  message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()

execute_process(COMMAND ${CMAKE_COMMAND} --build . RESULT_VARIABLE result WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download)

if(result)
  message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/googletest-src ${CMAKE_CURRENT_BINARY_DIR}/googletest-build EXCLUDE_FROM_ALL)

enable_testing()
include(GoogleTest)

# Include our dist.hpp
set(BASEPATH "${CMAKE_SOURCE_DIR}")
include_directories("${BASEPATH}")

# Executable unit tests
add_executable(test_dist dist.cpp dist_impl.cpp ../../tests/test_dist.cpp)
target_link_libraries(test_dist "${Boost_LIBRARIES}" "${PYTHON_LIBRARIES}" gtest_main pthread)
gtest_add_tests(TARGET test_dist)

# A C++ library running on Python
add_library(nb_plot_streamlit SHARED dist.cpp dist_impl.cpp)
target_compile_options(nb_plot_streamlit PRIVATE "-DPIC -shared -fPIC")
target_link_options(nb_plot_streamlit PRIVATE "-DPIC -shared -fPIC")
target_link_libraries(nb_plot_streamlit "${Boost_LIBRARIES}")

message("${PYTHON_LIBRARIES}")
message("${Boost_LIBRARIES}")
