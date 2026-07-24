"""Receive VL53L0X measurements over serial and publish them to ROS 2."""

import rclpy
from rclpy.node import Node
import serial
from serial import SerialException
from std_msgs.msg import UInt16


MESSAGE_PREFIX = 'DISTANCE:'


def parse_distance(line):
    """Return a distance in millimetres from a protocol line, or None."""
    try:
        text = line.decode('ascii').strip()
    except (UnicodeDecodeError, AttributeError):
        return None

    if not text.startswith(MESSAGE_PREFIX):
        return None

    value_text = text[len(MESSAGE_PREFIX):]
    try:
        distance = int(value_text)
    except ValueError:
        return None

    if not 0 <= distance <= 65535:
        return None
    return distance


class DistanceSensorRecv(Node):
    """Publish distance measurements received from an STM32."""

    def __init__(self):
        super().__init__('distance_sensor_recv')
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('poll_period', 0.01)

        port = self.get_parameter('port').value
        baudrate = self.get_parameter('baudrate').value
        poll_period = self.get_parameter('poll_period').value

        self.publisher = self.create_publisher(UInt16, '/distance', 10)
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=0,
        )
        self.receive_buffer = bytearray()
        self.timer = self.create_timer(poll_period, self.read_serial)
        self.get_logger().info(
            f'Reading distance data from {port} at {baudrate} baud'
        )

    def read_serial(self):
        """Read all complete pending lines and publish valid measurements."""
        try:
            bytes_waiting = self.ser.in_waiting
            if bytes_waiting == 0:
                return

            self.receive_buffer.extend(self.ser.read(bytes_waiting))
            while b'\n' in self.receive_buffer:
                line, _, remainder = self.receive_buffer.partition(b'\n')
                self.receive_buffer = bytearray(remainder)
                distance = parse_distance(line)
                if distance is None:
                    continue

                message = UInt16()
                message.data = distance
                self.publisher.publish(message)

            if len(self.receive_buffer) > 256:
                self.get_logger().warning('Discarding oversized serial message')
                self.receive_buffer.clear()
        except SerialException as error:
            self.get_logger().error(f'Serial read failed: {error}')
            self.timer.cancel()

    def destroy_node(self):
        """Close the serial port before destroying the ROS node."""
        if self.ser.is_open:
            self.ser.close()
        return super().destroy_node()


def main(args=None):
    """Run the distance sensor receiver node."""
    rclpy.init(args=args)
    node = None
    try:
        node = DistanceSensorRecv()
        rclpy.spin(node)
    except SerialException as error:
        if node is None:
            print(f'Failed to open serial port: {error}')
        else:
            node.get_logger().error(f'Serial port error: {error}')
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
