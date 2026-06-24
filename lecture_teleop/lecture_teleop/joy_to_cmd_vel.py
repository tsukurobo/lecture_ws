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

from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Joy

import rclpy


class JoyToCmdVelNode(Node):
    # ノードの初期化
    def __init__(self):
        # ノードの初期化
        super().__init__('joy_to_cmd_vel_node')

        # パブリッシャの作成
        self._publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # サブスクライバの作成
        self.create_subscription(Joy, '/joy', self._on_joy, 10)

    # Joyメッセージを受信したときのコールバック関数
    def _on_joy(self, message):
        # Twistメッセージを作成
        twist = Twist()

        # Joyメッセージの値をTwistメッセージに変換
        
        # Twistメッセージをパブリッシュ
        self._publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = JoyToCmdVelNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
