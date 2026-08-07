from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='joy',
            executable='joy_node',
        ),
        Node(
            package='serial_communication',
            executable='motor_serial',
        ),
    ])
