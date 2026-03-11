cmake_minimum_required(VERSION 3.8)
project(gesture_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

# Note: We removed 'ament_python_install_package' to fix the error.

# Install the Python Script directly
install(PROGRAMS
  src/keyboard_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME keyboard_driver
)

# Install URDF and Launch files
install(DIRECTORY
  launch
  urdf
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
