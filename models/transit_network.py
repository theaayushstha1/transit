"""Transit network graph using adjacency list representation."""

from .station import Station


class TransitNetwork:
    """
    Graph data structure for the transit system.

    Adjacency list: dict[int, dict[int, float]]
    stations[id] -> Station object
    adj_list[id] -> {neighbor_id: weight_in_minutes}

    Undirected graph: every connection is stored in both directions.
    """

    def __init__(self):
        self.stations: dict[int, Station] = {}
        self.adj_list: dict[int, dict[int, float]] = {}
        self.undo_stack: list = []  # managed by UndoManager

    # --- Public Graph Operations (push to undo stack) ---

    def add_station(self, station: Station) -> None:
        """Add a station node to the graph. O(1)."""
        self._raw_add_station(station)
        self.undo_stack.append({
            "action": "add_station",
            "station": station,
        })

    def remove_station(self, station_id: int) -> None:
        """Remove a station and all its connections. O(V + E)."""
        if station_id not in self.stations:
            raise ValueError(f"Station {station_id} not found")
        station = self.stations[station_id]
        connections = []
        for neighbor_id, weight in self.adj_list.get(station_id, {}).items():
            connections.append((station_id, neighbor_id, weight))
        self._raw_remove_station(station_id)
        self.undo_stack.append({
            "action": "remove_station",
            "station": station,
            "connections": connections,
        })

    def add_connection(self, id1: int, id2: int, weight: float) -> None:
        """Add a weighted undirected edge. O(1)."""
        self._raw_add_connection(id1, id2, weight)
        self.undo_stack.append({
            "action": "add_connection",
            "id1": id1, "id2": id2, "weight": weight,
        })

    def remove_connection(self, id1: int, id2: int) -> None:
        """Remove an edge between two stations. O(1)."""
        weight = self.adj_list.get(id1, {}).get(id2)
        if weight is None:
            raise ValueError(f"No connection between {id1} and {id2}")
        self._raw_remove_connection(id1, id2)
        self.undo_stack.append({
            "action": "remove_connection",
            "id1": id1, "id2": id2, "weight": weight,
        })

    def get_neighbors(self, station_id: int) -> list[tuple[int, float]]:
        """Return list of (neighbor_id, weight) for a station."""
        return list(self.adj_list.get(station_id, {}).items())

    def get_all_stations(self) -> list[Station]:
        """Return all stations sorted by ID."""
        return sorted(self.stations.values(), key=lambda s: s.station_id)

    def get_station_by_name(self, name: str) -> Station | None:
        """Find a station by name (case-insensitive)."""
        name_lower = name.lower()
        for station in self.stations.values():
            if station.name.lower() == name_lower:
                return station
        return None

    # --- Raw Operations (no undo push, used by undo manager) ---

    def _raw_add_station(self, station: Station) -> None:
        self.stations[station.station_id] = station
        if station.station_id not in self.adj_list:
            self.adj_list[station.station_id] = {}

    def _raw_remove_station(self, station_id: int) -> None:
        for neighbor_id in list(self.adj_list.get(station_id, {}).keys()):
            self.adj_list[neighbor_id].pop(station_id, None)
        self.adj_list.pop(station_id, None)
        self.stations.pop(station_id, None)

    def _raw_add_connection(self, id1: int, id2: int, weight: float) -> None:
        if id1 not in self.adj_list:
            self.adj_list[id1] = {}
        if id2 not in self.adj_list:
            self.adj_list[id2] = {}
        self.adj_list[id1][id2] = weight
        self.adj_list[id2][id1] = weight

    def _raw_remove_connection(self, id1: int, id2: int) -> None:
        self.adj_list.get(id1, {}).pop(id2, None)
        self.adj_list.get(id2, {}).pop(id1, None)

    # --- Info ---

    def station_count(self) -> int:
        return len(self.stations)

    def connection_count(self) -> int:
        total = sum(len(neighbors) for neighbors in self.adj_list.values())
        return total // 2  # undirected, each edge counted twice

    def __repr__(self):
        return f"TransitNetwork({self.station_count()} stations, {self.connection_count()} connections)"
