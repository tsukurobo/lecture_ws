import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial


class MotorSerial(Node):
    def __init__(self):
        super().__init__("motor_serial")
        self.declare_parameter("port", "/dev/ttyACM0")

        # 演習3 TODO
        # 初期値255でmax_speedを宣言する
        self.declare_parameter(
            "Max_Speed",
            20,
        )

        port = self.get_parameter("port").value

        self.ser = serial.Serial(port=port, baudrate=115200, timeout=1)
        self.subscription = self.create_subscription(Joy, "joy", self.joy_callback, 10)

        self.get_logger().info(f"Serial port {port} opened for motor control.")

    def joy_callback(self, msg):
        # 演習3では、ここでmax_speedの現在値を取得し、
        # 下のモータ指令値の計算に使用する
        max_value = self.get_parameter("Max_Speed").value

        # TODO
        # Joyの値（-1.0～1.0）を
        # モータの値（-255～255）に変換する
        # 今回は絶対値10以下に変化
        # 軸番号は使用するジョイコンに合わせる
        inputx = int(msg.axes[0] * max_value)
        inputy = int(msg.axes[1] * max_value)
        inputr = int(msg.axes[3] * max_value)

        s = 1.0 / math.sqrt(2.0)

        motor1 = int(inputx * s + inputy * s + inputr)
        motor3 = int(-(inputx * s + inputy * s) + inputr)
        motor2 = int(-(inputx * s - inputy * s) + inputr)
        motor4 = int(inputx * s - inputy * s + inputr)

        # TODO
        # 「モータ1,モータ2\n」の文字列を作る
        if abs(motor1) > 0.05 or abs(motor2) > 0.05 or abs(motor3) > 0.05 or abs(motor4) > 0.05:
            data = f"{motor1},{motor2},{motor3},{motor4}\n"
        else:
            data = "0,0,0,0\n"

        self.get_logger().info(data)

        # TODO
        # 文字列をbytes型へ変換して送信する
        self.ser.write(data.encode())


def main():
    rclpy.init()
    node = MotorSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
