#!/usr/bin/env python3
"""
Galaxea Perception Recruitment Assignment: Single-Image YOLO Service
Candidate Skeleton Code
"""

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
from std_srvs.srv import Trigger
from ultralytics import YOLO
import cv2
import os
import time


class YoloServiceNode(Node):
    def __init__(self):
        super().__init__('yolo_service_node')

        # Declare parameters
        self.declare_parameter('model_path', 'models/yolov8n.pt')
        self.declare_parameter('image_path', 'data/image_1.jpg')  # Path to the test image
        self.declare_parameter('target_color', 'red')  # Example target filtering attribute
        # Filter by YOLO class name; empty = keep all. dynamic_typing: empty list infers
        # BYTE_ARRAY in Humble, so allow overrides of any array type.
        self.declare_parameter('target_classes', [], ParameterDescriptor(dynamic_typing=True))
        self.declare_parameter('conf_thres', 0.5)  # Confidence threshold

        # Initialize YOLO Model
        self.get_logger().info('Loading YOLO model...')
        self.model = None
        target_classes_value = self.get_parameter('target_classes').value
        self.target_classes = list(target_classes_value) if target_classes_value else []
        self.conf_thres = self.get_parameter('conf_thres').get_parameter_value().double_value
        self.model_path = self.get_parameter('model_path').get_parameter_value().string_value
        try:
            self.model = YOLO(self.model_path)
            self.get_logger().info(f'YOLO model loaded from {self.model_path}')
        except Exception as e:
            self.get_logger().error(f'Failed to load YOLO model from {self.model_path}: {e}')

        # ROS 2 Publishers & Services (No Camera Subscriber needed anymore)
        self.pub_detections = self.create_publisher(
            Detection2DArray,
            '/yolo/detections',
            10
        )
        self.srv_trigger = self.create_service(
            Trigger,
            '/yolo_detector/trigger_inference',
            self.trigger_callback
        )

        self.get_logger().info('YoloServiceNode is ready! Waiting for trigger service calls...')

    def trigger_callback(self, request, response):
        """
        Trigger Service Callback:
        Reads the target image from disk and executes YOLO inference.
        """
        image_path = self.get_parameter('image_path').get_parameter_value().string_value
        self.get_logger().info(f'Trigger requested! Processing image: {image_path}')

        if not os.path.exists(image_path):
            response.success = False
            response.message = f"Image not found at {image_path}"
            return response

        # Read the image using OpenCV
        cv_img = cv2.imread(image_path)
        if cv_img is None:
            response.success = False
            response.message = f"Failed to read image at {image_path}"
            return response

        if self.model is None:
            response.success = False
            response.message = "YOLO model is not loaded. Check the 'model_path' parameter."
            return response

        # TODO 1: Perform YOLO Inference

        # TODO 2: Target Filtering Logic

        # TODO 3: Construct and Publish Detection2DArray Message



def main(args=None):
    rclpy.init(args=args)
    node = YoloServiceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
