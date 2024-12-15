# **Global Path Planning for ROS**

## **Overview**
This project focuses on implementing global path planning algorithms within a **ROS** (Robot Operating System) environment. The implementation allows for flexible selection and visualization of pathfinding algorithms, enabling smooth navigation for robots in various simulated worlds.

The project supports **multiple algorithms** like A*, Dijkstra, PRM, and others, providing modular autonomous navigation in obstacle/non obstacle environments.

---

## **Project Structure**
The repository is organized as follows:

```plaintext
global_path_planning/
├── launch/                   # ROS launch files
├── param/                    # Configuration and parameter files
├── rviz/                     # RViz visualization configurations
├── scripts/                  # Python scripts for the project
│   ├── algorithms/           # Path planning algorithms
│   │   ├── __init__.py       # Package initializer
│   │   ├── astar.py          # A* algorithm implementation
│   │   ├── dijkstra.py       # Dijkstra algorithm implementation
│   │   ├── neighbors.py      # Neighbor detection module
│   │   ├── prm.py            # Probabilistic Roadmap (PRM) implementation
│   │   ├── wt_astar.py       # Weighted A* algorithm implementation
│   │   ├── gridviz.py        # Grid visualization utilities
│   ├── path_planning_server.py # ROS server to handle path planning requests
├── pp_msgs/                  # Custom ROS message definitions (if any)
├── q_learning_world/         # Q-learning environment integration
├── ros_world/                # ROS-specific environments
├── srv_client_plugin/        # Service-client communication plugins
├── turtlebot3/               # Integration with TurtleBot3
├── CMakeLists.txt            # Build configuration for ROS
├── package.xml               # ROS package metadata
└── README.md                 # Project documentation
```
## **Steps to Run the Project**

Follow these steps to set up and execute the **Global Path Planning** project with the TurtleBot3 simulation:

---

### **1. Build the Project**
Ensure the current directory is your ROS workspace. Use `catkin_make` to build the project:

```bash
catkin_make
```
```source devel/setup.bash```
```bash
roslaunch ros_world turtlebot3_world.launch
```
```bash
roslaunch global_path_planning turtlebot3_ros_world.launch
```
```bash
rosrun global_path_planning path_planning_server.py
```

