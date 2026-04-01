"""
Generate the 8-10 page PDF report for Baltimore MTA Transit Simulator.
COSC 320 - Algorithm Design
"""

import os
from fpdf import FPDF

SCREENSHOTS_DIR = "screenshots/png"


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
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 51, 102)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 51, 102)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def subsection_title(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(51, 51, 51)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 4.8, text)
        self.ln(1.5)

    def code_block(self, code):
        self.set_font("Courier", "", 7.5)
        self.set_fill_color(240, 240, 240)
        self.set_draw_color(200, 200, 200)
        y = self.get_y()
        lines = code.strip().split("\n")
        block_height = len(lines) * 3.8 + 3
        if y + block_height > self.h - 22:
            self.add_page()
            y = self.get_y()
        self.rect(self.l_margin, y, self.w - self.l_margin - self.r_margin, block_height, "FD")
        self.set_xy(self.l_margin + 2, y + 1.5)
        for line in lines:
            self.cell(0, 3.8, line)
            self.ln(3.8)
        self.ln(3)
        self.set_font("Helvetica", "", 9)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            available = self.w - self.l_margin - self.r_margin
            col_widths = [available / len(headers)] * len(headers)

        needed = 6 * (len(rows) + 1) + 3
        if self.get_y() + needed > self.h - 22:
            self.add_page()

        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6, h, border=1, fill=True, align="C")
        self.ln()

        self.set_font("Helvetica", "", 8)
        self.set_text_color(0, 0, 0)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell in enumerate(row):
                align = "L" if i == 0 else "C"
                self.cell(col_widths[i], 6, str(cell), border=1, fill=True, align=align)
            self.ln()
            fill = not fill
        self.ln(3)

    def screenshot_grid(self, images, title=None):
        """Place 2-4 screenshots in a grid on the current page."""
        if title:
            self.section_title(title)

        usable_w = self.w - self.l_margin - self.r_margin
        gap = 4
        img_w = (usable_w - gap) / 2

        for idx, (path, caption) in enumerate(images):
            col = idx % 2
            if idx > 0 and col == 0:
                self.ln(2)

            x = self.l_margin + col * (img_w + gap)
            y = self.get_y()

            # Caption
            self.set_xy(x, y)
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(0, 51, 102)
            self.cell(img_w, 5, caption, align="C")
            self.set_text_color(0, 0, 0)

            # Image
            try:
                self.image(path, x=x, y=y + 5, w=img_w)
            except Exception:
                self.set_xy(x, y + 5)
                self.set_font("Helvetica", "I", 8)
                self.cell(img_w, 10, f"[{caption}]", align="C")

            if col == 1:
                # Move below the taller image (estimate)
                self.set_y(y + img_w * 0.55 + 8)


