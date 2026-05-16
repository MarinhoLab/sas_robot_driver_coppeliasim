cmake_minimum_required(VERSION 3.20)
project(sas_robot_driver_coppeliasim)

# Default to C++20
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 20)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(sas_core REQUIRED)
find_package(sas_common REQUIRED)
find_package(sas_robot_driver REQUIRED)

# Python library
ament_python_install_package(${PROJECT_NAME})

####################################
# CPP Shared Library Block [BEGIN] #
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv #
# https://ros2-tutorial.readthedocs.io/en/latest/
# The most common use case is to merge everything you need to export
# into the same shared library called ${PROJECT_NAME}.
add_library(${PROJECT_NAME} SHARED
    src/${PROJECT_NAME}.cpp
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
    $<INSTALL_INTERFACE:include>)

target_include_directories(${PROJECT_NAME}
    PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    )

ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
    dqrobotics
    sas_core::sas_core
    sas_common::sas_common
    sas_robot_driver::sas_robot_driver
)

install(
    DIRECTORY include/
    DESTINATION include

    )

install(
    TARGETS ${PROJECT_NAME}
    EXPORT export_${PROJECT_NAME}
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include

    )
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #
# CPP Shared Library Block [END] #
##################################

############################
# CPP Binary Block [BEGIN] #
# vvvvvvvvvvvvvvvvvvvvvvvv #
# https://ros2-tutorial.readthedocs.io/en/latest/
# While we cant use blocks https://cmake.org/cmake/help/latest/command/block.html#command:block
# we use set--unset
set(RCLCPP_LOCAL_BINARY_NAME sas_robot_driver_coppeliasim_node)

add_executable(${RCLCPP_LOCAL_BINARY_NAME}
    src/${RCLCPP_LOCAL_BINARY_NAME}.cpp

    )

target_link_libraries(${RCLCPP_LOCAL_BINARY_NAME}
    PRIVATE
    ${PROJECT_NAME}
    )

target_include_directories(${RCLCPP_LOCAL_BINARY_NAME} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)

target_compile_features(${RCLCPP_LOCAL_BINARY_NAME} PUBLIC c_std_99 cxx_std_17)

install(TARGETS ${RCLCPP_LOCAL_BINARY_NAME}
    DESTINATION lib/${PROJECT_NAME})

unset(RCLCPP_LOCAL_BINARY_NAME)
# ^^^^^^^^^^^^^^^^^^^^^^ #
# CPP Binary Block [END] #
##########################

########################
# Launch Block [BEGIN] #
# vvvvvvvvvvvvvvvvvvvv #
# According to https://github.com/SmartArmStack/sas_robot_driver/blob/ros2/CMakeLists.txt
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)
# ^^^^^^^^^^^^^^^^^^ #
# Launch Block [END] #
######################

#########################
# Scripts Block [BEGIN] #
# vvvvvvvvvvvvvvvvvvvvv #
# https://ros2-tutorial.readthedocs.io/en/latest/
install(DIRECTORY
  scripts/
  FILE_PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ
  DESTINATION lib/${PROJECT_NAME}
)
# ^^^^^^^^^^^^^^^^^^^ #
# Scripts Block [END] #
#######################

ament_package()
