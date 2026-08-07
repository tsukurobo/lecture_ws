import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial


class MotorSerial(Node):
    def __init__(self):
        super().__init__('motor_serial')
        self.declare_parameter('port', '/dev/ttyACM0')

        # 演習3 TODO
        # 初期値255でmax_speedを宣言する
        # self.________________________________________

        port = self.get_parameter('port').value

        self.ser = serial.Serial(port=port, baudrate=115200, timeout=1)
        self.subscription = self.create_subscription(
            Joy, 'joy', self.joy_callback, 10
        )
        self.get_logger().info(f'Serial port {port} opened for motor control.')

    def joy_callback(self, msg):
        # 演習3では、ここでmax_speedの現在値を取得し、
        # 下のモータ指令値の計算に使用する

        # TODO
        # Joyの値（-1.0～1.0）を
        # モータの値（-255～255）に変換する
        # 軸番号は使用するジョイコンに合わせる
        motor1 = ______________________________
        motor2 = ______________________________

        # TODO
        # 「モータ1,モータ2\n」の文字列を作る
        data = ______________________________

        # TODO
        # 文字列をbytes型へ変換して送信する
        self.ser.write(______________________________)


def main():
    rclpy.init()
    node = MotorSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
