"""
Baltimore MTA Transit Simulator
COSC 320 - Algorithm Design

Entry point: interactive menu wiring all components together.
"""

import sys
sys.path.insert(0, ".")

from rich.console import Console

from data.baltimore_mta import build_default_network
from models.station import Station
from ui.display import Display
from ui.visualizer import Visualizer
from algorithms.traversal import dfs, bfs
from algorithms.shortest_path import dijkstra
from algorithms.sorting import merge_sort, quick_sort
from algorithms.searching import binary_search, linear_search
from simulation.undo_manager import UndoManager
from simulation.passenger_sim import PassengerSimulation


def main():
    console = Console()
    display = Display(console)
    viz = Visualizer(console)

    # Load real Baltimore MTA data
    network = build_default_network()
    undo = UndoManager(network)
    sim = PassengerSimulation(network)

    console.print("\n[bold cyan]Loaded Baltimore MTA network:[/bold cyan] "
                  f"{network.station_count()} stations, "
                  f"{network.connection_count()} connections\n")

    while True:
        choice = display.show_menu()

        if choice == "1":
            # View Network Map
            display.show_network(network)

        elif choice == "2":
            # Manage Stations & Connections
            _manage_menu(console, display, network)

        elif choice == "3":
            # Find Route: DFS vs BFS
            console.print("\n[bold]Select START station:[/bold]")
            start = display.station_picker(network, "Start station")
            console.print("\n[bold]Select END station:[/bold]")
            end = display.station_picker(network, "End station")

            console.print("\n[cyan]Running DFS...[/cyan]")
            dfs_result = dfs(network, start, end)

            console.print("[cyan]Running BFS...[/cyan]\n")
            bfs_result = bfs(network, start, end)

            # Animate DFS
            console.print("[bold green]DFS Traversal Animation:[/bold green]")
            viz.animate_traversal(network, dfs_result[1], dfs_result[0], "DFS")

            # Animate BFS
            console.print("[bold yellow]BFS Traversal Animation:[/bold yellow]")
            viz.animate_traversal(network, bfs_result[1], bfs_result[0], "BFS")

            # Comparison
            viz.show_traversal_comparison(network, dfs_result, bfs_result)

        elif choice == "4":
            # Shortest Path: Dijkstra
            console.print("\n[bold]Select START station:[/bold]")
            start = display.station_picker(network, "Start station")
            console.print("\n[bold]Select END station:[/bold]")
            end = display.station_picker(network, "End station")

            path, total_time, distances, elapsed = dijkstra(network, start, end)
            display.show_dijkstra_result(network, path, total_time)
            console.print(f"  [dim]Dijkstra completed in {elapsed * 1_000_000:.2f} us[/dim]\n")

        elif choice == "5":
            # Passenger Boarding Simulation
            console.print("\n[bold]Select station for passenger simulation:[/bold]")
            station_id = display.station_picker(network, "Station")
            station = network.stations[station_id]

            try:
                count = int(input("  Number of passengers to generate: "))
                capacity = int(input("  Train capacity: "))
            except ValueError:
                console.print("[red]Invalid number.[/red]")
                continue

            # Generate passengers
            sim.generate_passengers(station_id, count)
            total_waiting = sim.get_queue_size(station_id)
            console.print(f"\n  Generated {count} passengers at {station.name}")

            # Board passengers
            boarded, remaining = sim.board_passengers(station_id, capacity)

            viz.show_boarding_animation(
                station.name, total_waiting, capacity, len(boarded), remaining
            )

        elif choice == "6":
            # Sort: Merge Sort vs Quick Sort
            stations = network.get_all_stations()
            console.print(f"\n[cyan]Sorting {len(stations)} stations by capacity...[/cyan]\n")

            merge_result = merge_sort(stations)
            quick_result = quick_sort(stations)

            display.show_sort_comparison(merge_result, quick_result, network)

        elif choice == "7":
            # Search: Binary vs Linear
            stations = network.get_all_stations()
            sorted_stations = merge_sort(stations)[0]  # sort first for binary search

            try:
                target = int(input("\n  Enter target capacity to search for: "))
            except ValueError:
                console.print("[red]Invalid number.[/red]")
                continue

            b_result = binary_search(sorted_stations, target)
            l_result = linear_search(sorted_stations, target)

            display.show_search_comparison(target, b_result, l_result, sorted_stations)

        elif choice == "8":
            # Performance Dashboard
            display.show_performance_dashboard(network)

        elif choice == "9":
            # Undo Last Action
            if undo.can_undo():
                msg = undo.undo()
                console.print(f"\n  [yellow]{msg}[/yellow]\n")
            else:
                console.print("\n  [dim]Nothing to undo.[/dim]\n")

        elif choice == "0":
            console.print("\n[cyan]Goodbye![/cyan]\n")
            break

        else:
            console.print("[red]Invalid option. Try again.[/red]")


def _manage_menu(console: Console, display: Display, network):
    """Sub-menu for managing stations and connections."""
    console.print("\n[bold]Station & Connection Management[/bold]")
    console.print("  [1] Add Station")
    console.print("  [2] Remove Station")
    console.print("  [3] Add Connection")
    console.print("  [4] Remove Connection")
    console.print("  [5] Back to Main Menu\n")

    choice = input("  Choose: ").strip()

    if choice == "1":
        name = input("  Station name: ").strip()
        try:
            capacity = int(input("  Passenger capacity: "))
        except ValueError:
            console.print("[red]Invalid capacity.[/red]")
            return
        line = input("  Line (light_rail/metro/both): ").strip() or "light_rail"
        station = Station(name=name, capacity=capacity, line=line)
        network.add_station(station)
        console.print(f"\n  [green]Added: {station}[/green]\n")

    elif choice == "2":
        sid = display.station_picker(network, "Station to remove")
        name = network.stations[sid].name
        network.remove_station(sid)
        console.print(f"\n  [yellow]Removed: {name}[/yellow]\n")

    elif choice == "3":
        console.print("\n[bold]Select first station:[/bold]")
        id1 = display.station_picker(network, "Station 1")
        console.print("\n[bold]Select second station:[/bold]")
        id2 = display.station_picker(network, "Station 2")
        try:
            weight = float(input("  Travel time (minutes): "))
        except ValueError:
            console.print("[red]Invalid time.[/red]")
            return
        network.add_connection(id1, id2, weight)
        n1 = network.stations[id1].name
        n2 = network.stations[id2].name
        console.print(f"\n  [green]Connected: {n1} <-> {n2} ({weight} min)[/green]\n")

    elif choice == "4":
        console.print("\n[bold]Select first station:[/bold]")
        id1 = display.station_picker(network, "Station 1")
        console.print("\n[bold]Select second station:[/bold]")
        id2 = display.station_picker(network, "Station 2")
        try:
            network.remove_connection(id1, id2)
            console.print("\n  [yellow]Connection removed.[/yellow]\n")
        except ValueError as e:
            console.print(f"\n  [red]{e}[/red]\n")


if __name__ == "__main__":
    main()
