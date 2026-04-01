"""Merge Sort and Quick Sort implementations with comparison counting."""

import time
from models.station import Station


def merge_sort(
    stations: list[Station], key=lambda s: s.capacity
) -> tuple[list[Station], int, float]:
    """
    Merge Sort: stable, O(n log n) always, O(n) extra space.

    Returns:
        (sorted_list, comparison_count, elapsed_seconds)
    """
    comparisons = [0]  # mutable counter for nested scope

    def _merge_sort(arr: list) -> list:
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        return _merge(left, right)

    def _merge(left: list, right: list) -> list:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    start_time = time.perf_counter()
    sorted_list = _merge_sort(list(stations))
    elapsed = time.perf_counter() - start_time

    return (sorted_list, comparisons[0], elapsed)


def quick_sort(
    stations: list[Station], key=lambda s: s.capacity
) -> tuple[list[Station], int, float]:
    """
    Quick Sort: unstable, O(n log n) avg / O(n^2) worst, O(log n) stack space.

    Returns:
        (sorted_list, comparison_count, elapsed_seconds)
    """
    comparisons = [0]
    arr = list(stations)  # work on a copy

    def _quick_sort(lo: int, hi: int) -> None:
        if lo < hi:
            p = _partition(lo, hi)
            _quick_sort(lo, p - 1)
            _quick_sort(p + 1, hi)

    def _partition(lo: int, hi: int) -> int:
        pivot = key(arr[hi])
        i = lo - 1
        for j in range(lo, hi):
            comparisons[0] += 1
            if key(arr[j]) <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1

    start_time = time.perf_counter()
    if len(arr) > 1:
        _quick_sort(0, len(arr) - 1)
    elapsed = time.perf_counter() - start_time

    return (arr, comparisons[0], elapsed)
