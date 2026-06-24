from setuptools import find_packages, setup

package_name = 'lecture_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='kengo',
    maintainer_email='kengo171227@gmail.com',
    description='Joystick teleoperation node for publishing cmd_vel',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'joy_to_cmd_vel = lecture_teleop.joy_to_cmd_vel:main',
        ],
    },
)
