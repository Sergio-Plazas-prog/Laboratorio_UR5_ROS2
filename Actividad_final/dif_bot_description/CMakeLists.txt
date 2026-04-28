cmake_minimum_required(VERSION 3.8)
project(dif_bot_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 1. Encontrar dependencias
find_package(ament_cmake REQUIRED)

# ==========================================================
# 2. INSTRUCCIÓN DE INSTALACIÓN
# ==========================================================
# Aquí le decimos a ROS que copie tus carpetas al directorio 'share'
install(DIRECTORY
  description
  launch
  rviz
  world
  DESTINATION share/${PROJECT_NAME}
)

# 3. Pruebas y Linters (Opcional)
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# 4. Empaquetar todo
ament_package()
