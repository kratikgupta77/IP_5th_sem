# IP_5th_sem
Projects made using robotic operating system (ROS)

## how to run this repo on your system
1. Create a directory and run ```catkin_make ```
2. In the src directory clone any folder from this repo .this is the Package folder.
3. Run ```roscore``` in a separate terminal .(this is your master node of ROS.
4. Do ```source ~/direc_name/devel/setup.bash```
5. Run any source code node ```rosrun your_package_name your_node_name```

## turtle_sim projects 
This repository contains Python scripts using the Turtlesim library in ROS to demonstrate various robot motion and interaction tasks. The  ```2_turtle_collision_avoid.py ``` script spawns two turtles on the same simulation screen and implements collision avoidance by monitoring their Euclidean distance, stopping movement when they come too close. The move_turtle_pentagon.py and  ```move_turtle_square.py ``` scripts move a single turtle in the shapes of a pentagon and square, respectively, by calculating linear and angular velocities for precise control. The ``` spawn.py ``` script allows dynamic creation of turtles at specified positions using the  ```/spawn ``` service in ROS. Together, these scripts provide a practical understanding of robot motion, multi-turtle spawning, and simple collision avoidance logic in a simulated environment.
## robot_pkg
this project is a simple distribution of 1 publishing node generating numbers from 1 to 1000 and a subscriber node for that same topic .This is visualised using ```rqt_graph``` command.
## multi_husky_square
this makes the husky robot in Gazebo move in a square.
## algo_sim_rviz
This project, Global Path Planning for ROS, implements and visualizes global path planning algorithms for robot navigation in simulated environments. Supporting algorithms like A*, Dijkstra, PRM, and Weighted A*, the project offers flexible selection and modular design for autonomous navigation in obstacle and non-obstacle scenarios. The structure includes ROS launch files, parameter configurations, RViz visualizations, and Python scripts for algorithmic implementations. The core path_planning_server.py script functions as a ROS service server, handling path-planning requests, processing costmaps with start/goal indices, and visualizing results in RViz. Integration with TurtleBot3 allows for testing and simulation in both Gazebo and RViz environments. To run the project, users build the workspace using catkin_make, launch the simulation world, and execute the server script, ensuring smooth visualization and navigation of planned paths.
