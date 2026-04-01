"""Binary Search and Linear Search with comparison counting."""

import time
from models.station import Station


def binary_search(
    sorted_stations: list[Station], target_capacity: int
) -> tuple[int, int, float]:
    """
    Binary Search on a sorted list of stations by capacity.
    Requires the list to be pre-sorted by capacity.

    Returns:
        (index_or_-1, comparison_count, elapsed_seconds)
    """
    comparisons = 0
    lo, hi = 0, len(sorted_stations) - 1

    start_time = time.perf_counter()

    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1

        if sorted_stations[mid].capacity == target_capacity:
            elapsed = time.perf_counter() - start_time
            return (mid, comparisons, elapsed)
        elif sorted_stations[mid].capacity < target_capacity:
            lo = mid + 1
        else:
            hi = mid - 1

    elapsed = time.perf_counter() - start_time
    return (-1, comparisons, elapsed)


def linear_search(
    stations: list[Station], target_capacity: int
) -> tuple[int, int, float]:
    """
    Linear Search through stations by capacity.

    Returns:
        (index_or_-1, comparison_count, elapsed_seconds)
    """
    comparisons = 0

    start_time = time.perf_counter()

    for i, station in enumerate(stations):
        comparisons += 1
        if station.capacity == target_capacity:
            elapsed = time.perf_counter() - start_time
            return (i, comparisons, elapsed)

    elapsed = time.perf_counter() - start_time
    return (-1, comparisons, elapsed)
