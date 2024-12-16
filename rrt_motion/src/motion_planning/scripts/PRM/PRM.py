#!/usr/bin/env python3

import rospy
import yaml
import math
import random
import numpy as np
from yaml.loader import SafeLoader
from geometry_msgs.msg import Point, Twist
from motion_planning.msg import motion_planning
from utils.make_graph import Visualize
from utils.graph import Graph, get_grid_size
from utils.Nodes import Node
from utils.heuristic import manhattan_heuristic, euclidean_heuristic
from utils.non_holonomic import NonHolonomicDrive

class PRM:
    def __init__(self, start, goal, graph, RPM, orientation_res, num_samples=500, k_nearest=10):
        self.start = start
        self.goal = goal
        self.graph = graph
        self.num_samples = num_samples
        self.k_nearest = k_nearest
        self.goal_sample_rate = 0.05  # Probability of sampling goal
        self.orienatation_res = orientation_res
        self.drive = NonHolonomicDrive(RPM, graph.grid_size)
        self.orientation = {(360 // orientation_res) * i: i for i in range(orientation_res)}

    def plan(self):
        '''
        Performs the PRM algorithm by building a roadmap and searching for a path.

        Returns:
        - Path found (list of nodes)
        '''
        roadmap = self.build_roadmap()
        
        # Search for the shortest path from start to goal using the roadmap
        path = self.search_path(roadmap)
        
        if path:
            return self.extract_path(path)
        else:
            rospy.loginfo("No valid path found.")
            return None

    def build_roadmap(self):
        '''
        Builds the PRM roadmap by randomly sampling nodes and connecting them to the k-nearest neighbors.
        '''
        sampled_nodes = []

        # Sampling nodes randomly
        for _ in range(self.num_samples):
            sample = self.sample()
            if sample and not self.graph.checkObstacleSpace(sample):
                sampled_nodes.append(sample)

        # Connecting the nodes
        roadmap = {node: [] for node in sampled_nodes}

        for i, node in enumerate(sampled_nodes):
            neighbors = self.get_k_nearest_neighbors(node, sampled_nodes[:i] + sampled_nodes[i+1:])
            for neighbor in neighbors:
                if self.is_collision_free(node, neighbor):
                    roadmap[node].append(neighbor)

        return roadmap

    def sample(self):
        '''
        Randomly samples a node, with a bias towards the goal.
        '''
        if np.random.random() > self.goal_sample_rate:
            return self.graph.generate_random_node()
        return self.goal

    def get_k_nearest_neighbors(self, node, sampled_nodes):
        '''
        Finds the k-nearest neighbors of a node.
        '''
        distances = [euclidean_heuristic(node, n) for n in sampled_nodes]
        nearest_neighbors = np.argsort(distances)[:self.k_nearest]
        return [sampled_nodes[i] for i in nearest_neighbors]

    def is_collision_free(self, node1, node2):
        '''
        Checks if the path between two nodes is collision-free.
        '''
        return not self.graph.checkObstacleSpace(node1) and not self.graph.checkObstacleSpace(node2)

    def search_path(self, roadmap):
        '''
        Searches for a path from the start node to the goal node using graph search.
        '''
        # Use a simple Dijkstra search algorithm to find the shortest path
        open_list = [(0, self.start)]
        came_from = {self.start: None}
        g_score = {self.start: 0}
        
        while open_list:
            current = min(open_list, key=lambda x: x[0])[1]
            open_list.remove((g_score[current], current))
            
            if current == self.goal:
                break

            for neighbor in roadmap[current]:
                tentative_g_score = g_score[current] + euclidean_heuristic(current, neighbor)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    came_from[neighbor] = current
                    open_list.append((g_score[neighbor], neighbor))

        # Reconstruct the path from goal to start
        path = []
        current = self.goal
        while current != self.start:
            path.append(current)
            current = came_from[current]
        path.append(self.start)

        return path

    def extract_path(self, path_nodes):
        '''
        Extracts the path by going through the parent nodes and returning it in the right order.
        '''
        extracted_path = []
        for node in path_nodes:
            extracted_path.append({
                "vertex": node,
                "twist": None,  # No twists needed in PRM (for non-holonomic robots, this may be adjusted)
                "intermediate_nodes": []  # No intermediate nodes for PRM in this case
            })
        return extracted_path

if __name__ == "__main__":
    rospy.init_node("PRM")
    mp_pub = rospy.Publisher("/motion_planning_results", motion_planning, queue_size=10)

    # Getting all the parameters from the server
    obstacles_file = rospy.get_param("obstacles_file")
    start_node = rospy.get_param("robot_pose")
    goal_pose = rospy.get_param("goal_position")
    RPM_val = rospy.get_param("RRM")
    orientation_pr = int(rospy.get_param("orientation_pr"))
    grid_pr = float(rospy.get_param("grid_pr"))

    with open(obstacles_file) as f:
        obs_locations = yaml.load(f, Loader=SafeLoader)

    grid_size = get_grid_size(obs_locations)
    rospy.loginfo(f"The grid_x_min : {grid_size[0][0]} and grid_x_max : {grid_size[0][1]}")
    graph = Graph(grid_size, obs_locations, 20, 35)

    orientation_res = 360 // orientation_pr
    grid_res = [int(abs(grid_size[0][0] - grid_size[0][1]) / grid_pr + 1), int(abs(grid_size[1][0] - grid_size[1][1]) / grid_pr + 1)]

    start_node = [float(x) for x in start_node[1:-1].split(" ")]
    start = Node(*(x for x in start_node))
    start.x = start.x * 100
    start.y = start.y * 100
    goal_node = [float(x) for x in goal_pose[1:-1].split(" ")]
    goal = Node(*(x for x in goal_node))

    if graph.checkObstacleSpace(start) or graph.checkObstacleSpace(goal):
        rospy.logerr("The start or goal nodes are beyond the grid dimensions")

    RPM = [float(x) for x in RPM_val[1:-1].split(" ")]
    algorithm = PRM(start, goal, graph, RPM, orientation_res)
    shortest_path = algorithm.plan()

    mp_data = motion_planning()
    for i in shortest_path[1:]:
        path_pt = Point()
        path_pt.x = i["vertex"].x
        path_pt.y = i["vertex"].y
        path_pt.z = 0
        mp_data.path.append(path_pt)

        mp_data.orientation.append(i["vertex"].theta)

        twist_pt = Twist()
        twist_pt.angular.z = i["twist"][0]
        twist_pt.linear.x = i["twist"][1]

        mp_data.turtlebot_twist.append(twist_pt)

    mp_pub.publish(mp_data)

    plot_result = Visualize(start, goal, obs_locations, RPM, grid_size)
    plot_result.animate("PRM", shortest_path)

    for i in shortest_path:
        rospy.loginfo(f"The x coordinate : {i['vertex'].x} and y coordinate : {i['vertex'].y} and orientation : {i['vertex'].theta}")

