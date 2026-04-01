"""
Generate the 8-10 page PDF report for Baltimore MTA Transit Simulator.
COSC 320 - Algorithm Design
"""

import os
from fpdf import FPDF

SCREENSHOTS_DIR = "screenshots/png"
FIG_NUM = [0]  # mutable counter for figure numbering


def fig(caption):
    """Return 'Figure N: caption' and increment counter."""
    FIG_NUM[0] += 1
    return f"Figure {FIG_NUM[0]}: {caption}"


class Report(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 7.5)
            self.cell(0, 4, "Baltimore MTA Transit Simulator  |  COSC 320 Algorithm Design  |  Aayush Shrestha", align="C")
            self.ln(6)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7.5)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2.5)
        self.set_text_color(0, 0, 0)

    def subsection_title(self, title):
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(51, 51, 51)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        self.set_font("Helvetica", "", 8.5)
        self.multi_cell(0, 4.2, text)
        self.ln(1.5)

    def figure_caption(self, text):
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(80, 80, 80)
        self.cell(0, 4, text, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def inline_image(self, filename, caption, width_pct=0.85):
        """Place a screenshot inline with a figure caption. width_pct = fraction of usable width."""
        png_path = f"{SCREENSHOTS_DIR}/{filename}.png"
        if not os.path.isfile(png_path):
            return
        usable_w = self.w - self.l_margin - self.r_margin
        img_w = usable_w * width_pct
        x_offset = (usable_w - img_w) / 2 + self.l_margin
        # Check if we need a page break (estimate image height)
        est_h = img_w * 0.48 + 8
        if self.get_y() + est_h > self.h - 15:
            self.add_page()
        try:
            self.image(png_path, x=x_offset, w=img_w)
        except Exception:
            pass
        self.figure_caption(fig(caption))

    def inline_image_half(self, filename, caption, width_pct=0.55):
        """Smaller inline screenshot."""
        self.inline_image(filename, caption, width_pct)

    def code_block(self, code):
        self.set_font("Courier", "", 7)
        self.set_fill_color(242, 242, 242)
        self.set_draw_color(210, 210, 210)
        y = self.get_y()
        lines = code.strip().split("\n")
        block_height = len(lines) * 3.4 + 3
        if y + block_height > self.h - 15:
            self.add_page()
            y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, block_height, "FD")
        self.set_xy(self.l_margin + 2, y + 1.5)
        for line in lines:
            self.cell(0, 3.4, line)
            self.ln(3.4)
        self.ln(2.5)
        self.set_font("Helvetica", "", 8.5)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            available = self.w - self.l_margin - self.r_margin
            col_widths = [available / len(headers)] * len(headers)

        row_h = 5.5
        needed = row_h * (len(rows) + 1) + 3
        if self.get_y() + needed > self.h - 15:
            self.add_page()

        self.set_font("Helvetica", "B", 7.5)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], row_h, h, border=1, fill=True, align="C")
        self.ln()

        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(248, 248, 248)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                align = "L" if i == 0 else "C"
                self.cell(col_widths[i], row_h, str(cell), border=1, fill=True, align=align)
            self.ln()
            fill = not fill
        self.ln(2.5)


