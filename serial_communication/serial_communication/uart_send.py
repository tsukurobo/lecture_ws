import rclpy
from rclpy.node import Node
import serial


class SerialNode(Node):
    def __init__(self):
        super().__init__("serial_node")
        self.declare_parameter("port", "/dev/ttyACM0")

        port = self.get_parameter("port").value

        self.ser = serial.Serial(port=port, baudrate=115200, timeout=1)

        self.timer = self.create_timer(1, self.send_serial)

    def send_serial(self):
        self.ser.write(b"Hello from ROS2 \n")


def main():
    rclpy.init()
    node = SerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
