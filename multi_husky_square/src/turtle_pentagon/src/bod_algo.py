#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import heapq

class Node:
    def __init__(self, state):
        self.state = state
        self.g_value = float('inf')  # Initialize with infinity
        self.parent = None

    def __lt__(self, other):
        # Comparison based on g_value
        return self.g_value < other.g_value

def bod_algorithm():
    # Initialize the ROS node
    rospy.init_node('bod_algorithm', anonymous=True)
    
    # Create a publisher to control the Husky
    pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)

    # Example graph: {state: [(cost, neighbor_state), ...]}
    graph = {
        'A': [(1, 'B'), (4, 'C')],
        'B': [(2, 'C'), (5, 'D')],
        'C': [(1, 'D')],
        'D': []
    }

    # Set the start and goal states
    start_state = 'A'
    goal_state = 'D'

    # Initialize the Open list
    open_list = []
    start_node = Node(start_state)
    start_node.g_value = 0
    heapq.heappush(open_list, start_node)

    # Initialize solutions
    sols = {}

    while open_list:
        # Remove the node with the smallest g-value
        current_node = heapq.heappop(open_list)

        # If the current node's state is already processed, skip it
        if current_node.state in sols:
            continue

        # Store the Pareto-optimal solution
        sols[current_node.state] = current_node.g_value

        # Check if we reached the goal
        if current_node.state == goal_state:
            rospy.loginfo(f"Reached goal state: {goal_state} with cost: {current_node.g_value}")
            break

        # Explore neighbors
        for cost, neighbor_state in graph.get(current_node.state, []):
            neighbor_node = Node(neighbor_state)
            new_g_value = current_node.g_value + cost
            
            if neighbor_state not in sols and new_g_value < neighbor_node.g_value:
                neighbor_node.g_value = new_g_value
                neighbor_node.parent = current_node
                heapq.heappush(open_list, neighbor_node)

        # Example movement command for the Husky based on the next state
        move_cmd = get_movement_cmd(current_node.state)
        pub.publish(move_cmd)

        rospy.sleep(1)  # Sleep to simulate time taken for movement

    # Stop the robot after reaching the goal
    stop_cmd = Twist()
    pub.publish(stop_cmd)

def get_movement_cmd(current_state):
    move_cmd = Twist()
    # Example logic for movement based on the current state
    if current_state == 'A':
        move_cmd.linear.x = 0.5  # Move forward from A
    elif current_state == 'B':
        move_cmd.linear.x = 0.4  # Adjust speed for B
    elif current_state == 'C':
        move_cmd.linear.x = 0.3  # Adjust speed for C
    # Add more conditions as needed for other states
    else:
        move_cmd.linear.x = 0.0  # Stop for other states or if no movement is required
    return move_cmd

if __name__ == '__main__':
    try:
        bod_algorithm()
    except rospy.ROSInterruptException:
        pass
