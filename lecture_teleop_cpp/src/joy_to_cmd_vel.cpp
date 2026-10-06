// Copyright 2026 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <functional>
#include <memory>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joy.hpp"

class JoyToCmdVelNode : public rclcpp::Node
{
public:
  JoyToCmdVelNode()
  : Node("joy_to_cmd_vel_node")
  {
    publisher_ =
      this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

    subscription_ =
      this->create_subscription<sensor_msgs::msg::Joy>(
      "/joy",
      10,
      std::bind(
        &JoyToCmdVelNode::on_joy,
        this,
        std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "joy_to_cmd_vel_node started");
  }

private:
  void on_joy(const sensor_msgs::msg::Joy::SharedPtr message)
  {
    geometry_msgs::msg::Twist twist;

    // TODO: Joyメッセージの値をTwistメッセージに変換する
    (void)message;

    publisher_->publish(twist);
  }

  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<JoyToCmdVelNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
