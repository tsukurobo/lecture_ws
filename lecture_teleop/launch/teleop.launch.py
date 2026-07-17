from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription(
        [
            Node(
                package="joy",
                executable="joy_node",
            ),
            Node(
                package="lecture_teleop",
                executable="joy_to_cmd_vel",
            ),
            Node(
                package="turtlesim",
                executable="turtlesim_node",
                remappings=[("/turtle1/cmd_vel", "/cmd_vel")],
            ),
        ]
    )
