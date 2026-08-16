#!/usr/bin/env python3
"""
Visualizer Node for verifying Detection2DArray messages.
Subscribes to raw image and detection topics, overlays bounding boxes, and displays them.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray
from cv_bridge import CvBridge
import cv2

class YoloVisualizerNode(Node):
    def __init__(self):
        super().__init__('yolo_visualizer_node')
        self.bridge = CvBridge()
        self.latest_image = None
        
        self.create_subscription(Image, '/data', self.image_callback, 10)
        self.create_subscription(Detection2DArray, '/yolo/detections', self.detection_callback, 10)
        self.pub_annotated = self.create_publisher(Image, '/yolo/annotated_image', 10)
        
        self.get_logger().info('YOLO Visualizer Node started. Subscribed to /data and /yolo/detections')

    def image_callback(self, msg):
        self.latest_image = msg

    def detection_callback(self, msg):
        if self.latest_image is None:
            return

        try:
            cv_img = self.bridge.imgmsg_to_cv2(self.latest_image, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Failed to convert image: {e}')
            return

        # Draw detections on image
        for detection in msg.detections:
            center_x = int(detection.bbox.center.position.x)
            center_y = int(detection.bbox.center.position.y)
            w = int(detection.bbox.size_x)
            h = int(detection.bbox.size_y)
            
            x1 = int(center_x - w / 2)
            y1 = int(center_y - h / 2)
            x2 = int(center_x + w / 2)
            y2 = int(center_y + h / 2)

            class_id = "Object"
            if len(detection.results) > 0:
                class_id = f"ID:{detection.results[0].hypothesis.class_id} ({detection.results[0].hypothesis.score:.2f})"

            cv2.rectangle(cv_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(cv_img, class_id, (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        annotated_msg = self.bridge.cv2_to_imgmsg(cv_img, encoding='bgr8')
        self.pub_annotated.publish(annotated_msg)

def main(args=None):
    rclpy.init(args=args)
    node = YoloVisualizerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
