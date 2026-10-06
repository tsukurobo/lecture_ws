cmake_minimum_required(VERSION 3.8)
project(lecture_teleop_cpp)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)

add_executable(joy_to_cmd_vel src/joy_to_cmd_vel.cpp)
ament_target_dependencies(
  joy_to_cmd_vel
  geometry_msgs
  rclcpp
  sensor_msgs
)

target_compile_features(joy_to_cmd_vel PUBLIC cxx_std_17)

install(
  TARGETS joy_to_cmd_vel
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
