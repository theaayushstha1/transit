"""Station node in the transit network graph."""

from collections import deque


class Station:
    _next_id = 1

    def __init__(self, name: str, capacity: int, line: str):
        self.station_id = Station._next_id
        Station._next_id += 1
        self.name = name
        self.capacity = capacity
        self.line = line  # "light_rail", "metro", "both"
        self.passenger_queue = deque()

    def __repr__(self):
        return f"Station({self.station_id}: {self.name})"

    def __lt__(self, other):
        return self.capacity < other.capacity
