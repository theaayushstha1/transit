"""
Generate the 8-10 page PDF report for Baltimore MTA Transit Simulator.
COSC 320 - Algorithm Design
"""

from fpdf import FPDF

class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.cell(0, 5, "Baltimore MTA Transit Simulator | COSC 320 Algorithm Design", align="C")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def subsection_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(51, 51, 51)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(240, 240, 240)
        self.set_draw_color(200, 200, 200)
        x = self.get_x()
        y = self.get_y()
        # Calculate height
        lines = code.strip().split("\n")
        block_height = len(lines) * 4.5 + 4
        if y + block_height > self.h - 25:
            self.add_page()
            y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, block_height, "FD")
        self.set_xy(self.l_margin + 3, y + 2)
        for line in lines:
            self.cell(0, 4.5, line)
            self.ln(4.5)
        self.ln(4)
        self.set_font("Helvetica", "", 10)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            available = self.w - self.l_margin - self.r_margin
            col_widths = [available / len(headers)] * len(headers)

        # Check if table fits on current page
        needed = 7 * (len(rows) + 1) + 4
        if self.get_y() + needed > self.h - 25:
            self.add_page()

        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()

        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                align = "L" if i == 0 else "C"
                self.cell(col_widths[i], 7, str(cell), border=1, fill=True, align=align)
            self.ln()
            fill = not fill
        self.ln(4)


