#! /usr/bin/env python

import rospy
from algorithms.neighbors import find_neighbors

def dijkstra(start_index, goal_index, width, height, costmap, resolution, origin, grid_viz, previous_plan_variables):
    """Performs Dijkstra's shortest path algorithm on a costmap."""

    open_list = [[start_index, 0]]
    closed_list = set()
    parents = {}
    g_costs = {start_index: 0}
    path_found = False
    rospy.loginfo('Dijkstra: Initialization complete')

    while open_list:
        open_list.sort(key=lambda x: x[1])
        current_node = open_list.pop(0)[0]

        if current_node in closed_list:
            continue

        closed_list.add(current_node)
        grid_viz.set_color(current_node, "pale yellow")

        if current_node == goal_index:
            path_found = True
            break

        for neighbor_index, step_cost in find_neighbors(current_node, width, height, costmap, resolution):
            if neighbor_index in closed_list:
                continue

            g_cost = g_costs[current_node] + step_cost
            if g_cost < g_costs.get(neighbor_index, float('inf')):
                g_costs[neighbor_index] = g_cost
                parents[neighbor_index] = current_node
                open_list.append([neighbor_index, g_cost])
                grid_viz.set_color(neighbor_index, 'orange')

    if not path_found:
        rospy.logwarn('Dijkstra: No path found!')
        return [], None

    shortest_path = []
    node = goal_index
    while node != start_index:
        shortest_path.append(node)
        node = parents[node]
    shortest_path.append(start_index)

    rospy.loginfo('Dijkstra: Path reconstruction complete')
    return shortest_path[::-1], None
