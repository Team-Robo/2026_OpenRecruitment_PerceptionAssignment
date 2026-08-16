import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'perception_assignment'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'models'), glob('models/*')),
        (os.path.join('share', package_name, 'data'), glob('data/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Team Robo',
    maintainer_email='teamrobontu@gmail.com',
    description='ROS 2 Recruitment Task for Perception Pipeline',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_publisher_node = perception_assignment.image_publisher_node:main',
            'yolo_service_node = perception_assignment.yolo_service_node:main',
            'yolo_visualizer_node = perception_assignment.yolo_visualizer_node:main',
        ],
    },
)