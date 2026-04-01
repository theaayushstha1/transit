"""Algorithm visualization with Rich Live display."""

import time as time_module

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich import box

from models.transit_network import TransitNetwork


class Visualizer:
    """Animated algorithm visualizations using Rich Live display."""

    def __init__(self, console: Console | None = None, step_delay: float = 0.15):
        self.console = console or Console()
        self.step_delay = step_delay

    def _build_traversal_table(
        self,
        network: TransitNetwork,
        visited: set,
        path_set: set,
        current: int | None,
        algorithm: str,
        step: int,
        total_steps: int,
    ) -> Panel:
        """Build a station table with color-coded traversal state."""
        table = Table(box=box.SIMPLE, border_style="dim")
        table.add_column("ID", width=4)
        table.add_column("Station", width=28)
        table.add_column("Status", width=14)

        for station in network.get_all_stations():
            sid = station.station_id

            if sid == current:
                style = "bold yellow"
                status = "EXPLORING"
            elif sid in path_set and sid in visited:
                style = "bold green"
                status = "ON PATH"
            elif sid in visited:
                style = "dim"
                status = "visited"
            else:
                style = "white"
                status = ""

            table.add_row(
                str(sid),
                Text(station.name, style=style),
                Text(status, style=style),
            )

        title = f"{algorithm} - Step {step}/{total_steps}"
        return Panel(table, title=title, border_style="cyan", box=box.ROUNDED)

    def animate_traversal(
        self,
        network: TransitNetwork,
        visit_order: list[int],
        final_path: list[int],
        algorithm_name: str,
    ) -> None:
        """Animate DFS or BFS traversal with color-coded nodes."""
        if not visit_order:
            self.console.print("[red]No nodes were visited.[/red]")
            return

        path_set = set(final_path)
        visited_so_far = set()
        total = len(visit_order)

        with Live(console=self.console, refresh_per_second=4) as live:
            for i, node_id in enumerate(visit_order):
                visited_so_far.add(node_id)
                panel = self._build_traversal_table(
                    network, visited_so_far, path_set,
                    current=node_id,
                    algorithm=algorithm_name,
                    step=i + 1,
                    total_steps=total,
                )
                live.update(panel)
                time_module.sleep(self.step_delay)

            # Final frame: no "current" node, just show visited + path
            panel = self._build_traversal_table(
                network, visited_so_far, path_set,
                current=None,
                algorithm=f"{algorithm_name} - Complete",
                step=total,
                total_steps=total,
            )
            live.update(panel)
            time_module.sleep(0.5)

    def show_traversal_comparison(
        self,
        network: TransitNetwork,
        dfs_result: tuple,
        bfs_result: tuple,
    ) -> None:
        """Side-by-side comparison of DFS vs BFS results."""
        dfs_path, dfs_visited, dfs_time = dfs_result
        bfs_path, bfs_visited, bfs_time = bfs_result

        table = Table(
            title="DFS vs BFS Comparison",
            box=box.ROUNDED,
            border_style="cyan",
        )
        table.add_column("Metric", style="bold")
        table.add_column("DFS (Recursive)", style="green", justify="right")
        table.add_column("BFS (Queue)", style="yellow", justify="right")

        table.add_row("Path Found?", "Yes" if dfs_path else "No", "Yes" if bfs_path else "No")
        table.add_row("Path Length", f"{len(dfs_path)} stations", f"{len(bfs_path)} stations")
        table.add_row("Nodes Visited", str(len(dfs_visited)), str(len(bfs_visited)))
        table.add_row(
            "Time",
            f"{dfs_time * 1_000_000:.2f} us",
            f"{bfs_time * 1_000_000:.2f} us",
        )
        table.add_row("Optimal? (unweighted)", "Not guaranteed", "Yes")
        table.add_row("Data Structure", "Recursion stack", "Queue (deque)")

        self.console.print(table)

        # Show paths
        if dfs_path:
            dfs_names = " -> ".join(network.stations[s].name for s in dfs_path)
            self.console.print(f"\n  [green]DFS path:[/green] {dfs_names}")
        if bfs_path:
            bfs_names = " -> ".join(network.stations[s].name for s in bfs_path)
            self.console.print(f"  [yellow]BFS path:[/yellow] {bfs_names}\n")

    def show_boarding_animation(
        self,
        station_name: str,
        total_waiting: int,
        train_capacity: int,
        boarded_count: int,
        remaining: int,
    ) -> None:
        """Animate passenger boarding with a filling progress bar."""
        bar_width = 30

        with Live(console=self.console, refresh_per_second=10) as live:
            for step in range(boarded_count + 1):
                filled = int((step / train_capacity) * bar_width) if train_capacity > 0 else 0
                empty = bar_width - filled
                bar = "[green]" + "#" * filled + "[/green][dim]" + "-" * empty + "[/dim]"

                content = (
                    f"\n  [bold cyan]Station: {station_name}[/bold cyan]\n"
                    f"  Passengers waiting: {total_waiting}\n"
                    f"  Train capacity: {train_capacity}\n\n"
                    f"  Boarding: {bar} {step}/{train_capacity} boarded\n"
                    f"  Remaining in queue: {total_waiting - step}\n"
                )
                live.update(Panel(content, title="Passenger Boarding", border_style="cyan", box=box.ROUNDED))
                if step < boarded_count:
                    time_module.sleep(0.05)

            # Hold final frame
            time_module.sleep(0.3)