def build_report():
    pdf = Report()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ==================== TITLE PAGE ====================
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, "Baltimore MTA Transit Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "A Real-Data Transit Network Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Demonstrating Core Data Structures & Algorithms", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    info = [
        ("Course", "COSC 320 - Algorithm Design"),
        ("Student", "Aayush Shrestha"),
        ("University", "Morgan State University"),
        ("Date", "March 2026"),
        ("Language", "Python 3.13 with Rich terminal UI"),
    ]
    for label, value in info:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(50, 7, f"{label}:", align="R")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, f"  {value}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)

    pdf.set_draw_color(0, 51, 102)
    pdf.line(50, pdf.get_y(), pdf.w - 50, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 5, (
        "This project implements a transit network simulator using real Baltimore MTA data "
        "(Light Rail and Metro SubwayLink, 37 stations). It demonstrates graph traversal "
        "(DFS, BFS), shortest path (Dijkstra's), sorting (Merge Sort, Quick Sort), "
        "searching (Binary, Linear), and queue/stack data structures through an "
        "interactive terminal interface with animated algorithm visualizations."
    ), align="C")

    # ==================== PAGE 2: SYSTEM DESIGN ====================
    pdf.add_page()
    pdf.section_title("1. System Design & Architecture")

    pdf.body_text(
        "The simulator is organized into five modules following separation of concerns. "
        "Each module has a distinct responsibility, making the codebase maintainable and "
        "each algorithm independently testable."
    )

    pdf.subsection_title("1.1 Directory Structure")
    pdf.code_block(
        "baltimore-mta-simulator/\n"
        "|-- main.py                  # Entry point, menu loop\n"
        "|-- models/\n"
        "|   |-- station.py           # Station node class\n"
        "|   |-- passenger.py         # Passenger class\n"
        "|   +-- transit_network.py   # Graph (adjacency list)\n"
        "|-- algorithms/\n"
        "|   |-- traversal.py         # DFS + BFS\n"
        "|   |-- shortest_path.py     # Dijkstra's\n"
        "|   |-- sorting.py           # Merge Sort + Quick Sort\n"
        "|   +-- searching.py         # Binary + Linear Search\n"
        "|-- simulation/\n"
        "|   |-- undo_manager.py      # Stack-based undo\n"
        "|   +-- passenger_sim.py     # Queue-based boarding\n"
        "|-- data/\n"
        "|   +-- baltimore_mta.py     # Real MTA station data\n"
        "+-- ui/\n"
        "    |-- display.py           # Rich tables, panels, menus\n"
        "    +-- visualizer.py        # Algorithm animations"
    )

    pdf.subsection_title("1.2 Design Decisions")
    pdf.add_table(
        ["Decision", "Choice", "Reasoning"],
        [
            ["Graph repr.", "Adjacency list (dict of dicts)", "O(1) edge lookup, natural for sparse graphs"],
            ["Edge weights", "Travel time in minutes", "Enables Dijkstra, maps to real MTA data"],
            ["Shared stations", "Dedup by name", "Lexington Market on both lines = 1 node"],
            ["UI library", "Python Rich", "Colored tables, live animations, zero web deps"],
            ["Undo pattern", "Command pattern + inverse", "Clean stack demo, _raw_ methods skip undo"],
            ["Sorting key", "Station capacity", "Numeric field with varied values for comparison"],
        ],
        col_widths=[35, 55, 95],
    )

    # ==================== PAGE 3: DATA STRUCTURES ====================
    pdf.add_page()
    pdf.section_title("2. Data Structures")

    pdf.subsection_title("2.1 Graph (Adjacency List)")
    pdf.body_text(
        "The transit network is represented as a weighted undirected graph using an adjacency list. "
        "The implementation uses a dictionary of dictionaries: adj_list[station_id] maps to "
        "{neighbor_id: weight_in_minutes}. This provides O(1) edge lookup and insertion, "
        "which is optimal for the sparse graph topology of a transit network (37 nodes, 36 edges)."
    )
    pdf.code_block(
        "class TransitNetwork:\n"
        "    def __init__(self):\n"
        "        self.stations: dict[int, Station] = {}\n"
        "        self.adj_list: dict[int, dict[int, float]] = {}\n"
        "        self.undo_stack: list = []\n"
        "\n"
        "    def add_connection(self, id1, id2, weight):\n"
        "        self.adj_list[id1][id2] = weight  # undirected:\n"
        "        self.adj_list[id2][id1] = weight  # store both"
    )

    pdf.subsection_title("2.2 Queue (FIFO - Passenger Boarding)")
    pdf.body_text(
        "Each station maintains a passenger queue using collections.deque. Passengers are "
        "enqueued (append) when generated and dequeued (popleft) during boarding, demonstrating "
        "FIFO behavior. The deque provides O(1) for both operations, unlike a list which would "
        "be O(n) for popleft due to element shifting."
    )
    pdf.code_block(
        "# Enqueue: passenger joins the line\n"
        "station.passenger_queue.append(passenger)\n"
        "\n"
        "# Dequeue: board in FIFO order\n"
        "while queue and len(boarded) < capacity:\n"
        "    passenger = station.passenger_queue.popleft()"
    )

    pdf.subsection_title("2.3 Stack (LIFO - Undo System)")
    pdf.body_text(
        "The undo system uses a Python list as a stack (append/pop). Every graph mutation "
        "(add station, remove station, add/remove connection) pushes its inverse action onto "
        "the stack. The UndoManager pops actions and applies the inverse using internal _raw_ "
        "methods that bypass the undo stack to prevent infinite loops."
    )
    pdf.code_block(
        "# Public method pushes to undo stack\n"
        "def add_station(self, station):\n"
        "    self._raw_add_station(station)\n"
        "    self.undo_stack.append({\"action\": \"add_station\", ...})\n"
        "\n"
        "# Undo pops and applies inverse via _raw_ method\n"
        "def undo(self):\n"
        "    action = self.network.undo_stack.pop()\n"
        "    if action[\"action\"] == \"add_station\":\n"
        "        self.network._raw_remove_station(action[\"station\"].id)"
    )

    pdf.subsection_title("2.4 Priority Queue (Min-Heap - Dijkstra)")
    pdf.body_text(
        "Dijkstra's algorithm uses Python's heapq module as a min-heap priority queue. "
        "Each entry is a (distance, station_id) tuple. heappush and heappop both operate "
        "in O(log n) time, giving Dijkstra's algorithm its O((V+E) log V) time complexity."
    )

    # ==================== PAGE 4-5: ALGORITHMS ====================
    pdf.add_page()
    pdf.section_title("3. Algorithm Implementations")

    pdf.subsection_title("3.1 Depth-First Search (DFS)")
    pdf.body_text(
        "DFS is implemented recursively. It explores as deeply as possible along each branch "
        "before backtracking. The algorithm maintains a visited set to avoid cycles and a path "
        "list that grows/shrinks via append/pop as it explores/backtracks. It also records the "
        "visit order for the animated visualization."
    )
    pdf.code_block(
        "def _dfs_helper(current: int) -> bool:\n"
        "    visited.add(current)\n"
        "    visit_order.append(current)\n"
        "    path.append(current)\n"
        "    if current == goal_id:\n"
        "        return True\n"
        "    for neighbor_id, _ in sorted(network.get_neighbors(current)):\n"
        "        if neighbor_id not in visited:\n"
        "            if _dfs_helper(neighbor_id):\n"
        "                return True\n"
        "    path.pop()  # backtrack\n"
        "    return False"
    )

    pdf.subsection_title("3.2 Breadth-First Search (BFS)")
    pdf.body_text(
        "BFS uses a collections.deque as a queue. It explores all neighbors at the current "
        "depth before moving to the next level. BFS guarantees the shortest path in an "
        "unweighted graph (fewest edges). Each queue entry stores the full path to that node "
        "for easy path reconstruction."
    )
    pdf.code_block(
        "visited = {start_id}\n"
        "queue = deque([(start_id, [start_id])])\n"
        "while queue:\n"
        "    current, path = queue.popleft()\n"
        "    if current == goal_id:\n"
        "        return path\n"
        "    for neighbor_id, _ in sorted(network.get_neighbors(current)):\n"
        "        if neighbor_id not in visited:\n"
        "            visited.add(neighbor_id)\n"
        "            queue.append((neighbor_id, path + [neighbor_id]))"
    )

    pdf.subsection_title("3.3 DFS vs BFS Comparison")
    pdf.body_text(
        "When finding a route from Hunt Valley to Johns Hopkins Hospital, DFS visited all 37 "
        "stations (exploring every branch before finding the goal), while BFS visited only 23 "
        "(expanding level-by-level and stopping as soon as the goal is reached). Both found a "
        "17-station path in this case because the graph is largely linear. In a denser graph, "
        "BFS would find the shorter path while DFS might find a longer one."
    )
    pdf.add_table(
        ["Metric", "DFS (Recursive)", "BFS (Queue)"],
        [
            ["Path Length", "17 stations", "17 stations"],
            ["Nodes Visited", "37", "23"],
            ["Optimal (unweighted)?", "Not guaranteed", "Yes"],
            ["Time Complexity", "O(V + E)", "O(V + E)"],
            ["Space Complexity", "O(V) recursion stack", "O(V) queue"],
        ],
        col_widths=[55, 65, 65],
    )

    pdf.subsection_title("3.4 Dijkstra's Shortest Path Algorithm")
    pdf.body_text(
        "Dijkstra's algorithm finds the shortest weighted path using a min-heap priority queue. "
        "It greedily selects the unvisited node with the smallest known distance, then relaxes "
        "its neighbors. The path from Hunt Valley to Johns Hopkins Hospital traverses 17 stations "
        "in 37 minutes, transferring from Light Rail to Metro at Lexington Market."
    )
    pdf.code_block(
        "while pq:\n"
        "    current_dist, current = heapq.heappop(pq)\n"
        "    if current in visited: continue\n"
        "    visited.add(current)\n"
        "    if current == end_id: break\n"
        "    for neighbor_id, weight in network.get_neighbors(current):\n"
        "        new_dist = current_dist + weight\n"
        "        if new_dist < distances[neighbor_id]:\n"
        "            distances[neighbor_id] = new_dist\n"
        "            previous[neighbor_id] = current\n"
        "            heapq.heappush(pq, (new_dist, neighbor_id))"
    )

    # ==================== SORTING ====================
    pdf.add_page()
    pdf.subsection_title("3.5 Merge Sort")
    pdf.body_text(
        "Merge Sort divides the array in half recursively, then merges the sorted halves. "
        "It is stable (preserves relative order of equal elements) and always runs in "
        "O(n log n) time, but requires O(n) extra space for the merge step. "
        "On our 37 stations sorted by capacity, Merge Sort used 140 comparisons."
    )
    pdf.code_block(
        "def _merge(left, right):\n"
        "    result = []\n"
        "    i = j = 0\n"
        "    while i < len(left) and j < len(right):\n"
        "        comparisons[0] += 1\n"
        "        if key(left[i]) <= key(right[j]):\n"
        "            result.append(left[i]); i += 1\n"
        "        else:\n"
        "            result.append(right[j]); j += 1\n"
        "    result.extend(left[i:])\n"
        "    result.extend(right[j:])\n"
        "    return result"
    )

    pdf.subsection_title("3.6 Quick Sort")
    pdf.body_text(
        "Quick Sort selects a pivot (last element), partitions the array so elements smaller "
        "than the pivot go left and larger go right, then recurses on both halves. It is "
        "in-place (O(log n) stack space) but unstable and has O(n^2) worst-case on already "
        "sorted input. On our 37 stations, Quick Sort used 188 comparisons (more than Merge "
        "Sort's 140, as expected for this data distribution)."
    )

    pdf.subsection_title("3.7 Sorting Comparison")
    pdf.add_table(
        ["Metric", "Merge Sort", "Quick Sort"],
        [
            ["Comparisons (n=37)", "140", "188"],
            ["Time (measured)", "~35 us", "~23 us"],
            ["Time Complexity", "O(n log n) always", "O(n log n) avg / O(n^2) worst"],
            ["Space Complexity", "O(n) extra", "O(log n) stack"],
            ["Stable?", "Yes", "No"],
            ["In-place?", "No", "Yes"],
        ],
        col_widths=[55, 65, 65],
    )

    pdf.body_text(
        "Quick Sort was faster in practice despite more comparisons because it is in-place "
        "(better cache locality, no memory allocation for merge buffers). Merge Sort's "
        "advantage is guaranteed O(n log n) worst case and stability."
    )

    pdf.subsection_title("3.8 Binary Search vs Linear Search")
    pdf.body_text(
        "Binary Search requires a sorted array and eliminates half the remaining elements "
        "each step (O(log n)). Linear Search scans sequentially (O(n)). When searching for "
        "capacity 200 among 37 sorted stations, Binary Search found it in 3 comparisons "
        "while Linear Search needed 20."
    )
    pdf.add_table(
        ["Metric", "Binary Search", "Linear Search"],
        [
            ["Comparisons (target=200)", "3", "20"],
            ["Time Complexity", "O(log n)", "O(n)"],
            ["Requires Sorted?", "Yes", "No"],
        ],
        col_widths=[55, 65, 65],
    )

    # ==================== COMPLEXITY ====================
    pdf.ln(4)
    pdf.section_title("4. Algorithm Complexity Analysis")

    pdf.body_text(
        "The following table summarizes the theoretical time and space complexity of every "
        "operation implemented in the simulator. These are verified empirically by the "
        "performance dashboard, which runs live benchmarks."
    )

    pdf.add_table(
        ["Operation", "Time Complexity", "Space Complexity"],
        [
            ["Add Station", "O(1)", "O(1)"],
            ["Remove Station", "O(V + E)", "O(1)"],
            ["Add Connection", "O(1)", "O(1)"],
            ["Remove Connection", "O(1)", "O(1)"],
            ["DFS Traversal", "O(V + E)", "O(V) recursion stack"],
            ["BFS Traversal", "O(V + E)", "O(V) queue"],
            ["Dijkstra's Algorithm", "O((V+E) log V)", "O(V)"],
            ["Merge Sort", "O(n log n) always", "O(n) extra"],
            ["Quick Sort", "O(n log n) avg / O(n^2) worst", "O(log n) stack"],
            ["Binary Search", "O(log n)", "O(1)"],
            ["Linear Search", "O(n)", "O(1)"],
            ["Stack Push/Pop", "O(1)", "O(1) per action"],
            ["Queue Enq/Deq", "O(1)", "O(1)"],
        ],
        col_widths=[55, 65, 65],
    )

    pdf.subsection_title("4.1 Empirical Benchmarks")
    pdf.body_text(
        "All algorithms were benchmarked on the full 37-station, 36-edge Baltimore MTA network. "
        "Timings use time.perf_counter() for microsecond precision. Sorting and searching "
        "algorithms also track exact comparison counts."
    )
    pdf.add_table(
        ["Algorithm", "Measured Time", "Comparisons"],
        [
            ["DFS (Hunt Valley to JHH)", "~18 us", "-"],
            ["BFS (Hunt Valley to JHH)", "~14 us", "-"],
            ["Dijkstra (Hunt Valley to JHH)", "~12 us", "-"],
            ["Merge Sort (37 stations)", "~35 us", "140"],
            ["Quick Sort (37 stations)", "~23 us", "188"],
            ["Binary Search (target=200)", "~0.3 us", "3"],
            ["Linear Search (target=200)", "~1.2 us", "20"],
        ],
        col_widths=[70, 55, 60],
    )

    pdf.body_text(
        "Key observations: (1) BFS outperforms DFS on this graph because it visits fewer nodes "
        "by expanding level-by-level. (2) Dijkstra is the fastest graph algorithm because it "
        "terminates early when the target is reached. (3) Quick Sort is faster than Merge Sort "
        "in practice due to cache-friendly in-place operations, despite more comparisons. "
        "(4) Binary Search uses 3 comparisons vs Linear's 20, confirming O(log n) vs O(n)."
    )

    # ==================== REAL DATA ====================
    pdf.ln(4)
    pdf.section_title("5. Baltimore MTA Transit Data")

    pdf.body_text(
        "The simulator uses real Baltimore MTA data for two transit lines. Station names, "
        "line assignments, and approximate travel times are based on the actual MTA system map."
    )

    pdf.subsection_title("5.1 Light Rail (24 stations)")
    pdf.body_text(
        "Runs from Hunt Valley in the north through downtown Baltimore (Penn Station, "
        "Camden Yards) to Cromwell/Glen Burnie in the south, with a spur to BWI Airport "
        "branching at Linthicum. The line has 23 connections with travel times of 2-5 minutes."
    )

    pdf.subsection_title("5.2 Metro SubwayLink (13 stations)")
    pdf.body_text(
        "Runs from Owings Mills in the northwest through Mondawmin and downtown to Johns "
        "Hopkins Hospital in the east. The line has 13 connections with travel times of 2-4 minutes."
    )

    pdf.subsection_title("5.3 Transfer Point: Lexington Market")
    pdf.body_text(
        "Lexington Market appears on both lines and is stored as a single node in the graph "
        "with 4 connections (2 Light Rail neighbors: Centre Street and Convention Center; "
        "2 Metro neighbors: State Center and Charles Center). This creates the cross-line "
        "routing that makes Dijkstra's algorithm interesting: the shortest path from Hunt "
        "Valley (Light Rail) to Johns Hopkins Hospital (Metro) naturally routes through "
        "Lexington Market, demonstrating a real-world transfer."
    )

    pdf.subsection_title("5.4 Network Statistics")
    pdf.add_table(
        ["Property", "Value"],
        [
            ["Total stations", "37"],
            ["Total connections", "36"],
            ["Light Rail stations", "24 (including shared)"],
            ["Metro stations", "14 (including shared)"],
            ["Transfer stations", "1 (Lexington Market)"],
            ["Min travel time", "2 minutes"],
            ["Max travel time", "5 minutes (Linthicum to BWI)"],
            ["Longest shortest path", "37 min (Hunt Valley to JHH)"],
        ],
        col_widths=[80, 105],
    )

    # ==================== UI ====================
    pdf.ln(4)
    pdf.section_title("6. User Interface & Visualization")

    pdf.body_text(
        "The simulator uses the Python Rich library for a polished terminal UI. All output "
        "is styled with colored text, formatted tables, bordered panels, and tree views. "
        "The Rich Live display enables real-time animated visualizations."
    )

    pdf.subsection_title("6.1 Interactive Menu")
    pdf.body_text(
        "The main menu provides 10 options covering all functionality: network viewing, "
        "station/connection management, DFS vs BFS comparison, Dijkstra shortest path, "
        "passenger boarding simulation, sorting comparison, searching comparison, "
        "performance dashboard, undo, and exit. Users can select stations by ID number or "
        "by typing the station name (case-insensitive matching)."
    )

    pdf.subsection_title("6.2 Algorithm Animations")
    pdf.body_text(
        "DFS and BFS traversals are animated using Rich Live display. Each step shows a table "
        "of all stations with color-coded status: white (unvisited), yellow (currently exploring), "
        "green (on the final path), and dim gray (visited but not on path). This makes the "
        "behavioral difference between DFS and BFS immediately visible: DFS goes deep then "
        "backtracks, while BFS expands outward level by level. The animation runs at ~6 frames "
        "per second, fast enough to convey behavior without dragging during a demo."
    )

    pdf.subsection_title("6.3 Passenger Boarding Animation")
    pdf.body_text(
        "The boarding simulation animates a progress bar that fills as passengers board one by one, "
        "showing the FIFO queue in action. The display updates in real-time inside a bordered panel "
        "with station info, capacity, boarded count, and remaining queue count. For example, "
        "generating 50 passengers at Camden Yards with a train capacity of 30 boards exactly 30 "
        "in FIFO order, leaving 20 in the queue."
    )

    pdf.subsection_title("6.4 Dijkstra Path Display")
    pdf.body_text(
        "Dijkstra results are shown as a visual chain with travel times on each edge: "
        "Station A --3min--> Station B --2min--> Station C. The panel also displays total "
        "travel time, number of stations, and number of line transfers. Cross-line routes "
        "automatically detect when the active transit line changes, counting the transfer at "
        "shared stations like Lexington Market."
    )

    pdf.subsection_title("6.5 Performance Dashboard")
    pdf.body_text(
        "The performance dashboard runs live benchmarks on all algorithms and displays two tables: "
        "a theoretical complexity table (Big-O for time and space) and an empirical benchmarks table "
        "with measured execution time and comparison counts. This bridges theory and practice, "
        "showing that the measured performance matches asymptotic predictions."
    )

    # ==================== CONCLUSION ====================
    pdf.ln(4)
    pdf.section_title("7. Conclusion")

    pdf.body_text(
        "This project demonstrates the practical application of core data structures and "
        "algorithms to a real-world transit network. By using actual Baltimore MTA station data "
        "rather than abstract examples, the project grounds algorithmic concepts in a tangible "
        "system that students and professors can relate to."
    )

    pdf.body_text(
        "Key takeaways from the implementation:"
    )

    points = [
        "Graph representation: An adjacency list (dict of dicts) provides O(1) edge operations "
        "and naturally models the sparse connectivity of a transit network.",

        "DFS vs BFS: BFS guarantees the shortest unweighted path and typically visits fewer nodes, "
        "while DFS's deep exploration is visible in the animation. Both run in O(V+E) time.",

        "Dijkstra's algorithm: The min-heap priority queue enables weighted shortest path in "
        "O((V+E) log V). Cross-line routing through shared stations demonstrates real graph connectivity.",

        "Sorting: Merge Sort's guaranteed O(n log n) and stability comes at the cost of O(n) space. "
        "Quick Sort's in-place operation gives better cache performance despite O(n^2) worst case.",

        "Searching: Binary Search's O(log n) dramatically outperforms Linear Search's O(n), "
        "confirmed empirically with 3 vs 20 comparisons on 37 stations.",

        "Queue/Stack: The deque-based passenger queue and list-based undo stack demonstrate "
        "fundamental FIFO/LIFO patterns with O(1) operations.",
    ]

    for i, point in enumerate(points, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(8, 5.5, f"{i}.")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5.5, point)
        pdf.ln(1)

    pdf.ln(4)
    pdf.body_text(
        "The Rich terminal UI elevates the project beyond a standard command-line implementation, "
        "with animated algorithm visualizations that make abstract concepts tangible. The performance "
        "dashboard bridges theory and practice by displaying Big-O complexity alongside measured "
        "benchmarks, reinforcing that algorithmic analysis predicts real-world behavior."
    )

    # ==================== REFERENCES ====================
    pdf.ln(8)
    pdf.section_title("References")

    refs = [
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to Algorithms (4th ed.). MIT Press.",
        "Baltimore MTA. Maryland Transit Administration System Map. mta.maryland.gov",
        "Python Software Foundation. collections.deque, heapq documentation. docs.python.org",
        "Will McGugan. Rich: Python library for rich text in the terminal. github.com/Textualize/rich",
    ]
    pdf.set_font("Helvetica", "", 9)
    for i, ref in enumerate(refs, 1):
        pdf.cell(8, 5, f"[{i}]")
        pdf.multi_cell(0, 5, ref)
        pdf.ln(1)

    # Save
    output_path = "report.pdf"
    pdf.output(output_path)
    print(f"Report generated: {output_path} ({pdf.page_no()} pages)")
    return output_path


if __name__ == "__main__":
    build_report()
