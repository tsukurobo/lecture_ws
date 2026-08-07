import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial


class MotorSerial(Node):
    def __init__(self):
        super().__init__('motor_serial')
        self.declare_parameter('port', '/dev/ttyACM1')

        port = self.get_parameter('port').value

        self.ser = serial.Serial(port=port, baudrate=115200, timeout=1)
        self.subscription = self.create_subscription(
            Joy, 'joy', self.joy_callback, 10
        )
        self.get_logger().info(f'Serial port {port} opened for motor control.')

    def joy_callback(self, msg):
        # Joyの値（-1.0～1.0）をモータの値（-255～255）に変換
        left_motor = int(msg.axes[1] * 255)
        right_motor = int(msg.axes[4] * 255)

        # 「左モータ,右モータ」の形式で送信
        data = f'{left_motor},{right_motor}\n'
        self.ser.write(data.encode())
        self.get_logger().info(f'Sent to motor: {data.strip()}')


def main():
    rclpy.init()
    node = MotorSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
