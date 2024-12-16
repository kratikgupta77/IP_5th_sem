# p3dx_ws: Multi-Robot Algorithms Workspace

This workspace is designed for developing and simulating multi-robot algorithms using the Pioneer 3-DX (P3-DX) mobile robot in a ROS (Robot Operating System) environment.

## Overview

The `p3dx_ws` workspace integrates various packages and tools to facilitate the simulation and control of multiple P3-DX robots. It includes configurations for robot description, control, and simulation environments, enabling the development and testing of multi-robot algorithms.

## Features

- **Pioneer 3-DX Simulation**: Simulate P3-DX robots in a virtual environment using Gazebo.

- **Multi-Robot Coordination**: Develop and test algorithms for coordinating multiple robots.

- **Mapping and Navigation**: Implement mapping and navigation strategies for autonomous exploration.

## Installation

1. **Set Up ROS Environment**: Ensure that ROS is installed and properly configured on your system.

2. **Create a Catkin Workspace**: If you don't have one already, create a catkin workspace:

   ```bash
   mkdir -p ~/catkin_ws/src
   cd ~/catkin_ws/
   catkin_make
   source devel/setup.bash
   ```

3. **Clone the Repository**: Navigate to the `src` directory of your catkin workspace and clone this repository:

   ```bash
   cd ~/catkin_ws/src
   git clone https://github.com/kratikgupta77/IP_5th_sem.git
   ```

4. **Install Dependencies**: Install the necessary ROS packages:

   ```bash
   sudo apt install ros-noetic-gazebo-ros-control ros-noetic-diff-drive-controller ros-noetic-joint-state-controller ros-noetic-robot-state-publisher
   ```

5. **Build the Workspace**: After installing dependencies, build the workspace:

   ```bash
   cd ~/catkin_ws/
   catkin_make
   ```

## Usage

1. **Launch the Simulation**: To start the simulation environment with the P3-DX robots, use the following command:

   ```bash
   roslaunch p3dx_gazebo p3dx.launch
   ```

   This will launch Gazebo with the P3-DX robots in the predefined world.

2. **Control the Robots**: You can control the robots using ROS topics or by implementing custom control scripts. For example, to teleoperate the robot using a keyboard:

   ```bash
   rosrun p3dx_description <<Astar.py "your .py file name">>
   ```

   Ensure that the `cmd_vel` topic is correctly remapped to control the desired robot.

3. **Developing Algorithms**: Use this workspace to develop and test your multi-robot algorithms. Organize your packages within the `src` directory and ensure they are properly integrated with the existing setup.

## Resources

- **ROS Tutorials**: [ROS Wiki](http://wiki.ros.org/ROS/Tutorials)

- **Pioneer 3-DX Information**: [Pioneer 3-DX Specifications](https://www.mobilerobots.com/researchrobots/pioneer-3-dx)

- **Gazebo Tutorials**: [Gazebo Tutorials](http://gazebosim.org/tutorials)

## Acknowledgments

This workspace utilizes resources and packages from various open-source projects. We acknowledge the contributions of the ROS community and the developers of the packages included in this workspace.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

---

*Note: This README provides a general overview and setup instructions for the `p3dx_ws` workspace. For detailed information on specific packages and their usage, refer to the respective package documentation.* 
