import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    package_name = 'mi_robot'
    
    pkg_path = get_package_share_directory(package_name)
    xacro_file = os.path.join(pkg_path, 'urdf', 'robot.urdf.xacro')
    
    robot_description_config = xacro.process_file(xacro_file)
    params = {'robot_description': robot_description_config.toxml()}
    # nodo que  publica frames fijos 
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    # nodo que publica frames moviles 
    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
	)
    #nodo que abre la ventana de rviz 
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # 👇 Esta es la única línea nueva
        # arguments=['-d', os.path.join(pkg_path, 'rviz', 'config.rviz')]
    )
   # 4. Incluir el lanzamiento de Gazebo (Mundo vacío por defecto)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(), # El '-r' es para que arranque de una vez
    )
    # 5. Nodo para "aparecer" el robot en Gazebo (Spawn Entity)
    spawn_entity = Node(    
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'mi_rosbot'],
        output='screen'
    )

    return LaunchDescription([
        node_robot_state_publisher,
        #node_joint_state_publisher,
        #node_rviz,
        gazebo,
        spawn_entity
    ])
