from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    pkg_bringup = get_package_share_directory('qube_bringup')
    pkg_driver = get_package_share_directory('qube_driver')

    urdf_file = os.path.join(pkg_bringup, 'urdf', 'controlled_qube.urdf.xacro')
    robot_description_content = xacro.process_file(
        urdf_file,
        mappings={
            'baud_rate': '115200',
            'device': '/dev/ttyACM0',
            'simulation': 'true',
        }
    ).toxml()
    robot_description = {'robot_description': robot_description_content}

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
        output='screen',
    )

    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            robot_description,
            os.path.join(pkg_driver, 'config', 'joint_controllers.yaml'),
        ],
        remappings=[
            ('~/robot_description', '/robot_description'),
        ],
        output='screen',
    )

    joint_state_spawner = TimerAction(period=2.0, actions=[
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['joint_state_broadcaster'],
        )
    ])

    velocity_spawner = TimerAction(period=3.0, actions=[
        Node(
            package='controller_manager',
            executable='spawner',
            arguments=['velocity_controller'],
        )
    ])

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
    )

    return LaunchDescription([rsp, control_node, joint_state_spawner, velocity_spawner, rviz])