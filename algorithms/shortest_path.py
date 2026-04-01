"""Dijkstra's shortest path algorithm using heapq priority queue."""

import heapq
import time
from models.transit_network import TransitNetwork


def dijkstra(
    network: TransitNetwork, start_id: int, end_id: int
) -> tuple[list, float, dict, float]:
    """
    Dijkstra's algorithm for weighted shortest path.

    Uses heapq (min-heap) as the priority queue.

    Returns:
        (path, total_weight, all_distances, elapsed_seconds)
        - path: list of station IDs from start to end
        - total_weight: total travel time in minutes
        - all_distances: dict of shortest distance to every reachable station
        - elapsed: time taken in seconds
    """
    distances = {sid: float("inf") for sid in network.stations}
    distances[start_id] = 0
    previous: dict[int, int | None] = {sid: None for sid in network.stations}
    pq = [(0, start_id)]  # (distance, station_id)
    visited = set()

    start_time = time.perf_counter()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        if current == end_id:
            break

        for neighbor_id, weight in network.get_neighbors(current):
            if neighbor_id not in visited:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current
                    heapq.heappush(pq, (new_dist, neighbor_id))

    elapsed = time.perf_counter() - start_time

    # Reconstruct path
    path = []
    current = end_id
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    # If path doesn't start with start_id, no path exists
    if not path or path[0] != start_id:
        return ([], float("inf"), distances, elapsed)

    return (path, distances[end_id], distances, elapsed)
