import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    # 1. Encontrar la ruta donde se instaló el paquete
    pkg_share = launch_ros.substitutions.FindPackageShare(package="dif_bot_description").find("dif_bot_description")
    
    # 2. Definir rutas por defecto para el URDF/XACRO y la configuración de RViz
    # Ajusté la ruta a 'description' para que coincida con tu carpeta anterior
    default_model_path = os.path.join(pkg_share, "description/dif_bot_description.urdf.xacro")
    default_rviz_config_path = os.path.join(pkg_share, "rviz/urdf_config.rviz")

    # 3. Nodo Robot State Publisher: Lee el XACRO y publica el árbol de TFs
    robot_state_publisher_node = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": Command(["xacro ", LaunchConfiguration("model")])}]
    )

    # 4. Nodo Joint State Publisher: Publica estados de joints (sin interfaz)
    joint_state_publisher_node = launch_ros.actions.Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        condition=launch.conditions.UnlessCondition(LaunchConfiguration("gui"))
    )

    # 5. Nodo Joint State Publisher GUI: Abre ventanitas para mover las ruedas/articulaciones
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
        condition=launch.conditions.IfCondition(LaunchConfiguration("gui"))
    )

    # 6. Nodo RViz2: El visualizador 3D
    rviz_node = launch_ros.actions.Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rvizconfig")],
    )

    # 7. Retornar la descripción completa con sus argumentos
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name="gui", default_value="True",
                                            description="Flag to enable joint_state_publisher_gui"),
        launch.actions.DeclareLaunchArgument(name="model", default_value=default_model_path,
                                            description="Absolute path to robot urdf file"),
        launch.actions.DeclareLaunchArgument(name="rvizconfig", default_value=default_rviz_config_path,
                                            description="Absolute path to rviz config file"),
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ])
