# Perception Recruitment Assignment

This is a ROS 2 On-Demand Edge YOLO Detection starter kit. 


**TL;DR for assignment:**

1. Pick one language track: Complete the provided **Python** skeleton, OR rewrite the node entirely in **C++** (highly encouraged for lower latency to score well in assignment).
2. Pick your engine: A base `yolov8n.pt` is provided, but you are free to swap the model for optimization.
3. Write the logic: Implement a ROS 2 Service that reads a single image and publishes the bounding boxes *only* when triggered.
4. Submit your code + an `README.md`** ([See Section 6](#6-what-to-submit)). 

---

## 1. Package Structure

```text
perception_assignment/
├── README.md                    <- You are here
├── package.xml                  
├── setup.py                     
├── setup.cfg
├── launch/                      
│   └── demo.launch.py           <- One-shot demo (node + visualizer + RViz)
├── rviz/                        
│   └── yolo_demo.rviz           <- RViz config showing /yolo/annotated_image
├── models/                      
│   └── yolov8n.pt               <- Default model 
├── perception_assignment/
│   ├── __init__.py
│   ├── image_publisher_node.py  <- Demo helper: throttled static image publisher
│   ├── yolo_service_node.py     <- The Python skeleton you need to complete (if choosing Python)
│   └── yolo_visualizer_node.py  <- A provided visualization tool for your bounding boxes
└── data/                         <- Sample test images
    └── image_1.jpg ... image_5.jpg
```

---

## 2. The Challenge & Rules

Unlike continuous detection streams which consume too much CPU/GPU, our robot operates in a resource-constrained environment. Your node must run silently in the background. When a specific ROS 2 Service is called, it will read a single test image from the disk, run YOLO inference, and return the result.

| #   | Rule                               | Detail                                                                                                                                       |
| --- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **On-Demand Inference Only** | Do NOT run inference in a continuous loop. Inference must ONLY execute when the `std_srvs/srv/Trigger` service is called.                    |
| 2   | **Language Choice (C++ / Python)** | You can fill in the `# TODO` in `yolo_service_node.py`, OR you can create a new C++ node (`yolo_service_node.cpp`) to replace it.            |
| 3   | **Model Freedom** | You can use the provided `yolov8n.pt`, or replace it with your optimized model.      |
| 4   | **Standard ROS Output** | The final output must be published as a standard `vision_msgs/msg/Detection2DArray`.                                                         |

---

## 3. Inputs & Outputs Specifications

Whether you use Python or C++, your node must conform to the following ROS 2 interfaces:

* **Node Name:** `yolo_service_node`
* **Node Parameter:** `image_path` (string) - The absolute or relative path to the image you want to process.
* **Trigger Service Name:** `/yolo_detector/trigger_inference` (`std_srvs/srv/Trigger`)
* **Detection Output Topic:** `/yolo/detections` (`vision_msgs/msg/Detection2DArray`)

---

## 4. One-time Setup & Build

Clone this repository into your ROS 2 Workspace (Humble or Jazzy) and build it:

```bash
cd ~/ros2_ws/src
git clone git@github.com:Team-Robo/perception_assignment.git
cd ~/ros2_ws

# Install ROS dependencies (Make sure you have vision_msgs installed)
sudo apt update
sudo apt install ros-$ROS_DISTRO-vision-msgs ros-$ROS_DISTRO-cv-bridge

# Build the package
colcon build --packages-select perception_assignment
source install/setup.bash
```

*(Note: If you use additional Python libraries please document them in your submission).*

---

## 5. How to Test Your Node

1. **Place a test image:** Put any `.jpg` image (e.g., `test.jpg`) containing multiple objects in your workspace.
2. **Run your YOLO Service node (passing the image path as a parameter):**
   ```bash
   ros2 run perception_assignment yolo_service_node --ros-args -p image_path:="test.jpg"
   ```
3. **In a separate terminal, run the visualizer node (Optional):**
   ```bash
   ros2 run perception_assignment yolo_visualizer_node
   ```
4. **Trigger the inference manually:**
   ```bash
   ros2 service call /yolo_detector/trigger_inference std_srvs/srv/Trigger "{}"
   ```
5. **Verify the output:** Check if your node publishes the correct filtered Bounding Boxes to `/yolo/detections`.

---

### 5.1 One-Shot Demo (RViz, optional)

The package ships a demo launch file that starts the image publisher (`image_publisher_node`), the YOLO service node, the visualizer, and RViz showing the annotated result:

```bash
ros2 launch perception_assignment demo.launch.py
```

Then trigger inference in a separate terminal:

```bash
ros2 service call /yolo_detector/trigger_inference std_srvs/srv/Trigger "{}"
```

Notes:
- `image_publisher_node` is a **visualization aid only**. It throttles the selected image to `/data` at a few Hz so the visualizer/RViz always have an Image stream. It is *not* part of the challenge and does not perform any inference.
- Pass a different image with `image_path:=/path/to/your.jpg` (forwarded to both the publisher and the service node).
- For headless systems, skip RViz with `rviz:=false`.

---

## 6. What to Submit

Please push your code to a GitHub repository and share the link with us. Your submission must include:

1. **Your working ROS 2 package:** Either the completed Python version or your new C++ version.
2. **Your model file:** If you tried another model, please include it in the `models/` folder.
3. **An `README.md`:** A file at the root of your repository covering:
   * **Language & Engine Choice:** Which language and inference engine did you use and why?
   * **Strategy:** What are your strategies for optimization?
   * **Performance:** What is the average single-frame inference latency (in milliseconds) on your machine? (Please specify your CPU/GPU hardware).
   * **Setup Instructions:** Any extra pip or apt packages we need to install before running your code.

Good luck, and we look forward to reviewing your approach!
