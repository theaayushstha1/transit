# Baltimore MTA Transit Simulator

A real-data transit network simulator demonstrating core data structures and algorithms using Baltimore's Light Rail and Metro SubwayLink systems (37 stations).

**Course:** COSC 320 - Algorithm Design | Morgan State University

## Features

- **Graph (Adjacency List)** with add/remove stations and connections
- **DFS** (recursive) and **BFS** (queue-based) traversal with animated comparison
- **Dijkstra's Algorithm** for weighted shortest path with cross-line transfers
- **Merge Sort** and **Quick Sort** with comparison counting
- **Binary Search** and **Linear Search** with performance comparison
- **Passenger Queue** (FIFO) simulation with boarding animation
- **Undo Stack** (LIFO) using command pattern with inverse actions
- **Performance Dashboard** with Big-O theory and live benchmarks

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Project Structure

```
models/          Station, Passenger, TransitNetwork (graph)
algorithms/      DFS, BFS, Dijkstra, sorting, searching
simulation/      Passenger queue, undo stack
data/            Real Baltimore MTA station data
ui/              Rich terminal display and animations
```

## Algorithm Complexity

| Operation | Time | Space |
|-----------|------|-------|
| DFS / BFS | O(V+E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Merge Sort | O(n log n) | O(n) |
| Quick Sort | O(n log n) avg | O(log n) |
| Binary Search | O(log n) | O(1) |
| Linear Search | O(n) | O(1) |
