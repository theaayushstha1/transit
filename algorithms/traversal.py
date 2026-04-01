"""DFS (recursive) and BFS (queue-based) traversal algorithms."""

import time
from collections import deque
from models.transit_network import TransitNetwork


def dfs(network: TransitNetwork, start_id: int, goal_id: int) -> tuple[list, list, float]:
    """
    Depth-First Search using recursion.

    Returns:
        (path, visit_order, elapsed_seconds)
        - path: list of station IDs from start to goal (empty if not found)
        - visit_order: every node visited in order (for animation)
        - elapsed: time taken in seconds
    """
    visited = set()
    path = []
    visit_order = []

    def _dfs_helper(current: int) -> bool:
        visited.add(current)
        visit_order.append(current)
        path.append(current)

        if current == goal_id:
            return True

        for neighbor_id, _ in sorted(network.get_neighbors(current)):
            if neighbor_id not in visited:
                if _dfs_helper(neighbor_id):
                    return True

        path.pop()  # backtrack
        return False

    start_time = time.perf_counter()
    found = _dfs_helper(start_id)
    elapsed = time.perf_counter() - start_time

    return (list(path) if found else [], visit_order, elapsed)


def bfs(network: TransitNetwork, start_id: int, goal_id: int) -> tuple[list, list, float]:
    """
    Breadth-First Search using a queue (collections.deque).

    Returns:
        (path, visit_order, elapsed_seconds)
        - path: list of station IDs from start to goal (empty if not found)
        - visit_order: every node visited in order (for animation)
        - elapsed: time taken in seconds
    """
    visited = {start_id}
    queue = deque([(start_id, [start_id])])
    visit_order = []

    start_time = time.perf_counter()

    while queue:
        current, path = queue.popleft()
        visit_order.append(current)

        if current == goal_id:
            elapsed = time.perf_counter() - start_time
            return (path, visit_order, elapsed)

        for neighbor_id, _ in sorted(network.get_neighbors(current)):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    elapsed = time.perf_counter() - start_time
    return ([], visit_order, elapsed)
