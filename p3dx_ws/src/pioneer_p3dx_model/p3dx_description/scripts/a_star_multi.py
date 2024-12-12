#!/usr/bin/python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from math import sqrt, atan2, pi
import threading

class AStarPlanner:
    def __init__(self, start_position, goal_position):
        self.grid_size = 11
        self.start = start_position
        self.goal = goal_position
        self.maze_walls = self.get_maze_walls()
        self.path = self.a_star()

    def get_maze_walls(self):
        # Define the obstacles (walls) in the maze
        walls = {
            (2, 2), (2, 3), (3, 4), (4, 4), (5, 4), 
            (6, 4), (7, 4), (8, 4), (9, 4), (4, 2),
            (6, 2), (7, 2), (8, 2), (9, 2), (5, 7),
            (6, 7), (7, 7), (8, 7), (9, 7), (2, 8),
             (4, 9)
        }
        return walls

    def a_star(self):
        # A* algorithm to find the path from start to goal
        open_list = [(self.start, [])]
        closed_list = set()

        while open_list:
            current_pos, path_so_far = open_list.pop(0)
            if current_pos == self.goal:
                return path_so_far + [self.goal]

            closed_list.add(current_pos)
            x, y = current_pos
            neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

            for neighbor in neighbors:
                if neighbor not in closed_list and 0 <= neighbor[0] < self.grid_size and 0 <= neighbor[1] < self.grid_size and neighbor not in self.maze_walls:
                    open_list.append((neighbor, path_so_far + [current_pos]))

        return []  # Return empty if no path is found


def euler_from_quaternion(x, y, z, w):
    import math
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (w * y - z * x)
    pitch = math.asin(sinp) if abs(sinp) <= 1 else math.copysign(math.pi / 2, sinp)

    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


class RobotController:
    def __init__(self, robot_name, start_position, goal_position, following_robot=None):
        self.robot_name = robot_name
        self.current_position = start_position
        self.current_angle = 0
        self.following_robot = following_robot  # The robot that this robot will follow (if any)
        
        # Robot 1 calculates its own A* path; others follow it
        self.path = []  
        if not following_robot:
            self.planner = AStarPlanner(start_position, goal_position)
            self.path = self.planner.path
        
        # Use robot-specific topics
        self.velocity_publisher = rospy.Publisher(f'/{robot_name}/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber(f'/{robot_name}/odom', Odometry, self.odom_callback)

    def odom_callback(self, msg):
        x = round(msg.pose.pose.position.x / 0.5) * 0.5
        y = round(msg.pose.pose.position.y / 0.5) * 0.5
        self.current_position = (int(x), int(y))

        orientation = msg.pose.pose.orientation
        _, _, self.current_angle = euler_from_quaternion(
            orientation.x, orientation.y, orientation.z, orientation.w
        )

    def move_to_goal(self, rate):
        if not self.path and self.following_robot:
            self.path = self.following_robot.path  # Follow the preceding robot's path

        for target in self.path:
            target_x, target_y = target
            rospy.loginfo(f"{self.robot_name}: Moving to: {target}")

            while not rospy.is_shutdown():
                dx = target_x - self.current_position[0]
                dy = target_y - self.current_position[1]
                distance = sqrt(dx**2 + dy**2)
                angle_to_target = atan2(dy, dx)
                angle_diff = (angle_to_target - self.current_angle + pi) % (2 * pi) - pi

                vel_msg = Twist()

                # Scale speed based on the robot's position in the chain
                if self.robot_name == "robot1":
                    vel_msg.linear.x = min(0.35, distance)  # Robot 1 moves at normal speed
                elif self.robot_name == "robot2":
                    vel_msg.linear.x = min(0.28, distance)  # Robot 2 moves slower than Robot 1
                elif self.robot_name == "robot3":
                    vel_msg.linear.x = min(0.22, distance)  # Robot 3 moves slower than Robot 2
                elif self.robot_name == "robot4":
                    vel_msg.linear.x = min(0.19, distance)  # Robot 4 moves slower than Robot 3

                vel_msg.angular.z = 2.0 * angle_diff

                if distance < 0.1:
                    vel_msg.linear.x = 0.0
                    vel_msg.angular.z = 0.0
                    self.velocity_publisher.publish(vel_msg)
                    rospy.loginfo(f"{self.robot_name}: Reached position: {target}")
                    break

                self.velocity_publisher.publish(vel_msg)
                rate.sleep()


def move_robot_thread(robot, rate):
    robot.move_to_goal(rate)


def move_robots():
    rospy.init_node('multi_robot_a_star', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    # Define start and goal positions for each robot
    robot1 = RobotController("robot1", (0, 0), (5, 9))  # Robot 1 with its own A* path
    robot2 = RobotController("robot2", (0.5, 0), (5, 8.5), following_robot=robot1)  # Robot 2 follows Robot 1
    robot3 = RobotController("robot3", (1, 0), (5, 8), following_robot=robot2)    # Robot 3 follows Robot 2
    robot4 = RobotController("robot4", (1.5, 0), (5, 7.5), following_robot=robot3)  # Robot 4 follows Robot 3

    # Start moving robots simultaneously using threads
    threads = []
    threads.append(threading.Thread(target=move_robot_thread, args=(robot1, rate)))
    threads.append(threading.Thread(target=move_robot_thread, args=(robot2, rate)))
    threads.append(threading.Thread(target=move_robot_thread, args=(robot3, rate)))
    threads.append(threading.Thread(target=move_robot_thread, args=(robot4, rate)))

    # Start threads
    for thread in threads:
        thread.start()

    # Join all threads
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    try:
        move_robots()
    except rospy.ROSInterruptException:
        pass

