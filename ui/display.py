"""Rich terminal UI: tables, panels, menus, station picker."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
from rich import box

from models.transit_network import TransitNetwork


class Display:
    """All Rich-based display functions for the transit simulator."""

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    def show_menu(self) -> str:
        """Display main menu and return user's choice."""
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

        self.console.print(Panel(menu_text, box=box.ROUNDED, border_style="cyan"))
        return input("  Choose an option: ").strip()

    def show_network(self, network: TransitNetwork) -> None:
        """Display the network as a Rich Tree grouped by transit line."""
        tree = Tree("[bold cyan]Baltimore MTA Network[/bold cyan]")

        # Group stations by line
        lines = {"light_rail": [], "metro": [], "both": []}
        for station in network.get_all_stations():
            lines.setdefault(station.line, []).append(station)

        line_names = {
            "light_rail": "Light Rail",
            "metro": "Metro SubwayLink",
            "both": "Transfer Stations",
        }

        for line_key, display_name in line_names.items():
            stations = lines.get(line_key, [])
            if not stations:
                continue
            line_branch = tree.add(
                f"[bold yellow]{display_name}[/bold yellow] ({len(stations)} stations)"
            )
            for station in stations:
                neighbors = network.get_neighbors(station.station_id)
                station_node = line_branch.add(
                    f"[green]{station.name}[/green] "
                    f"(ID: {station.station_id}, Cap: {station.capacity})"
                )
                for neighbor_id, weight in neighbors:
                    neighbor = network.stations[neighbor_id]
                    station_node.add(
                        f"-> {neighbor.name} ({weight:.0f} min)"
                    )

        self.console.print(tree)

    def show_station_table(self, network: TransitNetwork) -> None:
        """Display all stations in a Rich Table."""
        table = Table(
            title="All Stations",
            box=box.ROUNDED,
            border_style="cyan",
            header_style="bold white",
        )
        table.add_column("ID", style="dim", width=4)
        table.add_column("Name", style="green")
        table.add_column("Line", style="yellow")
        table.add_column("Capacity", justify="right", style="cyan")
        table.add_column("Connections", justify="right")

        for station in network.get_all_stations():
            conn_count = len(network.get_neighbors(station.station_id))
            line_display = {
                "light_rail": "Light Rail",
                "metro": "Metro",
                "both": "Both",
            }.get(station.line, station.line)
            table.add_row(
                str(station.station_id),
                station.name,
                line_display,
                str(station.capacity),
                str(conn_count),
            )

        self.console.print(table)

    def station_picker(self, network: TransitNetwork, prompt: str = "Select station") -> int:
        """Show numbered station list and let user pick one. Returns station_id."""
        self.show_station_table(network)
        stations = network.get_all_stations()

        while True:
            choice = input(f"\n  {prompt} (enter ID or name): ").strip()

            # Try by ID
            try:
                sid = int(choice)
                if sid in network.stations:
                    return sid
            except ValueError:
                pass

            # Try by name
            station = network.get_station_by_name(choice)
            if station:
                return station.station_id

            self.console.print("[red]Station not found. Try again.[/red]")

    def show_dijkstra_result(
        self, network: TransitNetwork, path: list[int], total_time: float
    ) -> None:
        """Display Dijkstra result as a visual chain with weights."""
        if not path:
            self.console.print("[red]No path found![/red]")
            return

        chain_parts = []
        for i, sid in enumerate(path):
            station = network.stations[sid]
            chain_parts.append(f"[bold green]{station.name}[/bold green]")
            if i < len(path) - 1:
                next_sid = path[i + 1]
                weight = network.adj_list[sid][next_sid]
                chain_parts.append(f" [dim]--{weight:.0f}min-->[/dim] ")

        chain = "".join(chain_parts)

        # Detect line transfers (track the "active" line, ignoring "both" stations)
        transfers = 0
        active_line = None
        for sid in path:
            line = network.stations[sid].line
            if line == "both":
                continue
            if active_line is not None and line != active_line:
                transfers += 1
            active_line = line

        start_name = network.stations[path[0]].name
        end_name = network.stations[path[-1]].name

        body = (
            f"\n  {chain}\n\n"
            f"  [bold]Total travel time:[/bold] {total_time:.0f} minutes\n"
            f"  [bold]Stations:[/bold] {len(path)}    "
            f"[bold]Transfers:[/bold] {transfers}\n"
        )

        self.console.print(
            Panel(
                body,
                title=f"Shortest Path: {start_name} -> {end_name}",
                border_style="green",
                box=box.ROUNDED,
            )
        )

    def show_sort_comparison(
        self,
        merge_result: tuple,
        quick_result: tuple,
        network: TransitNetwork,
    ) -> None:
        """Side-by-side comparison of Merge Sort vs Quick Sort results."""
        merge_sorted, merge_comps, merge_time = merge_result
        quick_sorted, quick_comps, quick_time = quick_result

        table = Table(
            title="Sorting Comparison: Merge Sort vs Quick Sort",
            box=box.ROUNDED,
            border_style="cyan",
        )
        table.add_column("Metric", style="bold")
        table.add_column("Merge Sort", style="green", justify="right")
        table.add_column("Quick Sort", style="yellow", justify="right")

        table.add_row("Comparisons", str(merge_comps), str(quick_comps))
        table.add_row("Time", f"{merge_time * 1_000_000:.2f} us", f"{quick_time * 1_000_000:.2f} us")
        table.add_row("Time Complexity", "O(n log n) always", "O(n log n) avg")
        table.add_row("Space Complexity", "O(n) extra", "O(log n) stack")
        table.add_row("Stable?", "Yes", "No")

        self.console.print(table)

        # Show sorted result
        sorted_table = Table(title="Stations Sorted by Capacity", box=box.SIMPLE)
        sorted_table.add_column("Rank", width=4)
        sorted_table.add_column("Name", style="green")
        sorted_table.add_column("Capacity", justify="right", style="cyan")

        for i, station in enumerate(merge_sorted):
            sorted_table.add_row(str(i + 1), station.name, str(station.capacity))

        self.console.print(sorted_table)

    def show_search_comparison(
        self,
        target: int,
        binary_result: tuple,
        linear_result: tuple,
        sorted_stations: list,
    ) -> None:
        """Compare Binary Search vs Linear Search results."""
        b_idx, b_comps, b_time = binary_result
        l_idx, l_comps, l_time = linear_result

        table = Table(
            title=f"Search Comparison: Target Capacity = {target}",
            box=box.ROUNDED,
            border_style="cyan",
        )
        table.add_column("Metric", style="bold")
        table.add_column("Binary Search", style="green", justify="right")
        table.add_column("Linear Search", style="yellow", justify="right")

        found_b = sorted_stations[b_idx].name if b_idx >= 0 else "Not found"
        found_l = sorted_stations[l_idx].name if l_idx >= 0 else "Not found"

        table.add_row("Found", found_b, found_l)
        table.add_row("Comparisons", str(b_comps), str(l_comps))
        table.add_row("Time", f"{b_time * 1_000_000:.2f} us", f"{l_time * 1_000_000:.2f} us")
        table.add_row("Time Complexity", "O(log n)", "O(n)")
        table.add_row("Requires Sorted?", "Yes", "No")

        self.console.print(table)

    def show_performance_dashboard(self, network: TransitNetwork) -> None:
        """Run live benchmarks and display alongside Big-O theory."""
        import time as _time
        from algorithms.traversal import dfs, bfs
        from algorithms.shortest_path import dijkstra
        from algorithms.sorting import merge_sort, quick_sort
        from algorithms.searching import binary_search, linear_search

        self.console.print("\n  [dim]Running benchmarks...[/dim]\n")

        # Pick endpoints for graph algorithm benchmarks
        all_ids = list(network.stations.keys())
        start_id, end_id = all_ids[0], all_ids[-1]

        # Run benchmarks
        _, _, dfs_t = dfs(network, start_id, end_id)
        _, _, bfs_t = bfs(network, start_id, end_id)
        _, _, _, dij_t = dijkstra(network, start_id, end_id)

        stations = network.get_all_stations()
        _, m_comps, m_t = merge_sort(stations)
        _, q_comps, q_t = quick_sort(stations)

        sorted_s = merge_sort(stations)[0]
        target = sorted_s[len(sorted_s) // 2].capacity
        _, b_comps, b_t = binary_search(sorted_s, target)
        _, l_comps, l_t = linear_search(sorted_s, target)

        # Complexity table
        theory = Table(
            title="Algorithm Complexity (Theory)",
            box=box.ROUNDED,
            border_style="cyan",
            header_style="bold white",
        )
        theory.add_column("Operation", style="bold")
        theory.add_column("Time Complexity", style="green")
        theory.add_column("Space Complexity", style="yellow")

        theory_data = [
            ("Add Station", "O(1)", "O(1)"),
            ("Remove Station", "O(V + E)", "O(1)"),
            ("Add Connection", "O(1)", "O(1)"),
            ("Remove Connection", "O(1)", "O(1)"),
            ("DFS Traversal", "O(V + E)", "O(V) recursion stack"),
            ("BFS Traversal", "O(V + E)", "O(V) queue"),
            ("Dijkstra's Algorithm", "O((V+E) log V)", "O(V)"),
            ("Merge Sort", "O(n log n) always", "O(n) extra"),
            ("Quick Sort", "O(n log n) avg / O(n^2) worst", "O(log n) stack"),
            ("Binary Search", "O(log n)", "O(1)"),
            ("Linear Search", "O(n)", "O(1)"),
            ("Stack Push/Pop (Undo)", "O(1)", "O(1)"),
            ("Queue Enq/Deq (Passengers)", "O(1)", "O(1)"),
        ]
        for op, tc, sc in theory_data:
            theory.add_row(op, tc, sc)
        self.console.print(theory)

        # Empirical benchmarks table
        n = network.station_count()
        bench = Table(
            title=f"Empirical Benchmarks (n={n} stations, {network.connection_count()} edges)",
            box=box.ROUNDED,
            border_style="green",
            header_style="bold white",
        )
        bench.add_column("Algorithm", style="bold")
        bench.add_column("Measured Time", style="cyan", justify="right")
        bench.add_column("Comparisons", style="yellow", justify="right")

        bench.add_row("DFS", f"{dfs_t * 1_000_000:.2f} us", "-")
        bench.add_row("BFS", f"{bfs_t * 1_000_000:.2f} us", "-")
        bench.add_row("Dijkstra", f"{dij_t * 1_000_000:.2f} us", "-")
        bench.add_row("Merge Sort", f"{m_t * 1_000_000:.2f} us", str(m_comps))
        bench.add_row("Quick Sort", f"{q_t * 1_000_000:.2f} us", str(q_comps))
        bench.add_row("Binary Search", f"{b_t * 1_000_000:.2f} us", str(b_comps))
        bench.add_row("Linear Search", f"{l_t * 1_000_000:.2f} us", str(l_comps))

        self.console.print(bench)
        self.console.print()
