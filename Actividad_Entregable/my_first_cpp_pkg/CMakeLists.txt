cmake_minimum_required(VERSION 3.8)
project(my_first_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(my_first_cpp_node src/my_first_cpp_node.cpp)
add_executable(talker_node src/publisher_member_function.cpp)
add_executable(listener_node src/subscriber_member_function.cpp)

target_include_directories(my_first_cpp_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>)
target_compile_features(my_first_cpp_node PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  my_first_cpp_node
  "geometry_msgs"

)

ament_target_dependencies(
  talker_node
  "geometry_msgs"
  "rclcpp"
  "std_msgs"

)

ament_target_dependencies(listener_node rclcpp std_msgs)

install(TARGETS my_first_cpp_node
  talker_node
  listener_node
  DESTINATION lib/${PROJECT_NAME})




if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
