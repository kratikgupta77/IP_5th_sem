# Multi Husky Square

This package provides a simulation environment for multiple Clearpath Husky robots navigating in a square formation using ROS and Gazebo.

## Features

- **Multi-Robot Simulation**: Simulate multiple Husky robots within a Gazebo environment.
- **Square Formation Navigation**: Implement and test square formation algorithms for coordinated robot movement.
- **ROS Integration**: Utilize ROS for communication and control between robots.

## Prerequisites

Before using this package, ensure the following dependencies are installed:

- **ROS Noetic**: The Robot Operating System framework.
- **Gazebo**: The simulation environment.
- **Husky Packages**: Common ROS packages for the Clearpath Husky, usable for both simulation and real robot operation. 

Install the necessary packages:

```bash
sudo apt-get install ros-noetic-husky-simulator ros-noetic-husky-navigation ros-noetic-husky-control
```

## Installation

1. **Clone the Repository**:

   ```bash
   cd ~/catkin_ws/src
   git clone https://github.com/kratikgupta77/IP_5th_sem.git
   ```

2. **Build the Package**:

   ```bash
   cd ~/catkin_ws
   source ~/.bashrc
   catkin_make
   ```

3. **Source the Workspace**:

   ```bash
   source devel/setup.bash
   ```

## Usage

To launch the multi-Husky square formation simulation:

```bash
roslaunch turtle_pentagon move_husky.launch
```

This command will:

- Initialize the Gazebo simulation environment.
- Spawn multiple Husky robots.
- Execute the square formation navigation algorithm.

## Configuration

- **Number of Robots**: Modify the `num_robots` parameter in the launch file to change the number of simulated Huskies.
- **Formation Parameters**: Adjust the `formation_size` and `formation_shape` parameters to alter the formation's dimensions and shape.

## Visualization

Use RViz to visualize the robots and their trajectories:

```bash
roslaunch turtle_pentagon move_husky.launch
```

## References

- **Husky Packages**: Common ROS packages for the Clearpath Husky. 
- **Simulating Multiple Husky UGVs in Gazebo**: Guidelines on simulating multiple Husky robots. 


## Acknowledgments

This package builds upon the work of the ROS and Clearpath Robotics communities.

For more information, visit the [Husky GitHub repository](https://github.com/husky/husky). 
