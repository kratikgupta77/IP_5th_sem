import rospy
import random
from math import sqrt
from algorithms.neighbors import find_neighbors, calculate_step_cost

def euclidean_distance(index1, index2, width):
    """Calculates Euclidean distance between two points."""
    x1, y1 = index1 % width, index1 // width
    x2, y2 = index2 % width, index2 // width
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)
def prm(start_index, goal_index, width, height, costmap, resolution, origin, grid_viz, num_samples=500, connection_radius=10):
    """Performs Probabilistic Road Map (PRM) algorithm with RViz visualization."""
    roadmap = {}
    nodes = []

    lethal_cost = 150

    # Sampling phase: Generate random nodes in free space
    rospy.loginfo(f"PRM: Generating {num_samples} samples in free space...")
    for _ in range(num_samples):
        random_index = random.randint(0, width * height - 1)
        if costmap[random_index] < lethal_cost:  # Node is in free space
            nodes.append(random_index)
            roadmap[random_index] = []
            grid_viz.set_color(random_index, "blue")  # Highlight sampled point in RViz
        else:
            rospy.logdebug(f"Skipped node {random_index} due to obstacle.")

    # Connecting phase: Connect nodes within a certain radius
    rospy.loginfo("PRM: Connecting nodes...")
    for node in nodes:
        for neighbor_index, step_cost in find_neighbors(node, width, height, costmap, orthogonal_cost=1):
            if neighbor_index != node and euclidean_distance(node, neighbor_index, width) <= connection_radius:
                if calculate_step_cost(neighbor_index, costmap, 1, lethal_cost) != float('inf'):
                    roadmap[node].append(neighbor_index)
                    # Visualize connection in RViz
                    grid_viz.draw_line(node, neighbor_index, "green")

    # Add start and goal nodes to the roadmap
    rospy.loginfo("PRM: Adding start and goal nodes to roadmap...")
    roadmap[start_index] = []
    roadmap[goal_index] = []
    for node in nodes:
        if euclidean_distance(start_index, node, width) <= connection_radius:
            if calculate_step_cost(node, costmap, 1, lethal_cost) != float('inf'):
                roadmap[start_index].append(node)
                grid_viz.draw_line(start_index, node, "cyan")  # Visualize start connections

        if euclidean_distance(goal_index, node, width) <= connection_radius:
            if calculate_step_cost(node, costmap, 1, lethal_cost) != float('inf'):
                roadmap[goal_index].append(node)
                grid_viz.draw_line(goal_index, node, "magenta")  # Visualize goal connections

    # Query phase: Use A* or Dijkstra's algorithm on the roadmap
    rospy.loginfo("PRM: Querying roadmap for path...")
    path = query_roadmap(roadmap, start_index, goal_index, width, grid_viz)

    # Visualize the final path
    if path:
        rospy.loginfo('PRM: Path found! Highlighting path...')
        for i in range(len(path) - 1):
            grid_viz.draw_line(path[i], path[i + 1], "red")  # Highlight path in RViz
    else:
        rospy.logwarn('PRM: No path found! Check sampling density or connection radius.')

    return path, None
def query_roadmap(roadmap, start_index, goal_index, width, grid_viz):
    """Finds a path in the roadmap using A* search."""
    open_list = [[start_index, 0]]
    closed_list = set()
    parents, g_costs = {}, {}

    g_costs[start_index] = 0

    while open_list:
        current_node = min(open_list, key=lambda x: x[1])[0]
        open_list = [n for n in open_list if n[0] != current_node]

        if current_node == goal_index:
            return reconstruct_path(parents, start_index, goal_index)

        closed_list.add(current_node)
        grid_viz.set_color(current_node, "pale yellow")

        for neighbor in roadmap[current_node]:
            if neighbor in closed_list:
                continue

            g_cost = g_costs[current_node] + euclidean_distance(current_node, neighbor, width)

            if neighbor not in [n[0] for n in open_list] or g_cost < g_costs.get(neighbor, float('inf')):
                g_costs[neighbor] = g_cost
                parents[neighbor] = current_node
                open_list.append([neighbor, g_cost])
                grid_viz.set_color(neighbor, 'orange')

    rospy.logwarn("PRM: Failed to find a path in the roadmap.")
    return None

def reconstruct_path(parents, start_index, goal_index):
    """Reconstructs the shortest path from start to goal."""
    path = []
    node = goal_index
    while node != start_index:
        path.append(node)
        node = parents[node]
    path.append(start_index)
    return path[::-1]


