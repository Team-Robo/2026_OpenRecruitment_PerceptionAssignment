#!/usr/bin/env python3
"""
Image Publisher Node (visualization aid).

Publishes a single image from disk to a topic at a fixed rate so that
visualization nodes (e.g. the YOLO visualizer or RViz) always have an
Image stream to display. This is a demo helper and is NOT part of the
on-demand inference challenge.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher_node')
        self.bridge = CvBridge()

        self.declare_parameter('image_path', 'data/image_1.jpg')
        self.declare_parameter('topic', '/data')
        self.declare_parameter('rate_hz', 5.0)

        image_path = self.get_parameter('image_path').get_parameter_value().string_value
        topic = self.get_parameter('topic').get_parameter_value().string_value
        rate_hz = self.get_parameter('rate_hz').get_parameter_value().double_value

        cv_img = cv2.imread(image_path)
        if cv_img is None:
            self.get_logger().error(f'Failed to read image: {image_path}')
            raise SystemExit(1)

        self.msg = self.bridge.cv2_to_imgmsg(cv_img, encoding='bgr8')
        self.msg.header.frame_id = 'camera'

        self.publisher = self.create_publisher(Image, topic, 10)
        self.timer = self.create_timer(1.0 / rate_hz, self.timer_callback)

        self.get_logger().info(
            f'Publishing {image_path} to {topic} at {rate_hz:.1f} Hz'
        )

    def timer_callback(self):
        self.msg.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