def build_report():
    pdf = Report()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # ==================== TITLE PAGE ====================
    pdf.ln(18)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 11, "Baltimore MTA Transit Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, "A Real-Data Transit Network Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Demonstrating Core Data Structures & Algorithms", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(0, 0, 0)
    info = [
        ("Course", "COSC 320 - Algorithm Design"),
        ("Student", "Aayush Shrestha"),
        ("University", "Morgan State University"),
        ("Date", "March 2026"),
        ("Language", "Python 3.13 with Rich terminal UI"),
        ("GitHub", "github.com/theaayushstha1/transit"),
    ]
    for label, value in info:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(50, 6.5, f"{label}:", align="R")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6.5, f"  {value}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(0, 51, 102)
    pdf.line(50, pdf.get_y(), pdf.w - 50, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 4.5, (
        "This project implements a transit network simulator using real Baltimore MTA data "
        "(Light Rail and Metro SubwayLink, 37 stations). It demonstrates graph traversal "
        "(DFS, BFS), shortest path (Dijkstra's), sorting (Merge Sort, Quick Sort), "
        "searching (Binary, Linear), and queue/stack data structures through an "
        "interactive terminal interface with animated algorithm visualizations."
    ), align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Main menu screenshot on title page
    pdf.inline_image("01_menu", "Interactive main menu with 10 options covering all features", 0.70)

    # ==================== SYSTEM DESIGN (flows from ~page 2) ====================
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
        "|-- main.py                  # Entry point, interactive menu loop\n"
        "|-- models/\n"
        "|   |-- station.py           # Station node class (name, ID, capacity)\n"
        "|   |-- passenger.py         # Passenger class (origin, destination)\n"
        "|   +-- transit_network.py   # Graph (adjacency list representation)\n"
        "|-- algorithms/\n"
        "|   |-- traversal.py         # DFS (recursive) + BFS (queue-based)\n"
        "|   |-- shortest_path.py     # Dijkstra's algorithm (min-heap)\n"
        "|   |-- sorting.py           # Merge Sort + Quick Sort\n"
        "|   +-- searching.py         # Binary Search + Linear Search\n"
        "|-- simulation/\n"
        "|   |-- undo_manager.py      # Stack-based undo (command pattern)\n"
        "|   +-- passenger_sim.py     # Queue-based FIFO boarding\n"
        "|-- data/\n"
        "|   +-- baltimore_mta.py     # Real MTA station data (37 stations)\n"
        "+-- ui/\n"
        "    |-- display.py           # Rich tables, panels, menus\n"
        "    +-- visualizer.py        # Real-time algorithm animations"
    )

    pdf.subsection_title("1.2 Design Decisions")
    pdf.add_table(
        ["Decision", "Choice", "Reasoning"],
        [
            ["Graph repr.", "Adjacency list (dict of dicts)", "O(1) edge lookup, sparse transit graph"],
            ["Edge weights", "Travel time in minutes", "Enables Dijkstra, maps to real MTA data"],
            ["Shared stations", "Dedup by name", "Lexington Market on both lines = 1 node"],
            ["UI library", "Python Rich", "Colored tables, live animations, zero web deps"],
            ["Undo pattern", "Command + inverse actions", "_raw_ methods skip undo stack"],
            ["Sorting key", "Station passenger capacity", "Numeric field with varied values"],
        ],
        col_widths=[32, 54, 99],
    )

    pdf.subsection_title("1.3 Real Baltimore MTA Data")
    pdf.body_text(
        "The simulator uses real Baltimore MTA data: 24 Light Rail stations from Hunt Valley to "
        "Cromwell/Glen Burnie (with BWI Airport spur), 14 Metro SubwayLink stations from Owings "
        "Mills to Johns Hopkins Hospital. Lexington Market serves as the transfer point between "
        "lines, stored as a single shared node with 4 connections. All 37 stations, 36 weighted "
        "edges, travel times of 2-5 minutes."
    )

    # Station table screenshot right after the data description
    pdf.inline_image("03_station_table", "All 37 Baltimore MTA stations with IDs, lines, capacities, and connections", 0.80)

    # ==================== DATA STRUCTURES (flows naturally) ====================
    pdf.section_title("2. Data Structures")

    pdf.subsection_title("2.1 Graph (Adjacency List)")
    pdf.body_text(
        "The transit network is a weighted undirected graph. adj_list[station_id] maps to "
        "{neighbor_id: weight_in_minutes}. This provides O(1) edge lookup and insertion, "
        "optimal for the sparse topology of a transit network (37 nodes, 36 edges)."
    )
    pdf.code_block(
        "class TransitNetwork:\n"
        "    def __init__(self):\n"
        "        self.stations: dict[int, Station] = {}      # ID -> Station\n"
        "        self.adj_list: dict[int, dict[int, float]] = {}  # adjacency list\n"
        "        self.undo_stack: list = []                   # LIFO for undo\n"
        "\n"
        "    def add_connection(self, id1, id2, weight):\n"
        "        self.adj_list[id1][id2] = weight  # undirected: store both\n"
        "        self.adj_list[id2][id1] = weight"
    )

    pdf.subsection_title("2.2 Queue (FIFO) - Passenger Boarding")
    pdf.body_text(
        "Each station has a passenger queue (collections.deque). Passengers enqueue via append() "
        "and dequeue via popleft() during boarding, both O(1). A Python list would be O(n) for "
        "popleft due to element shifting."
    )
    pdf.code_block(
        "station.passenger_queue.append(passenger)       # O(1) enqueue\n"
        "passenger = station.passenger_queue.popleft()    # O(1) dequeue FIFO"
    )

    # Passenger boarding screenshot right here
    pdf.inline_image_half("08_passenger", "Passenger boarding simulation: 50 generated, capacity 30, 20 remain in queue")

    pdf.subsection_title("2.3 Stack (LIFO) - Undo System")
    pdf.body_text(
        "The undo system uses a Python list as a stack (append/pop). Every graph mutation pushes "
        "its inverse action onto the stack. The UndoManager pops and applies inverses using "
        "_raw_ methods that bypass the undo stack to prevent infinite loops."
    )
    pdf.code_block(
        "# Public method records action for undo\n"
        "def add_station(self, station):\n"
        "    self._raw_add_station(station)\n"
        "    self.undo_stack.append({\"action\": \"add_station\", ...})\n"
        "\n"
        "# Undo pops and applies the inverse operation\n"
        "def undo(self):\n"
        "    action = self.network.undo_stack.pop()  # LIFO\n"
        "    if action[\"action\"] == \"add_station\":\n"
        "        self.network._raw_remove_station(action[\"station\"].station_id)"
    )

    # Undo screenshot
    pdf.inline_image_half("09_undo", "Undo system: add station (38 total), then undo restores to 37")

    pdf.subsection_title("2.4 Priority Queue (Min-Heap)")
    pdf.body_text(
        "Dijkstra's algorithm uses Python's heapq as a min-heap priority queue. "
        "Each entry is a (distance, station_id) tuple. heappush/heappop are O(log n), "
        "giving Dijkstra O((V+E) log V) overall."
    )

    # ==================== ALGORITHMS ====================
    pdf.section_title("3. Algorithm Implementations")

    pdf.subsection_title("3.1 Depth-First Search (DFS) - Recursive")
    pdf.body_text(
        "DFS explores as deeply as possible along each branch before backtracking. "
        "Implemented using recursion (the call stack serves as the implicit stack). "
        "Maintains a visited set to avoid cycles and a path list that grows/shrinks via append/pop."
    )
    pdf.code_block(
        "def _dfs_helper(current: int) -> bool:\n"
        "    visited.add(current)\n"
        "    path.append(current)\n"
        "    if current == goal_id: return True\n"
        "    for neighbor_id, _ in sorted(network.get_neighbors(current)):\n"
        "        if neighbor_id not in visited:\n"
        "            if _dfs_helper(neighbor_id): return True\n"
        "    path.pop()  # backtrack on dead end\n"
        "    return False"
    )

    pdf.subsection_title("3.2 Breadth-First Search (BFS) - Queue")
    pdf.body_text(
        "BFS uses collections.deque as a FIFO queue, exploring all neighbors at the current "
        "depth before the next level. Guarantees shortest path in unweighted graphs. Each queue "
        "entry stores the full path for easy reconstruction."
    )
    pdf.code_block(
        "queue = deque([(start_id, [start_id])])\n"
        "while queue:\n"
        "    current, path = queue.popleft()          # FIFO\n"
        "    if current == goal_id: return path\n"
        "    for neighbor_id, _ in sorted(network.get_neighbors(current)):\n"
        "        if neighbor_id not in visited:\n"
        "            visited.add(neighbor_id)\n"
        "            queue.append((neighbor_id, path + [neighbor_id]))"
    )

    pdf.subsection_title("3.3 DFS vs BFS Performance Comparison")
    pdf.body_text(
        "Route from Hunt Valley to Johns Hopkins Hospital: DFS visited all 37 stations "
        "(exhaustive depth-first exploration), while BFS visited only 23 (level-by-level, "
        "terminates as soon as the goal is found). Both found a 17-station path because "
        "the graph is largely linear; in a denser graph BFS would find the shorter path."
    )
    pdf.add_table(
        ["Metric", "DFS (Recursive)", "BFS (Queue)"],
        [
            ["Path Length", "17 stations", "17 stations"],
            ["Nodes Visited", "37 (all)", "23 (early stop)"],
            ["Optimal (unweighted)?", "Not guaranteed", "Yes (fewest edges)"],
            ["Time Complexity", "O(V + E)", "O(V + E)"],
            ["Space Complexity", "O(V) recursion stack", "O(V) queue + paths"],
        ],
        col_widths=[48, 68, 69],
    )

    # DFS vs BFS screenshot
    pdf.inline_image("05_dfs_vs_bfs", "DFS vs BFS comparison showing paths, visit counts, and timing", 0.80)

    pdf.subsection_title("3.4 Dijkstra's Shortest Path Algorithm")
    pdf.body_text(
        "Dijkstra's finds the shortest weighted path using a min-heap priority queue. "
        "It greedily selects the unvisited node with the smallest known distance, then relaxes "
        "its neighbors. The path from Hunt Valley to Johns Hopkins Hospital traverses 17 stations "
        "in 37 minutes total, automatically transferring from Light Rail to Metro at Lexington Market."
    )
    pdf.code_block(
        "while pq:\n"
        "    current_dist, current = heapq.heappop(pq)  # min-heap\n"
        "    if current in visited: continue\n"
        "    visited.add(current)\n"
        "    if current == end_id: break                 # early termination\n"
        "    for neighbor_id, weight in network.get_neighbors(current):\n"
        "        new_dist = current_dist + weight\n"
        "        if new_dist < distances[neighbor_id]:   # relaxation\n"
        "            distances[neighbor_id] = new_dist\n"
        "            previous[neighbor_id] = current\n"
        "            heapq.heappush(pq, (new_dist, neighbor_id))"
    )

    # Dijkstra screenshot
    pdf.inline_image("04_dijkstra", "Dijkstra's shortest path: Hunt Valley to JHH, 17 stations, 37 min, 1 transfer", 0.80)

    # ==================== SORTING + SEARCHING ====================
    pdf.subsection_title("3.5 Merge Sort")
    pdf.body_text(
        "Merge Sort divides the array in half recursively, then merges the sorted halves. "
        "Stable (preserves order of equal elements), always O(n log n), but requires O(n) extra "
        "space. On 37 stations sorted by capacity: 140 comparisons, ~35 microseconds."
    )
    pdf.code_block(
        "def _merge(left, right):\n"
        "    result, i, j = [], 0, 0\n"
        "    while i < len(left) and j < len(right):\n"
        "        comparisons[0] += 1\n"
        "        if key(left[i]) <= key(right[j]):\n"
        "            result.append(left[i]); i += 1\n"
        "        else:\n"
        "            result.append(right[j]); j += 1\n"
        "    result.extend(left[i:]); result.extend(right[j:])\n"
        "    return result"
    )

    pdf.subsection_title("3.6 Quick Sort")
    pdf.body_text(
        "Quick Sort selects a pivot (last element), partitions in-place so smaller elements go "
        "left and larger go right, then recurses on both halves. O(n log n) average, O(n^2) worst "
        "case. Unstable but in-place with O(log n) stack space. On 37 stations: 188 comparisons, "
        "~23 microseconds (faster than Merge Sort despite more comparisons, due to cache locality)."
    )

    pdf.subsection_title("3.7 Sorting Algorithm Comparison")
    pdf.add_table(
        ["Metric", "Merge Sort", "Quick Sort"],
        [
            ["Comparisons (n=37)", "140", "188"],
            ["Measured Time", "~35 us", "~23 us"],
            ["Time Complexity", "O(n log n) always", "O(n log n) avg / O(n^2) worst"],
            ["Space Complexity", "O(n) extra arrays", "O(log n) stack only"],
            ["Stable?", "Yes", "No"],
            ["In-place?", "No", "Yes"],
        ],
        col_widths=[48, 68, 69],
    )

    # Sorting screenshot
    pdf.inline_image("06_sorting", "Merge Sort vs Quick Sort: side-by-side comparison with sorted output", 0.75)

    pdf.subsection_title("3.8 Binary Search vs Linear Search")
    pdf.body_text(
        "Binary Search requires a pre-sorted array and eliminates half the remaining elements "
        "each step (O(log n)). Linear Search scans sequentially from start (O(n)). Searching "
        "for capacity=200 among 37 stations: Binary Search found it in 3 comparisons (~0.3 us) "
        "while Linear Search needed 20 comparisons (~1.2 us)."
    )
    pdf.add_table(
        ["Metric", "Binary Search", "Linear Search"],
        [
            ["Comparisons (target=200)", "3", "20"],
            ["Measured Time", "~0.3 us", "~1.2 us"],
            ["Time Complexity", "O(log n)", "O(n)"],
            ["Space Complexity", "O(1)", "O(1)"],
            ["Requires Sorted Input?", "Yes", "No"],
        ],
        col_widths=[48, 68, 69],
    )

    # Search screenshot
    pdf.inline_image("07_search", "Binary vs Linear Search comparison with found station and metrics", 0.75)

    # ==================== BIG-O ANALYSIS ====================
    pdf.section_title("4. Algorithm Complexity Analysis")

    pdf.body_text(
        "The following table provides the complete theoretical time and space complexity for "
        "every operation implemented in the simulator. These complexities are verified empirically "
        "by the built-in performance dashboard, which runs live benchmarks on the 37-station network."
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
            ["Dijkstra's Algorithm", "O((V+E) log V)", "O(V) distances + heap"],
            ["Merge Sort", "O(n log n) always", "O(n) extra arrays"],
            ["Quick Sort", "O(n log n) avg / O(n^2) worst", "O(log n) stack"],
            ["Binary Search", "O(log n)", "O(1)"],
            ["Linear Search", "O(n)", "O(1)"],
            ["Stack Push/Pop (Undo)", "O(1)", "O(1) per action"],
            ["Queue Enq/Deq (Boarding)", "O(1)", "O(1)"],
        ],
        col_widths=[55, 65, 65],
    )

    pdf.subsection_title("4.1 Empirical Benchmarks")
    pdf.body_text(
        "All algorithms were benchmarked on the full 37-station, 36-edge Baltimore MTA network "
        "using time.perf_counter() for microsecond precision. Sorting and searching algorithms "
        "track exact comparison counts to validate theoretical predictions."
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
        col_widths=[68, 55, 62],
    )

    pdf.body_text(
        "Key observations: (1) BFS visits fewer nodes than DFS by expanding level-by-level and "
        "stopping early. (2) Dijkstra terminates as soon as the target node is popped from the "
        "priority queue. (3) Quick Sort is faster in wall-clock time than Merge Sort despite more "
        "comparisons, because in-place operations have better cache locality and avoid memory "
        "allocation. (4) Binary Search confirms O(log n) with 3 comparisons vs Linear's 20."
    )

    # Performance dashboard screenshot
    pdf.inline_image("10_dashboard", "Performance dashboard: Big-O theory table alongside measured benchmarks", 0.80)

    # ==================== CONCLUSION ====================
    pdf.section_title("5. Conclusion")

    pdf.body_text(
        "This project demonstrates the practical application of core data structures and algorithms "
        "to a real-world transit network. By using actual Baltimore MTA station data (37 stations "
        "across Light Rail and Metro SubwayLink) rather than abstract examples, the project grounds "
        "algorithmic concepts in a tangible, relatable system."
    )

    pdf.body_text("Key takeaways from the implementation:")

    points = [
        ("Graph Representation", "An adjacency list (dict of dicts) provides O(1) edge operations "
         "and naturally models the sparse connectivity of a transit network."),

        ("DFS vs BFS", "BFS guarantees the shortest unweighted path and visits fewer nodes by "
         "expanding level-by-level. DFS explores deeply first. Both run in O(V+E) time, but BFS "
         "is preferable when optimality matters."),

        ("Dijkstra's Algorithm", "The min-heap priority queue enables weighted shortest path in "
         "O((V+E) log V). Cross-line routing through Lexington Market demonstrates real transfers."),

        ("Sorting", "Merge Sort's guaranteed O(n log n) and stability come at the cost of O(n) "
         "space. Quick Sort's in-place operation gives better cache performance despite O(n^2) worst case."),

        ("Searching", "Binary Search's O(log n) dramatically outperforms Linear Search's O(n), "
         "confirmed empirically with 3 vs 20 comparisons on 37 stations."),

        ("Queue/Stack", "The deque-based passenger queue and list-based undo stack demonstrate "
         "fundamental FIFO/LIFO patterns with O(1) operations per action."),
    ]

    for i, (label, detail) in enumerate(points, 1):
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(5, 4.2, f"{i}.")
        pdf.cell(0, 4.2, f" {label}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(0, 4.2, f"   {detail}")
        pdf.ln(0.8)

    pdf.ln(2)
    pdf.body_text(
        "The Rich terminal UI elevates the project with animated algorithm visualizations and a "
        "performance dashboard that bridges Big-O theory with measured benchmarks, reinforcing "
        "that algorithmic analysis accurately predicts real-world behavior."
    )

    # ==================== FUTURE ENHANCEMENTS ====================
    pdf.section_title("6. Future Enhancements")

    enhancements = [
        ("A* Search Algorithm", "Implement A* with a heuristic based on geographic distance "
         "between stations. This would combine Dijkstra's optimality guarantee with faster "
         "convergence by prioritizing stations closer to the destination."),

        ("Real-Time Schedule Integration", "Connect to the MTA GTFS feed to incorporate actual "
         "departure times, allowing the simulator to compute shortest paths that account for "
         "wait times at transfer stations."),

        ("Interactive Graph Visualization", "Add a matplotlib or networkx-based visual map that "
         "renders the transit network as a graph with nodes and edges, color-coded by line, with "
         "animated pathfinding overlays."),

        ("Multi-Source Shortest Paths", "Implement Floyd-Warshall or run Dijkstra from every "
         "station to precompute an all-pairs shortest path matrix, enabling O(1) route queries."),

        ("Load Balancing Simulation", "Extend the passenger simulation to model rush-hour "
         "overcrowding, with passengers rerouting when a station reaches capacity, demonstrating "
         "graph algorithms in a dynamic environment."),
    ]

    for i, (title, desc) in enumerate(enhancements, 1):
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.cell(5, 4.2, f"{i}.")
        pdf.cell(0, 4.2, f" {title}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 8.5)
        pdf.multi_cell(0, 4.2, f"   {desc}")
        pdf.ln(0.8)

    pdf.ln(2)

    # ==================== REFERENCES ====================
    pdf.section_title("References")

    refs = [
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). "
        "Introduction to Algorithms (4th ed.). MIT Press.",
        "Baltimore MTA. Maryland Transit Administration System Map. mta.maryland.gov",
        "Python Software Foundation. collections.deque, heapq documentation. docs.python.org",
        "Will McGugan. Rich: Python library for rich text in terminal. github.com/Textualize/rich",
    ]
    pdf.set_font("Helvetica", "", 8)
    for i, ref in enumerate(refs, 1):
        pdf.cell(7, 4.5, f"[{i}]")
        pdf.multi_cell(0, 4.5, ref)
        pdf.ln(0.5)

    # Save
    output_path = "report.pdf"
    pdf.output(output_path)
    print(f"Report generated: {output_path} ({pdf.page_no()} pages)")
    return output_path


if __name__ == "__main__":
    build_report()
