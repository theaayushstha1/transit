"""Passenger waiting at a station."""


class Passenger:
    _next_id = 1

    def __init__(self, name: str, origin_id: int, destination_id: int):
        self.passenger_id = Passenger._next_id
        Passenger._next_id += 1
        self.name = name
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.boarded = False

    def __repr__(self):
        return f"Passenger({self.passenger_id}: {self.name})"
