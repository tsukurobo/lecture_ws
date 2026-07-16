from setuptools import find_packages
from setuptools import setup

package_name = "serial_communication"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="haru",
    maintainer_email="pafupafuXD3.3@gmail.com",
    description="TODO: Package description",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "uart_recv = serial_communication.uart_recv:main",
            "uart_send = serial_communication.uart_send:main",
        ],
    },
)
