import rclpy
from rclpy.node import Node
import serial
from std_msgs.msg import UInt16


class DistanceSensorRecv(Node):
    def __init__(self):
        super().__init__('distance_sensor_recv')
        self.declare_parameter('port', '/dev/ttyACM0')

        port = self.get_parameter('port').value

        self.publisher = self.create_publisher(UInt16, '/distance', 10)
        self.ser = serial.Serial(port, 115200, timeout=0.1)
        self.timer = self.create_timer(0.1, self.read_serial)

    def read_serial(self):
        if self.ser.in_waiting == 0:
            return

        distance = int(self.ser.readline().decode().strip())


def main():
    rclpy.init()
    node = DistanceSensorRecv()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.ser.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
