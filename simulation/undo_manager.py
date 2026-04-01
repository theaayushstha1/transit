"""Stack-based undo system for graph operations."""

from models.transit_network import TransitNetwork


class UndoManager:
    """
    Uses the network's undo_stack (a Python list used as a stack via append/pop).
    Each graph mutation pushes its inverse action.
    Undo pops the last action and applies the inverse using _raw_* methods.
    """

    def __init__(self, network: TransitNetwork):
        self.network = network

    def can_undo(self) -> bool:
        return len(self.network.undo_stack) > 0

    def undo(self) -> str:
        """
        Pop the last action from the stack and reverse it.
        Returns a description of what was undone.
        """
        if not self.network.undo_stack:
            return "Nothing to undo"

        action = self.network.undo_stack.pop()
        action_type = action["action"]

        if action_type == "add_station":
            # Reverse of adding = remove
            station = action["station"]
            self.network._raw_remove_station(station.station_id)
            return f"Undid: added station '{station.name}'"

        elif action_type == "remove_station":
            # Reverse of removing = re-add station and all its connections
            station = action["station"]
            self.network._raw_add_station(station)
            for id1, id2, weight in action["connections"]:
                self.network._raw_add_connection(id1, id2, weight)
            return f"Undid: removed station '{station.name}'"

        elif action_type == "add_connection":
            # Reverse of adding connection = remove it
            self.network._raw_remove_connection(action["id1"], action["id2"])
            s1 = self.network.stations.get(action["id1"])
            s2 = self.network.stations.get(action["id2"])
            n1 = s1.name if s1 else str(action["id1"])
            n2 = s2.name if s2 else str(action["id2"])
            return f"Undid: added connection '{n1}' <-> '{n2}'"

        elif action_type == "remove_connection":
            # Reverse of removing connection = add it back
            self.network._raw_add_connection(
                action["id1"], action["id2"], action["weight"]
            )
            s1 = self.network.stations.get(action["id1"])
            s2 = self.network.stations.get(action["id2"])
            n1 = s1.name if s1 else str(action["id1"])
            n2 = s2.name if s2 else str(action["id2"])
            return f"Undid: removed connection '{n1}' <-> '{n2}'"

        return "Unknown action"

    def history_count(self) -> int:
        return len(self.network.undo_stack)
