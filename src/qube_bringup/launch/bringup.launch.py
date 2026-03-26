from launch import LaunchDescription
from launch.actions import TimerAction, DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    pkg_bringup = get_package_share_directory('qube_bringup')
    pkg_driver = get_package_share_directory('qube_driver')

    # Launch argumenter
    baud_rate_arg = DeclareLaunchArgument('baud_rate', default_value='115200')
    device_arg = DeclareLaunchArgument('device', default_value='/dev/ttyACM0')
    simulation_arg = DeclareLaunchArgument('simulation', default_value='true')

    def create_nodes(context):
        baud_rate = LaunchConfiguration('baud_rate').perform(context)
        device = LaunchConfiguration('device').perform(context)
        simulation = LaunchConfiguration('simulation').perform(context)

        urdf_file = os.path.join(pkg_bringup, 'urdf', 'controlled_qube.urdf.xacro')
        robot_description_content = xacro.process_file(
            urdf_file,
            mappings={
                'baud_rate': baud_rate,
                'device': device,
                'simulation': simulation,
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
            remappings=[('~/robot_description', '/robot_description')],
            output='screen',
        )

        joint_state_spawner = TimerAction(period=2.0, actions=[
            Node(package='controller_manager', executable='spawner',
                 arguments=['joint_state_broadcaster'])
        ])

        velocity_spawner = TimerAction(period=3.0, actions=[
            Node(package='controller_manager', executable='spawner',
                 arguments=['velocity_controller'])
        ])

        rviz = Node(package='rviz2', executable='rviz2', output='screen')

        return [rsp, control_node, joint_state_spawner, velocity_spawner, rviz]

    return LaunchDescription([
        baud_rate_arg,
        device_arg,
        simulation_arg,
        OpaqueFunction(function=create_nodes),
    ])