import rospy
from math import sqrt
from algorithms.neighbors import find_neighbors
w=1
def euclidean_distance(index, goal_index, width):
    """Calculates Euclidean distance as the heuristic."""
    x1, y1 = index % width, index // width
    x2, y2 = goal_index % width, goal_index // width
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def wt_astar(start_index, goal_index, width, height, costmap, resolution, origin, grid_viz, previous_plan_variables):
    """Performs A* algorithm to find the shortest path."""
    open_list = [[start_index, 0]]
    closed_list = set()
    parents, g_costs, f_costs = {}, {}, {}

    g_costs[start_index] = 0
    f_costs[start_index] = euclidean_distance(start_index, goal_index, width)

    path_found = False
    rospy.loginfo('Weighted_AStar: Initialization complete')

    while open_list:
        # Pop the node with the lowest f_cost
        current_node = min(open_list, key=lambda x: x[1])[0]
        open_list = [n for n in open_list if n[0] != current_node]

        if current_node == goal_index:
            path_found = True
            break

        closed_list.add(current_node)
        grid_viz.set_color(current_node, "pale yellow")

        for neighbor_index, step_cost in find_neighbors(current_node, width, height, costmap, resolution):
            if neighbor_index in closed_list:
                continue

            g_cost = g_costs[current_node] + step_cost
            h_cost = euclidean_distance(neighbor_index, goal_index, width)
            f_cost = g_cost + h_cost*w

            if neighbor_index not in [n[0] for n in open_list] or f_cost < f_costs.get(neighbor_index, float('inf')):
                g_costs[neighbor_index] = g_cost
                f_costs[neighbor_index] = f_cost
                parents[neighbor_index] = current_node
                open_list.append([neighbor_index, f_cost])
                grid_viz.set_color(neighbor_index, 'orange')

    if not path_found:
        rospy.logwarn('AStar: No path found!')
        return [], None

    # Reconstruct path
    shortest_path = []
    node = goal_index
    while node != start_index:
        shortest_path.append(node)
        node = parents[node]
    shortest_path.append(start_index)

    rospy.loginfo('AStar: Path reconstruction complete')
    return shortest_path[::-1], None
