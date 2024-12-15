def calculate_step_cost(index, costmap, base_cost, lethal_cost):
    """Calculate the cost to step into a neighbor node."""
    return base_cost + costmap[index] / 255 if costmap[index] < lethal_cost else float('inf')


def get_neighbors(index, width, height, costmap, orthogonal_cost, lethal_cost, include_obstacles=False):
    """Find valid neighbors and their step costs for a given grid index."""
    directions = [
        (-width, orthogonal_cost),                         # Upper
        (-1, orthogonal_cost, lambda idx: idx % width > 0),  # Left
        (-width - 1, orthogonal_cost * 1.41421, lambda idx: idx % width > 0),  # Upper-left
        (-width + 1, orthogonal_cost * 1.41421, lambda idx: idx % width != width - 1),  # Upper-right
        (1, orthogonal_cost, lambda idx: idx % width != width - 1),  # Right
        (width - 1, orthogonal_cost * 1.41421, lambda idx: idx % width > 0),  # Lower-left
        (width, orthogonal_cost),                          # Lower
        (width + 1, orthogonal_cost * 1.41421, lambda idx: idx % width != width - 1)  # Lower-right
    ]

    neighbors = []
    for offset, base_cost, *conditions in directions:
        neighbor_index = index + offset
        if 0 <= neighbor_index < width * height and all(cond(neighbor_index) for cond in conditions if conditions):
            step_cost = calculate_step_cost(neighbor_index, costmap, base_cost, lethal_cost)
            if include_obstacles or step_cost != float('inf'):
                neighbors.append([neighbor_index, step_cost])
    return neighbors


def find_neighbors(index, width, height, costmap, orthogonal_cost):
    """Find neighbors, excluding obstacles."""
    lethal_cost = 150
    return get_neighbors(index, width, height, costmap, orthogonal_cost, lethal_cost, include_obstacles=False)


def find_weighted_neighbors(index, width, height, costmap, orthogonal_cost):
    """Find neighbors, including obstacles with infinite cost."""
    lethal_cost = 150
    return get_neighbors(index, width, height, costmap, orthogonal_cost, lethal_cost, include_obstacles=True)
