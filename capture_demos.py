"""Capture each demo screen as SVG using Rich's recording feature."""

import sys
sys.path.insert(0, ".")

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import box

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
from models.passenger import Passenger

import os
os.makedirs("screenshots", exist_ok=True)


def capture(filename, title, func):
    """Run func(console, display, ...) with recording, export SVG."""
    Station._next_id = 1  # Reset station IDs for each capture
    Passenger._next_id = 1
    console = Console(record=True, width=90)
    func(console)
    svg = console.export_svg(title=title)
    path = f"screenshots/{filename}.svg"
    with open(path, "w") as f:
        f.write(svg)
    print(f"  Saved: {path}")


def demo_menu(console):
    network = build_default_network()
    console.print(f"\n[bold cyan]Loaded Baltimore MTA network:[/bold cyan] "
                  f"{network.station_count()} stations, "
                  f"{network.connection_count()} connections\n")
    # Render menu panel directly (skip input() call)
    menu_text = Text()
    menu_text.append("Baltimore MTA Transit Simulator\n\n", style="bold cyan")
    menu_text.append("  [1]  View Network Map\n")
    menu_text.append("  [2]  Manage Stations & Connections\n")
    menu_text.append("  [3]  Find Route (DFS vs BFS)\n")
    menu_text.append("  [4]  Shortest Path (Dijkstra)\n")
    menu_text.append("  [5]  Passenger Boarding Simulation\n")
    menu_text.append("  [6]  Sort Stations (Merge vs Quick)\n")
    menu_text.append("  [7]  Search Stations (Binary vs Linear)\n")
    menu_text.append("  [8]  Performance Dashboard\n")
    menu_text.append("  [9]  Undo Last Action\n")
    menu_text.append("  [0]  Exit\n")
    console.print(Panel(menu_text, box=box.ROUNDED, border_style="cyan"))


def demo_network_map(console):
    network = build_default_network()
    display = Display(console)
    display.show_network(network)


def demo_dijkstra(console):
    network = build_default_network()
    display = Display(console)
    path, total_time, distances, elapsed = dijkstra(network, 1, 37)
    display.show_dijkstra_result(network, path, total_time)
    console.print(f"  [dim]Dijkstra completed in {elapsed * 1_000_000:.2f} us[/dim]\n")


def demo_dfs_vs_bfs(console):
    network = build_default_network()
    viz = Visualizer(console)
    dfs_result = dfs(network, 1, 37)
    bfs_result = bfs(network, 1, 37)
    viz.show_traversal_comparison(network, dfs_result, bfs_result)


def demo_sorting(console):
    network = build_default_network()
    display = Display(console)
    stations = network.get_all_stations()
    console.print(f"\n[cyan]Sorting {len(stations)} stations by capacity...[/cyan]\n")
    merge_result = merge_sort(stations)
    quick_result = quick_sort(stations)
    display.show_sort_comparison(merge_result, quick_result, network)


def demo_search(console):
    network = build_default_network()
    display = Display(console)
    stations = network.get_all_stations()
    sorted_stations = merge_sort(stations)[0]
    target = 200
    b_result = binary_search(sorted_stations, target)
    l_result = linear_search(sorted_stations, target)
    display.show_search_comparison(target, b_result, l_result, sorted_stations)


def demo_passenger(console):
    network = build_default_network()
    viz = Visualizer(console)
    sim = PassengerSimulation(network)
    station_id = 16  # Camden Yards
    station = network.stations[station_id]
    sim.generate_passengers(station_id, 50)
    total_waiting = sim.get_queue_size(station_id)
    console.print(f"\n  [bold]Generated 50 passengers at {station.name}[/bold]\n")
    boarded, remaining = sim.board_passengers(station_id, 30)
    # Static version for screenshot (animation won't capture)
    bar_width = 30
    filled = int((len(boarded) / 30) * bar_width)
    empty = bar_width - filled
    bar = "[green]" + "#" * filled + "[/green][dim]" + "-" * empty + "[/dim]"
    content = (
        f"\n  [bold cyan]Station: {station.name}[/bold cyan]\n"
        f"  Passengers waiting: {total_waiting}\n"
        f"  Train capacity: 30\n\n"
        f"  Boarding: {bar} {len(boarded)}/30 boarded\n"
        f"  Remaining in queue: {remaining}\n"
    )
    console.print(Panel(content, title="Passenger Boarding", border_style="cyan", box=box.ROUNDED))


def demo_undo(console):
    network = build_default_network()
    undo = UndoManager(network)
    console.print("\n[bold]Step 1:[/bold] Add new station 'Morgan State'")
    station = Station(name="Morgan State", capacity=150, line="light_rail")
    network.add_station(station)
    console.print(f"  [green]Added: {station}[/green]")
    console.print(f"  Network now has {network.station_count()} stations\n")
    console.print("[bold]Step 2:[/bold] Undo the addition")
    msg = undo.undo()
    console.print(f"  [yellow]{msg}[/yellow]")
    console.print(f"  Network back to {network.station_count()} stations\n")


def demo_dashboard(console):
    network = build_default_network()
    display = Display(console)
    display.show_performance_dashboard(network)


def demo_station_table(console):
    network = build_default_network()
    display = Display(console)
    display.show_station_table(network)


if __name__ == "__main__":
    print("Capturing demo screenshots...\n")
    captures = [
        ("01_menu", "Main Menu", demo_menu),
        ("02_network_map", "Network Map", demo_network_map),
        ("03_station_table", "All Stations", demo_station_table),
        ("04_dijkstra", "Dijkstra Shortest Path", demo_dijkstra),
        ("05_dfs_vs_bfs", "DFS vs BFS Comparison", demo_dfs_vs_bfs),
        ("06_sorting", "Merge Sort vs Quick Sort", demo_sorting),
        ("07_search", "Binary vs Linear Search", demo_search),
        ("08_passenger", "Passenger Boarding", demo_passenger),
        ("09_undo", "Undo System", demo_undo),
        ("10_dashboard", "Performance Dashboard", demo_dashboard),
    ]
    for filename, title, func in captures:
        capture(filename, title, func)
    print("\nDone! All SVGs saved in screenshots/")
