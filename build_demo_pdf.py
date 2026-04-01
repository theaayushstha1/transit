"""Convert SVG screenshots to PNG and compile into a demo PDF."""

import cairosvg
import os
from fpdf import FPDF

screenshots_dir = "screenshots"
os.makedirs(f"{screenshots_dir}/png", exist_ok=True)

# Convert SVGs to PNGs
demos = [
    ("01_menu", "Main Menu"),
    ("02_network_map", "Network Map - Real Baltimore MTA Data"),
    ("03_station_table", "All 37 Stations"),
    ("04_dijkstra", "Dijkstra's Shortest Path - Cross-Line Routing"),
    ("05_dfs_vs_bfs", "DFS vs BFS Comparison"),
    ("06_sorting", "Merge Sort vs Quick Sort"),
    ("07_search", "Binary Search vs Linear Search"),
    ("08_passenger", "Passenger Boarding Simulation (Queue/FIFO)"),
    ("09_undo", "Undo System (Stack/LIFO)"),
    ("10_dashboard", "Performance Dashboard - Theory + Benchmarks"),
]

print("Converting SVGs to PNGs...")
for filename, _ in demos:
    svg_path = f"{screenshots_dir}/{filename}.svg"
    png_path = f"{screenshots_dir}/png/{filename}.png"
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2)
    print(f"  {filename}.png")

# Build PDF
print("\nBuilding demo PDF...")

class DemoPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

pdf = DemoPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=15)

# Title page
pdf.add_page()
pdf.ln(40)
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(0, 51, 102)
pdf.cell(0, 14, "Baltimore MTA Transit Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)
pdf.set_font("Helvetica", "", 16)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, "Demo Screenshots", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
pdf.set_font("Helvetica", "", 12)
pdf.cell(0, 8, "COSC 320 - Algorithm Design", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "Aayush Shrestha | Morgan State University", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(20)
pdf.set_draw_color(0, 51, 102)
pdf.line(50, pdf.get_y(), pdf.w - 50, pdf.get_y())
pdf.ln(10)
pdf.set_font("Helvetica", "I", 10)
pdf.set_text_color(80, 80, 80)
pdf.multi_cell(0, 5.5, (
    "The following pages show actual terminal output from the simulator, "
    "captured using Rich's SVG export. The simulator uses real Baltimore MTA "
    "station data and demonstrates graph traversal (DFS, BFS), shortest path "
    "(Dijkstra), sorting (Merge Sort, Quick Sort), searching (Binary, Linear), "
    "queue-based passenger boarding, and stack-based undo operations."
), align="C")

# Screenshot pages
for filename, title in demos:
    pdf.add_page()
    png_path = f"{screenshots_dir}/png/{filename}.png"

    # Title
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(0, 51, 102)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)

    # Image - fit to page width with some margin
    img_width = pdf.w - pdf.l_margin - pdf.r_margin
    try:
        pdf.image(png_path, x=pdf.l_margin, w=img_width)
    except Exception as e:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 10, f"Error loading image: {e}", new_x="LMARGIN", new_y="NEXT")

output_path = "demo_screenshots.pdf"
pdf.output(output_path)
print(f"\nDone! Demo PDF: {output_path} ({pdf.page_no()} pages)")
