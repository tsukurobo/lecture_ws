#!/usr/bin/env python3

# Copyright 2026 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Convert Joy messages into cmd_vel commands."""

from __future__ import annotations

from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Joy

import rclpy


class JoyToCmdVelNode(Node):
    """Subscribe to Joy and publish velocity commands."""

    def __init__(self) -> None:
        super().__init__('joy_to_cmd_vel')

        self.declare_parameter('joy_topic', '/joy')
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('axis_linear', 1)
        self.declare_parameter('axis_angular', 0)
        self.declare_parameter('scale_linear', 0.5)
        self.declare_parameter('scale_angular', 1.5)
        self.declare_parameter('deadman_button', -1)

        joy_topic = self.get_parameter('joy_topic').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        self._axis_linear = int(self.get_parameter('axis_linear').value)
        self._axis_angular = int(self.get_parameter('axis_angular').value)
        self._scale_linear = float(self.get_parameter('scale_linear').value)
        self._scale_angular = float(self.get_parameter('scale_angular').value)
        self._deadman_button = int(self.get_parameter('deadman_button').value)

        self._publisher = self.create_publisher(Twist, cmd_vel_topic, 10)
        self._subscription = self.create_subscription(
            Joy,
            joy_topic,
            self._on_joy,
            10,
        )

        self.get_logger().info(
            f'Listening to {joy_topic} and publishing {cmd_vel_topic}',
        )

    @staticmethod
    def _read_axis(values: list[float], index: int) -> float:
        if index < 0 or index >= len(values):
            return 0.0
        return float(values[index])

    @staticmethod
    def _read_button(values: list[int], index: int) -> bool:
        if index < 0 or index >= len(values):
            return False
        return bool(values[index])

    def _on_joy(self, message: Joy) -> None:
        twist = Twist()

        if self._deadman_button >= 0 and not self._read_button(
            message.buttons,
            self._deadman_button,
        ):
            self._publisher.publish(twist)
            return

        twist.linear.x = self._read_axis(message.axes, self._axis_linear) * self._scale_linear
        twist.angular.z = (
            self._read_axis(message.axes, self._axis_angular) * self._scale_angular
        )
        self._publisher.publish(twist)


def main(args: list[str] | None = None) -> None:
    """Run the Joy to cmd_vel node."""
    rclpy.init(args=args)
    node = JoyToCmdVelNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
