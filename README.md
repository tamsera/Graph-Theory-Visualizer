# Graph Theory Visualizer

An interactive graph theory visualization and analysis tool developed in Python using Tkinter and NetworkX.

## Features

- Automatic planar graph visualization
- Randomized graph layouts
- Euler path detection with complete traversal
- Euler circuit detection with complete traversal
- Hamiltonian cycle detection with vertex sequence (up to 12 vertices)
- Bridge detection
- Articulation point detection
- Vertex degree calculation
- Spanning tree visualization
- Planar region counting using Euler's formula
- Interactive checkboxes and results console

## Requirements

- Python 3.10+
- NetworkX
- Tkinter

Install the required package:

```bash
pip install networkx
```

## Usage

Run the application:

```bash
python GRAF.py
```

Enter graph edges separated by commas:

```text
AB, AC, AE, BC, BD, BE, CE, CD, DE, DF, EF
```

Click **START** to generate a planar graph layout.

Select the graph theory properties you want to analyze. Results, including complete Euler and Hamiltonian traversal sequences when available, will appear in the console.

## Technologies

- Python
- Tkinter
- NetworkX

## License

MIT License
