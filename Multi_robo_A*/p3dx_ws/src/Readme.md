# A* Multi-Robot Pathfinding using ROS and Gazebo

## Overview
This project demonstrates the implementation of the A* algorithm for multi-robot pathfinding in a simulated Gazebo environment using ROS. The simulation features the P3DX robot navigating a predefined workspace efficiently with collision avoidance.

---

## Prerequisites
Before running the project, ensure you have the following installed:

- **Ubuntu 20.04** or compatible version
- **ROS Noetic**
- **Gazebo**
- Python (with required libraries for A* implementation)

---

## Directory Structure
The workspace follows the standard ROS structure:

```
p3dx_ws/
├── src/
│   ├── p3dx_description/
│   │   ├── scripts/
│   │   │   └── a_star_multi.py  # A* pathfinding script
│   │   └── ...                  # Robot description files
│   ├── p3dx_gazebo/             # Gazebo simulation package
│   └── ...
├── devel/                       # Workspace development files
└── build/                       # Build files
```

---

## Setup Instructions

### Step 1: Build the ROS Workspace
1. Open a terminal (Terminal 1):
    ```bash
    cd p3dx_ws
    catkin_make
    source devel/setup.bash
    ```

### Step 2: Launch Gazebo Simulation
1. Run the Gazebo simulation:
    ```bash
    roslaunch p3dx_gazebo p3dx.launch
    ```

### Step 3: Start the A* Pathfinding Script
1. Open another terminal (Terminal 2):
    ```bash
    cd p3dx_ws
    source devel/setup.bash
    rosrun p3dx_description a_star_multi.py
    ```

---

## Script Location
The A* pathfinding script is located at:

```
p3dx_ws/src/p3dx_description/scripts/a_star_multi.py
```

---

## Features
- Multi-robot pathfinding using the A* algorithm.
- Collision-free navigation in a simulated Gazebo environment.
- Modular and reusable design for future projects.

---

## How It Works
1. **A* Algorithm**: The script calculates the optimal path for the robots based on grid-based navigation.
2. **ROS Integration**: The robots publish and subscribe to relevant ROS topics for real-time movement updates.
3. **Gazebo Simulation**: Visualize robot movements and verify performance in a realistic environment.

---

## Future Improvements
- Enhance scalability for a larger number of robots.
- Implement dynamic obstacle avoidance.
- Extend support for other robot types.

---

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests for improvements or new features.

---




