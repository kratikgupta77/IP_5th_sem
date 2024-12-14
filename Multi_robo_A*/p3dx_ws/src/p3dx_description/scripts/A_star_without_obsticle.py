#!/usr/bin/python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, PoseArray, PoseStamped
from math import sqrt, atan2, pi
import threading
import math
from heapq import heappush, heappop


def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into Euler angles (roll, pitch, yaw).
    """
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (w * y - z * x)
    pitch = math.asin(sinp) if abs(sinp) <= 1 else math.copysign(math.pi / 2, sinp)

    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


class AStarPlanner:
    def __init__(self, start_position, goal_position, grid_size=25, resolution=0.5):
        """
        Initialize the A* planner.

        :param start_position: Tuple (x, y) in world coordinates.
        :param goal_position: Tuple (x, y) in world coordinates.
        :param grid_size: Number of cells in each dimension.
        :param resolution: Size of each grid cell in meters.
        """
        self.grid_size = grid_size
        self.resolution = resolution  # Size of each grid cell in meters
        self.start = self.world_to_grid(start_position)
        self.goal = self.world_to_grid(goal_position)
        self.maze_walls = self.get_maze_walls()
        self.path = self.a_star()

    def world_to_grid(self, position):
        """
        Convert world coordinates to grid coordinates.

        :param position: Tuple (x, y) in meters.
        :return: Tuple (grid_x, grid_y)
        """
        x, y = position
        grid_x = int(round(x / self.resolution))
        grid_y = int(round(y / self.resolution))
        rospy.logdebug(f"Converted world position {position} to grid position ({grid_x}, {grid_y})")
        return (grid_x, grid_y)

    def grid_to_world(self, grid_pos):
        """
        Convert grid coordinates back to world coordinates.

        :param grid_pos: Tuple (grid_x, grid_y)
        :return: Tuple (x, y) in meters.
        """
        x, y = grid_pos
        world_x = x * self.resolution
        world_y = y * self.resolution
        return (world_x, world_y)

    def get_maze_walls(self):
        """
        Define the static obstacles (walls) in the maze.
        Adjust these coordinates to match your Gazebo environment.
        """
        walls = {
            (2, 2), (2, 3), (3, 4), (4, 4), (5, 4),
            (6, 4), (7, 4), (8, 4), (9, 4), (4, 2),
            (6, 2), (7, 2), (8, 2), (9, 2), (5, 7),
            (6, 7), (7, 7), (8, 7), (9, 7), (2, 8),
            (4, 9)
        }
        rospy.logdebug(f"Predefined maze walls: {walls}")
        return walls

    def heuristic(self, a, b):
        """
        Heuristic function for A* (Manhattan distance).

        :param a: Tuple (x, y)
        :param b: Tuple (x, y)
        :return: Heuristic cost.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        """
        Get walkable neighbor nodes (8-connected grid).

        :param node: Tuple (x, y)
        :return: List of neighbor tuples.
        """
        x, y = node
        neighbors = [
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1),
            (x - 1, y - 1), (x - 1, y + 1),
            (x + 1, y - 1), (x + 1, y + 1)
        ]
        # Ensure neighbors are within grid bounds
        valid_neighbors = [
            (nx, ny) for nx, ny in neighbors
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size
        ]
        return valid_neighbors

    def a_star(self):
        """
        Perform the A* search algorithm to find the path from start to goal.

        :return: List of waypoints [(x1, y1), (x2, y2), ...] in world coordinates.
        """
        open_list = []
        heappush(open_list, (0 + self.heuristic(self.start, self.goal), 0, self.start, []))
        closed_set = set()

        while open_list:
            _, cost, current, path_so_far = heappop(open_list)

            if current in closed_set:
                continue

            path_so_far = path_so_far + [current]

            if current == self.goal:
                # Convert grid path back to world coordinates
                world_path = [self.grid_to_world(p) for p in path_so_far]
                rospy.loginfo(f"A* Planner: Path found with {len(world_path)} waypoints.")
                return world_path

            closed_set.add(current)
            neighbors = self.get_neighbors(current)

            for neighbor in neighbors:
                if neighbor in closed_set or neighbor in self.maze_walls:
                    continue
                new_cost = cost + sqrt((neighbor[0] - current[0])**2 + (neighbor[1] - current[1])**2)  # Euclidean distance
                heappush(open_list, (new_cost + self.heuristic(neighbor, self.goal), new_cost, neighbor, path_so_far))

        rospy.logwarn("A* Planner: No path found!")
        return []  # Return empty if no path is found


