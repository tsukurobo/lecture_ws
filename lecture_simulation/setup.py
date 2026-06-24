from glob import glob
import os

from setuptools import find_packages
from setuptools import setup

package_name = "lecture_simulation"

field_files = [f for f in glob("models/field/*") if os.path.isfile(f)]

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "config"), glob("config/*")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*")),
        (os.path.join("share", package_name, "models/field"), field_files),
        (os.path.join("share", package_name, "models/field/meshes"), glob("models/field/meshes/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="vscode",
    maintainer_email="kengo171227@gmail.com",
    description="Simulation package for Tourobo 2026",
    license="TODO: License declaration",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [],
    },
)
