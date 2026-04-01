"""Queue-based passenger boarding simulation."""

import random
from collections import deque
from models.passenger import Passenger
from models.transit_network import TransitNetwork


class PassengerSimulation:
    """
    Simulates passengers waiting at stations (queue/FIFO) and boarding trains.
    Demonstrates the Queue data structure.
    """

    def __init__(self, network: TransitNetwork):
        self.network = network

    def generate_passengers(self, station_id: int, count: int) -> list[Passenger]:
        """
        Create random passengers and add them to the station's queue.
        Each passenger has a random destination.
        """
        station = self.network.stations[station_id]
        other_ids = [sid for sid in self.network.stations if sid != station_id]
        generated = []

        for i in range(count):
            dest_id = random.choice(other_ids)
            dest_name = self.network.stations[dest_id].name
            passenger = Passenger(
                name=f"P-{station.name[:3]}-{i + 1}",
                origin_id=station_id,
                destination_id=dest_id,
            )
            station.passenger_queue.append(passenger)  # enqueue (FIFO)
            generated.append(passenger)

        return generated

    def board_passengers(
        self, station_id: int, train_capacity: int
    ) -> tuple[list[Passenger], int]:
        """
        Board passengers from the station queue onto a train (FIFO order).

        Returns:
            (boarded_passengers, remaining_in_queue)
        """
        station = self.network.stations[station_id]
        boarded = []

        while station.passenger_queue and len(boarded) < train_capacity:
            passenger = station.passenger_queue.popleft()  # dequeue (FIFO)
            passenger.boarded = True
            boarded.append(passenger)

        return (boarded, len(station.passenger_queue))

    def get_queue_size(self, station_id: int) -> int:
        """How many passengers are waiting at a station."""
        return len(self.network.stations[station_id].passenger_queue)

    def clear_queue(self, station_id: int) -> None:
        """Clear all passengers from a station's queue."""
        self.network.stations[station_id].passenger_queue.clear()
