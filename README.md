
# SOR File Parser and Visualizer

A Python package for parsing SOR/MSOR files (OTDR traces) and CSV files containing X,Y data points, with visualization capabilities.

## Features

- Parse `.sor` and `.msor` files using `otdrparser`
- Parse CSV files with X,Y data points
- Extract and process X,Y data with optional zero-centering adjustment
- Export processed data to CSV or TSV formats
- Generate static plots using matplotlib
- Create interactive visualizations using Plotly

## Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:
   ```bash
   pip install otdrparser matplotlib plotly
   ```

## Usage

### Basic Usage

```python
from sor_parser import SOR

# Initialize with a file
sor = SOR("trace.sor")  # or "data.csv"

# Extract X,Y data (optionally center Y values around zero)
sor.extract_axis(adjust=True)

# Export to CSV/TSV
sor.dump("output.csv")

# Generate static plot
sor.plot("plot.png")

# Create interactive plot
sor.interactive_plot(
    title="My OTDR Trace",
    vertical_lines={"Event1": 1250.3, "Fault": 3456.7},
    save_path="interactive_plot.html"
)
```

### File Format Support

**Input Formats:**
- `.sor` - Standard OTDR binary format
- `.msor` - Modified SOR format
- `.csv` - Comma-separated X,Y values (with optional header)

**Output Formats:**
- `.csv` - Comma-separated output
- `.tsv` - Tab-separated output
- `.png` - Static plot image (via matplotlib)
- `.html` - Interactive plot (via Plotly)

## API Reference

### `SOR(file_path: str)`
Main class for parsing and processing files.

**Methods:**
- `extract_axis(adjust: bool = False)` - Extract X,Y data points
- `dump(file_name: str)` - Export data to file
- `plot(file_name: str)` - Generate static plot
- `interactive_plot()` - Create interactive visualization

## Examples

### Basic Processing
```python
sor = SOR("data.sor")
sor.extract_axis(adjust=True)
sor.dump("processed_data.tsv")
```

### Advanced Plotting
```python
fig = sor.interactive_plot(
    title="Network Fiber Inspection",
    xaxis_title="Distance Along Fiber (m)",
    yaxis_title="Signal Loss (dB)",
    vertical_lines={
        "Splice": 1250.3,
        "Connector": 3456.7,
        "Fault": 5021.1
    },
    save_path="fiber_inspection.html"
)
```

## License

[MIT License](LICENSE)