def build_report():
    pdf = Report()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ==================== PAGE 1: TITLE ====================
    pdf.ln(25)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, "Baltimore MTA Transit Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "A Real-Data Transit Network Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Demonstrating Core Data Structures & Algorithms", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font("Helvetica", "", 12)
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
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(50, 7, f"{label}:", align="R")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, f"  {value}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    pdf.set_draw_color(0, 51, 102)
    pdf.line(50, pdf.get_y(), pdf.w - 50, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 5, (
        "This project implements a transit network simulator using real Baltimore MTA data "
        "(Light Rail and Metro SubwayLink, 37 stations). It demonstrates graph traversal "
        "(DFS, BFS), shortest path (Dijkstra's), sorting (Merge Sort, Quick Sort), "
        "searching (Binary, Linear), and queue/stack data structures through an "
        "interactive terminal interface with animated algorithm visualizations."
    ), align="C")

    # Screenshot: Main Menu below the abstract
    menu_png = f"{SCREENSHOTS_DIR}/01_menu.png"
    if os.path.isfile(menu_png):
        pdf.ln(4)
        img_w = pdf.w - pdf.l_margin - pdf.r_margin - 40
        pdf.image(menu_png, x=pdf.l_margin + 20, w=img_w)

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
            ["Graph repr.", "Adjacency list (dict of dicts)", "O(1) edge lookup, sparse transit graph"],
            ["Edge weights", "Travel time in minutes", "Enables Dijkstra, maps to real MTA data"],
            ["Shared stations", "Dedup by name", "Lexington Market on both lines = 1 node"],
            ["UI library", "Python Rich", "Colored tables, live animations, zero web deps"],
            ["Undo pattern", "Command + inverse", "_raw_ methods skip undo stack"],
            ["Sorting key", "Station capacity", "Numeric field with varied values"],
        ],
        col_widths=[32, 55, 98],
    )

    # ==================== PAGE 3: DATA STRUCTURES ====================
    pdf.add_page()
    pdf.section_title("2. Data Structures")

    pdf.subsection_title("2.1 Graph (Adjacency List)")
    pdf.body_text(
        "The transit network is a weighted undirected graph using an adjacency list (dict of dicts). "
        "adj_list[station_id] maps to {neighbor_id: weight_in_minutes}. This provides O(1) edge "
        "lookup and insertion, optimal for the sparse topology (37 nodes, 36 edges)."
    )
    pdf.code_block(
        "class TransitNetwork:\n"
        "    def __init__(self):\n"
        "        self.stations: dict[int, Station] = {}\n"
        "        self.adj_list: dict[int, dict[int, float]] = {}\n"
        "        self.undo_stack: list = []\n"
        "\n"
        "    def add_connection(self, id1, id2, weight):\n"
        "        self.adj_list[id1][id2] = weight  # undirected\n"
        "        self.adj_list[id2][id1] = weight  # store both"
    )

    pdf.subsection_title("2.2 Queue (FIFO - Passenger Boarding)")
    pdf.body_text(
        "Each station maintains a passenger queue using collections.deque. Passengers are "
        "enqueued (append) and dequeued (popleft) during boarding in FIFO order. "
        "deque provides O(1) for both operations vs O(n) for list.pop(0)."
    )
    pdf.code_block(
        "station.passenger_queue.append(passenger)       # enqueue\n"
        "passenger = station.passenger_queue.popleft()    # dequeue FIFO"
    )

    pdf.subsection_title("2.3 Stack (LIFO - Undo System)")
    pdf.body_text(
        "The undo system uses a Python list as a stack (append/pop). Every graph mutation "
        "pushes its inverse action. The UndoManager pops and applies the inverse using "
        "internal _raw_ methods that bypass the undo stack to prevent infinite loops."
    )
    pdf.code_block(
        "# Public method pushes to undo stack\n"
        "def add_station(self, station):\n"
        "    self._raw_add_station(station)\n"
        "    self.undo_stack.append({\"action\": \"add_station\", ...})\n"
        "\n"
        "# Undo pops and applies inverse\n"
        "def undo(self):\n"
        "    action = self.network.undo_stack.pop()\n"
        "    if action[\"action\"] == \"add_station\":\n"
        "        self.network._raw_remove_station(action[\"station\"].id)"
    )

    pdf.subsection_title("2.4 Priority Queue (Min-Heap)")
    pdf.body_text(
        "Dijkstra's uses Python's heapq as a min-heap priority queue. Each entry is a "
        "(distance, station_id) tuple. heappush/heappop operate in O(log n), giving "
        "Dijkstra O((V+E) log V) time complexity."
    )

    # Network map screenshot
    net_png = f"{SCREENSHOTS_DIR}/02_network_map.png"
    if os.path.isfile(net_png):
        pdf.ln(2)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 4, "Network Map - 37 Baltimore MTA Stations", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0, 0, 0)
        img_w = pdf.w - pdf.l_margin - pdf.r_margin - 20
        pdf.image(net_png, x=pdf.l_margin + 10, w=img_w)

    # ==================== PAGE 4: ALGORITHMS ====================
    pdf.add_page()
    pdf.section_title("3. Algorithm Implementations")

    pdf.subsection_title("3.1 Depth-First Search (DFS) - Recursive")
    pdf.body_text(
        "DFS explores as deeply as possible along each branch before backtracking. Uses "
        "recursion (call stack), a visited set, and a path list that grows/shrinks via append/pop."
    )
    pdf.code_block(
        "def _dfs_helper(current: int) -> bool:\n"
        "    visited.add(current)\n"
        "    path.append(current)\n"
        "    if current == goal_id: return True\n"
        "    for neighbor_id, _ in sorted(network.get_neighbors(current)):\n"
        "        if neighbor_id not in visited:\n"
        "            if _dfs_helper(neighbor_id): return True\n"
        "    path.pop()  # backtrack\n"
        "    return False"
    )

    pdf.subsection_title("3.2 Breadth-First Search (BFS) - Queue")
    pdf.body_text(
        "BFS uses collections.deque as a queue, exploring all neighbors at current depth "
        "before the next level. Guarantees shortest path in unweighted graphs."
    )
    pdf.code_block(
        "queue = deque([(start_id, [start_id])])\n"
        "while queue:\n"
        "    current, path = queue.popleft()\n"
        "    if current == goal_id: return path\n"
        "    for neighbor_id, _ in sorted(network.get_neighbors(current)):\n"
        "        if neighbor_id not in visited:\n"
        "            visited.add(neighbor_id)\n"
        "            queue.append((neighbor_id, path + [neighbor_id]))"
    )

    pdf.subsection_title("3.3 DFS vs BFS Comparison")
    pdf.body_text(
        "Route from Hunt Valley to Johns Hopkins Hospital: DFS visited all 37 stations "
        "(exhaustive depth-first), BFS visited only 23 (level-by-level, stops early)."
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
        col_widths=[50, 67, 68],
    )

    pdf.subsection_title("3.4 Dijkstra's Shortest Path")
    pdf.body_text(
        "Finds the shortest weighted path using a min-heap priority queue. Greedily selects "
        "the unvisited node with smallest known distance, then relaxes neighbors. Hunt Valley "
        "to Johns Hopkins Hospital: 17 stations, 37 minutes, transfers at Lexington Market."
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

    # ==================== PAGE 5: SORTING + SEARCHING ====================
    pdf.add_page()
    pdf.subsection_title("3.5 Merge Sort")
    pdf.body_text(
        "Divides array in half recursively, merges sorted halves. Stable, always O(n log n), "
        "but O(n) extra space. On 37 stations by capacity: 140 comparisons."
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
        "    result.extend(left[i:])\n"
        "    result.extend(right[j:])\n"
        "    return result"
    )

    pdf.subsection_title("3.6 Quick Sort")
    pdf.body_text(
        "Selects pivot (last element), partitions in-place, recurses. O(n log n) avg, "
        "O(n^2) worst. Unstable but in-place (O(log n) stack). 188 comparisons on 37 stations."
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
        col_widths=[50, 67, 68],
    )
    pdf.body_text(
        "Quick Sort was faster in practice despite more comparisons due to in-place "
        "operations and better cache locality. Merge Sort guarantees O(n log n) worst case."
    )

    pdf.subsection_title("3.8 Binary Search vs Linear Search")
    pdf.body_text(
        "Binary Search eliminates half per step (O(log n), requires sorted input). "
        "Linear Search scans sequentially (O(n)). Searching capacity=200 among 37 stations:"
    )
    pdf.add_table(
        ["Metric", "Binary Search", "Linear Search"],
        [
            ["Comparisons", "3", "20"],
            ["Time Complexity", "O(log n)", "O(n)"],
            ["Requires Sorted?", "Yes", "No"],
        ],
        col_widths=[50, 67, 68],
    )

    # ==================== PAGE 6: BIG-O ANALYSIS ====================
    pdf.add_page()
    pdf.section_title("4. Algorithm Complexity Analysis")

    pdf.body_text(
        "Complete time and space complexity for every operation in the simulator, "
        "verified empirically by the performance dashboard."
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
        "Benchmarked on the full 37-station, 36-edge Baltimore MTA network using "
        "time.perf_counter() for microsecond precision."
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
        "Key observations: (1) BFS visits fewer nodes than DFS by expanding level-by-level. "
        "(2) Dijkstra terminates early when target is reached. "
        "(3) Quick Sort beats Merge Sort in practice due to cache-friendly in-place ops. "
        "(4) Binary Search: 3 comparisons vs Linear's 20, confirming O(log n) vs O(n)."
    )

    # ==================== PAGES 7-8: SCREENSHOTS ====================
    screenshots_page1 = [
        ("04_dijkstra", "Dijkstra's Shortest Path"),
        ("05_dfs_vs_bfs", "DFS vs BFS Comparison"),
        ("03_station_table", "All 37 Stations"),
        ("06_sorting", "Merge Sort vs Quick Sort"),
    ]
    screenshots_page2 = [
        ("07_search", "Binary vs Linear Search"),
        ("08_passenger", "Passenger Boarding (Queue)"),
        ("09_undo", "Undo System (Stack)"),
        ("10_dashboard", "Performance Dashboard"),
    ]

    for page_screenshots, page_title in [
        (screenshots_page1, "5. Screenshots"),
        (screenshots_page2, "5. Screenshots (continued)"),
    ]:
        pdf.add_page()
        pdf.section_title(page_title)

        usable_w = pdf.w - pdf.l_margin - pdf.r_margin
        gap = 5
        img_w = (usable_w - gap) / 2
        # Estimate image height based on aspect ratio of terminal screenshots (~0.5)
        img_h = img_w * 0.52

        for idx, (filename, caption) in enumerate(page_screenshots):
            png_path = f"{SCREENSHOTS_DIR}/{filename}.png"
            if not os.path.isfile(png_path):
                continue

            col = idx % 2
            if idx == 2:
                # Move to second row
                pdf.ln(2)

            row_y = pdf.get_y()
            x = pdf.l_margin + col * (img_w + gap)

            # Caption above image
            pdf.set_xy(x, row_y)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(0, 51, 102)
            pdf.cell(img_w, 4, caption, align="C")
            pdf.set_text_color(0, 0, 0)

            # Image
            try:
                pdf.image(png_path, x=x, y=row_y + 4, w=img_w, h=img_h)
            except Exception:
                pass

            if col == 1:
                pdf.set_y(row_y + img_h + 8)

    # ==================== PAGE 9: CONCLUSION ====================
    pdf.add_page()
    pdf.section_title("6. Conclusion")

    pdf.body_text(
        "This project demonstrates the practical application of core data structures and "
        "algorithms to a real-world transit network. By using actual Baltimore MTA station data "
        "(37 stations across Light Rail and Metro SubwayLink) rather than abstract examples, "
        "the project grounds algorithmic concepts in a tangible system."
    )

    pdf.body_text("Key takeaways:")

    points = [
        "Graph: An adjacency list (dict of dicts) provides O(1) edge operations and "
        "naturally models the sparse connectivity of a transit network.",

        "DFS vs BFS: BFS guarantees the shortest unweighted path and typically visits fewer "
        "nodes, while DFS explores deeply first. Both run in O(V+E) time.",

        "Dijkstra: The min-heap priority queue enables weighted shortest path in "
        "O((V+E) log V). Cross-line routing through Lexington Market demonstrates real transfers.",

        "Sorting: Merge Sort's guaranteed O(n log n) and stability costs O(n) space. "
        "Quick Sort's in-place operation gives better cache performance despite O(n^2) worst case.",

        "Searching: Binary Search's O(log n) dramatically outperforms Linear Search's O(n), "
        "confirmed with 3 vs 20 comparisons on 37 stations.",

        "Queue/Stack: The deque-based passenger queue and list-based undo stack demonstrate "
        "fundamental FIFO/LIFO patterns with O(1) operations.",
    ]

    for i, point in enumerate(points, 1):
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(7, 4.8, f"{i}.")
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 4.8, point)
        pdf.ln(1)

    pdf.ln(3)
    pdf.body_text(
        "The Rich terminal UI elevates the project with animated algorithm visualizations "
        "and a performance dashboard that bridges Big-O theory with measured benchmarks, "
        "reinforcing that algorithmic analysis predicts real-world behavior."
    )

    pdf.body_text(
        "The simulator uses real Baltimore MTA data: 24 Light Rail stations from Hunt Valley "
        "to Cromwell/Glen Burnie (with BWI Airport spur), 14 Metro stations from Owings Mills "
        "to Johns Hopkins Hospital, connected at Lexington Market. All 37 stations with 36 "
        "weighted edges and travel times of 2-5 minutes."
    )

    # ==================== PAGE 10: REFERENCES ====================
    pdf.ln(4)
    pdf.section_title("References")

    refs = [
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). "
        "Introduction to Algorithms (4th ed.). MIT Press.",
        "Baltimore MTA. Maryland Transit Administration System Map. mta.maryland.gov",
        "Python Software Foundation. collections.deque, heapq documentation. docs.python.org",
        "Will McGugan. Rich: Python library for rich text in terminal. github.com/Textualize/rich",
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
