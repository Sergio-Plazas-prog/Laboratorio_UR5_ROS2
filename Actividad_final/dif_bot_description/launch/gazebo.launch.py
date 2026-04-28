import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    # Nombre de tu paquete
    package_name = 'dif_bot_description'
    pkg_share = get_package_share_directory(package_name)

    # 1. DEFINICIÓN DE RUTAS 
    default_model_path = os.path.join(pkg_share, 'description', 'dif_bot_description.urdf.xacro')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz', 'urdf_config.rviz')
    world_path = os.path.join(pkg_share, 'world', 'my_world.sdf')

    # 2. NODO ROBOT STATE PUBLISHER
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', LaunchConfiguration('model')]),
            'use_sim_time': True # Importante para que use el reloj de Gazebo
        }]
    )

    # 3. NODO JOINT STATE PUBLISHER 
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    # 4. NODO RVIZ
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    # 5. LANZAR GAZEBO CON EL MUNDO (Aquí conecta el world_path)
    launch_gazebo = ExecuteProcess(
        # Versión moderna
        cmd=['gz', 'sim', '-v', '4', world_path],
        output='screen'
    )
    # Nodo para meter el robot (Usando ros_gz_sim)
    spawn_entity = Node(
    	package='ros_gz_sim',
    	executable='create',
    	arguments=['-name', 'dif_bot', '-topic', 'robot_description'],
    	output='screen'
	)

    # EL RETURN: La lista de tareas para ROS
    return LaunchDescription([
        DeclareLaunchArgument(name='model', default_value=default_model_path),
        DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path),
        
        launch_gazebo,
        robot_state_publisher_node,
        joint_state_publisher_node,
        spawn_entity,
        rviz_node
    ])
