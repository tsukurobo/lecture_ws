import os
import tempfile

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import DeclareLaunchArgument
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.actions import RegisterEventHandler
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition
from launch.event_handlers import OnProcessExit
from launch.event_handlers import OnShutdown
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    sim_pkg_name = "lecture_simulation"
    desc_pkg_name = "lecture_description"

    sim_dir = get_package_share_directory(sim_pkg_name)
    desc_dir = get_package_share_directory(desc_pkg_name)
    ros_gz_sim_dir = get_package_share_directory("ros_gz_sim")

    namespace = LaunchConfiguration("namespace")
    use_sim_time = LaunchConfiguration("use_sim_time")
    headless = LaunchConfiguration("headless")
    world = LaunchConfiguration("world")
    use_robot_state_pub = LaunchConfiguration("use_robot_state_pub")

    pose = {
        "x": LaunchConfiguration("x_pose", default="1.00"),
        "y": LaunchConfiguration("y_pose", default="-1.00"),
        "z": LaunchConfiguration("z_pose", default="0.00"),
        "R": LaunchConfiguration("roll", default="0.00"),
        "P": LaunchConfiguration("pitch", default="0.00"),
        "Y": LaunchConfiguration("yaw", default="0.00"),
    }
    robot_name = LaunchConfiguration("robot_name")
    robot_sdf = LaunchConfiguration("robot_sdf")

    remappings = [("/tf", "tf"), ("/tf_static", "tf_static")]

    declare_namespace_cmd = DeclareLaunchArgument(
        "namespace", default_value="", description="Top-level namespace"
    )
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time", default_value="True", description="Use simulation clock"
    )
    declare_use_robot_state_pub_cmd = DeclareLaunchArgument(
        "use_robot_state_pub", default_value="True", description="Start robot state publisher"
    )
    declare_simulator_cmd = DeclareLaunchArgument(
        "headless", default_value="False", description="Execute gzclient"
    )
    declare_world_cmd = DeclareLaunchArgument(
        "world",
        default_value=os.path.join(sim_dir, "worlds", "field.sdf"),
        description="Full path to world model",
    )
    declare_robot_name_cmd = DeclareLaunchArgument(
        "robot_name", default_value="lecture", description="Robot name"
    )
    declare_robot_sdf_cmd = DeclareLaunchArgument(
        "robot_sdf",
        default_value=os.path.join(desc_dir, "urdf", "lecture.xacro"),
        description="Robot xacro path",
    )

    start_robot_state_publisher_cmd = Node(
        condition=IfCondition(use_robot_state_pub),
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        namespace=namespace,
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "robot_description": Command(["xacro ", robot_sdf, " prefix:=", namespace]),
            }
        ],
        remappings=remappings,
    )

    joint_state_publisher_cmd = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        name="joint_state_publisher",
        namespace=namespace,
    )

    world_sdf = tempfile.mktemp(prefix="gz_sim_", suffix=".sdf")
    world_sdf_xacro = ExecuteProcess(
        cmd=["xacro", "-o", world_sdf, ["headless:=", headless], world]
    )

    remove_temp_sdf_file = RegisterEventHandler(
        event_handler=OnShutdown(
            on_shutdown=[
                OpaqueFunction(
                    function=lambda _: os.remove(world_sdf) if os.path.exists(world_sdf) else None
                )
            ]
        )
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_sim_dir, "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": ["-r -s ", world_sdf]}.items(),
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_sim_dir, "launch", "gz_sim.launch.py")),
        condition=UnlessCondition(headless),
        launch_arguments={"gz_args": ["-v4 -g"]}.items(),
    )

    set_env_vars_resources = AppendEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        os.path.join(sim_dir, "worlds") + ":" + os.path.join(sim_dir, "models"),
    )

    gz_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(sim_dir, "launch", "spawn.launch.py")),
        launch_arguments={
            "namespace": namespace,
            "use_sim_time": use_sim_time,
            "robot_name": robot_name,
            "robot_sdf": robot_sdf,
            "x_pose": pose["x"],
            "y_pose": pose["y"],
            "z_pose": pose["z"],
            "roll": pose["R"],
            "pitch": pose["P"],
            "yaw": pose["Y"],
        }.items(),
    )

    launch_gazebo_after_xacro = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=world_sdf_xacro, on_exit=[gazebo_server, gazebo_client]
        )
    )

    launch_robot_after_xacro = RegisterEventHandler(
        event_handler=OnProcessExit(target_action=world_sdf_xacro, on_exit=[gz_robot])
    )

    ld = LaunchDescription()

    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_use_robot_state_pub_cmd)
    ld.add_action(declare_simulator_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_robot_name_cmd)
    ld.add_action(declare_robot_sdf_cmd)

    ld.add_action(set_env_vars_resources)

    ld.add_action(world_sdf_xacro)
    ld.add_action(launch_gazebo_after_xacro)
    ld.add_action(launch_robot_after_xacro)

    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(joint_state_publisher_cmd)
    ld.add_action(remove_temp_sdf_file)

    return ld
