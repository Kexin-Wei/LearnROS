#! /usr/bin/python3

from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution, TextSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    urdf_path = PathJoinSubstitution(
        [
            FindPackageShare("car_description"),
            "urdf",
            "a_car.urdf.xacro",
        ]
    )

    rviz_path = PathJoinSubstitution(
        [
            FindPackageShare("car_description"),
            "rviz",
            "robot.rviz",
        ]
    )

    robot_description = ParameterValue(
        Command(["xacro ", urdf_path]),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    rviz2_node = Node(package="rviz2", executable="rviz2", arguments=["-d", rviz_path])

    return LaunchDescription(
        [
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz2_node,
        ]
    )