class RobotController:
    def __init__(self, robot_name, start_position, goal_position, following_robot=None, robot_radius=0.2):
        """
        Initialize the robot controller.

        :param robot_name: Name of the robot (e.g., "robot1").
        :param start_position: Tuple (x, y) in meters.
        :param goal_position: Tuple (x, y) in meters.
        :param following_robot: Instance of RobotController to follow.
        :param robot_radius: Radius of the robot in meters.
        """
        self.robot_name = robot_name
        self.current_position = start_position
        self.current_angle = 0
        self.following_robot = following_robot  # The robot that this robot will follow (if any)
        self.robot_radius = robot_radius  # For collision buffer
        self.finished = False  # Flag to indicate completion

        # Initialize A* planner if this robot is not following another
        if not following_robot:
            self.planner = AStarPlanner(start_position, goal_position)
            self.path = self.planner.path
        else:
            self.planner = None
            self.path = []

        # Publisher and Subscribers
        self.velocity_publisher = rospy.Publisher(f'/{robot_name}/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber(f'/{robot_name}/odom', Odometry, self.odom_callback)

        # Lock for thread-safe operations
        self.lock = threading.Lock()

        # Path Publisher for visualization
        self.path_publisher = rospy.Publisher(f'/{robot_name}/planned_path', PoseArray, queue_size=10)

        # Retrieve speed parameters from ROS parameter server or set default values
        # These speeds are slightly increased from the previous values
        self.speeds = {
            "robot1": rospy.get_param(f'/{robot_name}/linear_speed', 0.45),  # Increased from 0.35 to 0.45
            "robot2": rospy.get_param(f'/{robot_name}/linear_speed', 0.35),  # Increased from 0.28 to 0.38
            "robot3": rospy.get_param(f'/{robot_name}/linear_speed', 0.27),  # Increased from 0.22 to 0.32
            "robot4": rospy.get_param(f'/{robot_name}/linear_speed', 0.21)   # Increased from 0.19 to 0.29
        }

    def odom_callback(self, msg):
        """
        Callback function for Odometry messages.

        :param msg: Odometry message.
        """
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.current_position = (x, y)

        orientation = msg.pose.pose.orientation
        _, _, self.current_angle = euler_from_quaternion(
            orientation.x, orientation.y, orientation.z, orientation.w
        )

    def publish_path(self):
        """
        Publish the planned path as a PoseArray for visualization.
        """
        pose_array = PoseArray()
        pose_array.header.frame_id = "map"
        pose_array.header.stamp = rospy.Time.now()
        for waypoint in self.path:
            pose = PoseStamped()
            pose.pose.position.x = waypoint[0]
            pose.pose.position.y = waypoint[1]
            pose.pose.position.z = 0
            pose.pose.orientation.w = 1.0  # No rotation
            pose_array.poses.append(pose.pose)
        self.path_publisher.publish(pose_array)

    def move_to_goal(self, rate):
        """
        Move the robot along the planned path.

        :param rate: ROS Rate object.
        """
        while not rospy.is_shutdown() and not self.finished:
            with self.lock:
                if not self.path and self.following_robot:
                    with self.following_robot.lock:
                        self.path = list(self.following_robot.path)  # Follow the preceding robot's path
                        rospy.loginfo(f"{self.robot_name}: Updated path from following {self.following_robot.robot_name}.")

            if not self.path:
                if not self.following_robot:
                    rospy.loginfo(f"{self.robot_name}: No path to follow.")
                rate.sleep()
                continue

            self.publish_path()  # Publish the current path for visualization

            for target in self.path:
                if rospy.is_shutdown() or self.finished:
                    break  # Exit if ROS is shutting down or robot is finished

                target_x, target_y = target
                rospy.loginfo(f"{self.robot_name}: Moving to: ({target_x}, {target_y})")

                while not rospy.is_shutdown() and not self.finished:
                    dx = target_x - self.current_position[0]
                    dy = target_y - self.current_position[1]
                    distance = sqrt(dx**2 + dy**2)
                    angle_to_target = atan2(dy, dx)
                    angle_diff = (angle_to_target - self.current_angle + pi) % (2 * pi) - pi

                    vel_msg = Twist()

                    # Retrieve speed from the speeds dictionary
                    vel_msg.linear.x = min(self.speeds.get(self.robot_name, 0.3), distance)  # Default speed 0.3 if not set
                    vel_msg.angular.z = 2.0 * angle_diff

                    # Publish velocity commands
                    self.velocity_publisher.publish(vel_msg)

                    if distance < 0.1:
                        vel_msg.linear.x = 0.0
                        vel_msg.angular.z = 0.0
                        self.velocity_publisher.publish(vel_msg)
                        rospy.loginfo(f"{self.robot_name}: Reached position: ({target_x}, {target_y})")
                        break

                    rate.sleep()

            # After reaching the current path, clear it and set finished flag if not following another robot
            with self.lock:
                if not self.following_robot:
                    self.path = []
                    self.finished = True  # Set the finished flag
                    rospy.loginfo(f"{self.robot_name}: Reached the goal successfully.")
                else:
                    # Continuously update the path based on the preceding robot's path
                    with self.following_robot.lock:
                        self.path = list(self.following_robot.path)
                        # If the preceding robot has finished, this robot has also finished
                        if self.following_robot.finished:
                            self.finished = True
                            rospy.loginfo(f"{self.robot_name}: Reached the goal successfully by following {self.following_robot.robot_name}.")
                            break

            rate.sleep()


def move_robot_thread(robot, rate):
    """
    Thread target function to move a robot.

    :param robot: Instance of RobotController.
    :param rate: ROS Rate object.
    """
    robot.move_to_goal(rate)


def move_robots():
    """
    Initialize and start movement threads for all robots.
    """
    rospy.init_node('multi_robot_a_star_static', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    # Define start and goal positions for each robot (in meters)
    robot1 = RobotController("robot1", (0.0, 0.0), (5.0, 9.0))     # Robot 1 with its own A* path
    robot2 = RobotController("robot2", (0.5, 0.0), (5.0, 8.5), following_robot=robot1)  # Robot 2 follows Robot 1
    robot3 = RobotController("robot3", (1.0, 0.0), (5.0, 8.0), following_robot=robot2)  # Robot 3 follows Robot 2
    robot4 = RobotController("robot4", (1.5, 0.0), (5.0, 7.5), following_robot=robot3)  # Robot 4 follows Robot 3

    robots = [robot1, robot2, robot3, robot4]

    # Start moving robots simultaneously using threads
    threads = []
    for robot in robots:
        threads.append(threading.Thread(target=move_robot_thread, args=(robot, rate)))

    # Start threads
    for thread in threads:
        thread.start()

    # Monitor the completion of all robots
    try:
        while not rospy.is_shutdown():
            all_finished = all(robot.finished for robot in robots)
            if all_finished:
                rospy.loginfo("All robots have reached their goals successfully.")
                rospy.signal_shutdown("All robots have reached their goals.")
                break
            rate.sleep()
    except rospy.ROSInterruptException:
        pass

    # Ensure all threads have finished
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    try:
        move_robots()
    except rospy.ROSInterruptException:
        pass
