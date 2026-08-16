#!/usr/bin/env python3
"""
Demo launch for the on-demand YOLO perception assignment.

Starts the image publisher (visualization aid), the YOLO service node,
the visualizer, and optionally RViz showing the annotated image.

After launch, trigger inference manually with:
    ros2 service call /yolo_detector/trigger_inference std_srvs/srv/Trigger "{}"
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('perception_assignment')
    rviz_config = os.path.join(pkg_share, 'rviz', 'yolo_demo.rviz')
    default_image = os.path.join(pkg_share, 'data', 'image_1.jpg')

    image_path = LaunchConfiguration('image_path')
    run_rviz = LaunchConfiguration('rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'image_path',
            default_value=default_image,
            description='Path to the image to process and display.'
        ),
        DeclareLaunchArgument(
            'rviz',
            default_value='true',
            description='Open RViz with the annotated image display.'
        ),
        Node(
            package='perception_assignment',
            executable='image_publisher_node',
            name='image_publisher_node',
            parameters=[{'image_path': image_path}]
        ),
        Node(
            package='perception_assignment',
            executable='yolo_service_node',
            name='yolo_service_node',
            parameters=[{'image_path': image_path}]
        ),
        Node(
            package='perception_assignment',
            executable='yolo_visualizer_node',
            name='yolo_visualizer_node'
        ),
        ExecuteProcess(
            condition=IfCondition(run_rviz),
            cmd=['rviz2', '-d', rviz_config],
            output='screen'
        ),
        LogInfo(
            msg='Trigger inference with: '
                'ros2 service call /yolo_detector/trigger_inference '
                'std_srvs/srv/Trigger "{}"'
        ),
    ])
