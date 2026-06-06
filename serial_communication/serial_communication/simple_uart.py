import rclpy
import serial
from rclpy.node import Node


class SerialNode(Node):
    def __init__(self):
        super().__init__("serial_node")
        self.declare_parameter("port", "/dev/ttyACM0")
        port = self.get_parameter("port").value

        self.ser = serial.Serial(port=port, baudrate=9600, timeout=1)

        self.timer = self.create_timer(0.1, self.read_serial)

    def read_serial(self):
        if self.ser.in_waiting > 0:
            data = self.ser.readline().decode().strip()
            self.get_logger().info(f"Received: {data}")


def main():
    rclpy.init()
    node = SerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
