"""Tests for the distance sensor serial protocol."""

from serial_communication.distance_sensor_recv import parse_distance


def test_parse_distance():
    assert parse_distance(b'DISTANCE:123\n') == 123
    assert parse_distance(b'DISTANCE:0\r\n') == 0
    assert parse_distance(b'DISTANCE:65535\n') == 65535


def test_reject_invalid_lines():
    assert parse_distance(b'Adafruit VL53L0X test\n') is None
    assert parse_distance(b'DISTANCE:OUT_OF_RANGE\n') is None
    assert parse_distance(b'DISTANCE:-1\n') is None
    assert parse_distance(b'DISTANCE:65536\n') is None
    assert parse_distance(b'\xff\n') is None
