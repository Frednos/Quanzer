from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro


def generate_launch_description():
    pkg_share = get_package_share_directory("qube_description")

    # URDF/Xacro
    urdf_file = os.path.join(pkg_share, "urdf", "qube.urdf.xarco")
    robot_description_content = xacro.process_file(urdf_file).toxml()

    # Robot state publisher
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description_content}],
    )

    # Joint state publisher GUI
    jsp_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
    )
    # RViz (bruk config hvis den finnes)
    rviz_config_file = os.path.join(pkg_share, "config", "view_model.rviz")
    rviz_args = ["-d", rviz_config_file] if os.path.exists(rviz_config_file) else []

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=rviz_args,
    )
    return LaunchDescription([rsp, jsp_gui, rviz])