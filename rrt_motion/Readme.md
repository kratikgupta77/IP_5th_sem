# Motion Planning Algorithms Project

This project, developed as part of the IP 5th Semester coursework, implements several fundamental motion planning algorithms, including Rapidly-exploring Random Tree (RRT), Dijkstra's, and A* algorithms.

## Overview

Motion planning is a critical aspect of robotics, enabling autonomous navigation through complex environments. This project focuses on three prominent algorithms:

- **Rapidly-exploring Random Tree (RRT)**: A sampling-based algorithm effective in high-dimensional spaces, particularly for pathfinding in environments with obstacles.

- **Dijkstra's Algorithm**: A search-based algorithm that finds the shortest path in weighted graphs, ensuring optimality in terms of path cost.

- **A* Algorithm**: An extension of Dijkstra's algorithm that incorporates heuristics to guide the search, improving efficiency by prioritizing paths that appear to lead more directly to the goal.

## Features

- **Algorithm Implementations**: Provides implementations of RRT, Dijkstra's, and A* algorithms for motion planning.

- **Visualization**: Includes graphical representations to visualize the planning process and resulting paths for each algorithm.

- **Obstacle Handling**: Capable of planning paths in environments with static obstacles, demonstrating the strengths and limitations of each algorithm.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/kratikgupta77/IP_5th_sem.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd IP_5th_sem/rrt_motion
   ```

3. **Install dependencies**:

   Ensure you have Python installed. Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Set up the ROS environment**:

   ```bash
   source devel/setup.bash
   ```

2. **Set the TurtleBot3 model**:

   ```bash
   export TURTLEBOT3_MODEL=burger
   ```

3. **Launch the simulation environment**:

   ```bash
   roslaunch motion_planning turtlebot.launch
   ```

4. **Run the desired algorithm**:

   For example, to run the A* algorithm:

   ```bash
   rosrun motion_planning Astar.py
   ```

   Replace `Astar.py` with `Dijkstra.py` or `RRT.py` to run the respective algorithms.

## Project Structure

- `main.py`: Entry point for running the selected motion planning algorithm.

- `rrt.py`: Contains the implementation of the RRT algorithm.

- `dijkstra.py`: Contains the implementation of Dijkstra's algorithm.

- `astar.py`: Contains the implementation of the A* algorithm.

- `config.py`: Configuration file for setting parameters like start/goal positions, obstacles, and algorithm selection.

- `utils.py`: Utility functions supporting the main algorithms.


https://github.com/user-attachments/assets/aed44a8e-8ff7-4f35-ad6e-8f74ec742e9d
A* simulation:






## References

- **RRT Algorithm**: For a comprehensive understanding of RRTs, refer to Steven M. LaValle's work on Rapidly-exploring Random Trees.

- **Dijkstra's Algorithm**: For insights into Dijkstra's algorithm, see Edsger W. Dijkstra's original paper on graph theory.

- **A* Algorithm**: For details on the A* algorithm, consult the foundational paper by Peter E. Hart, Nils J. Nilsson, and Bertram Raphael.

## Acknowledgments

This project was developed as part of the IP 5th Semester coursework. Special thanks to the course instructors and peers for their support and guidance.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

For any questions or contributions, please feel free to open an issue or submit a pull request. 
