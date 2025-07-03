# **OTDR SOR Parser and Visualizer Documentation**

## Overview

This module provides functionality to parse `.sor`, `.msor`, and `.csv` OTDR trace files, extract signal data, plot signals, save parsed output, and identify signal peaks for analysis. It is useful for handling fiber optic test data and generating visualizations.

---

## **Module-Level Constants**

```python
accepted_parsing_headers: Tuple[str, ...] = (".sor", ".msor", ".csv")
accepted_saving_headers: Tuple[str, ...] = (".csv", ".tsv")
```

* `accepted_parsing_headers`: File extensions supported for parsing.
* `accepted_saving_headers`: File extensions supported for saving/exporting data.

---

## **Helper Function**

### `grab_name(data: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]`

Searches a list of dictionaries for a dictionary with the specified name.

---

## **Class: SOR**

### `__init__(file_path: str)`

Initializes a `SOR` object and reads OTDR trace data from `.sor`, `.msor`, or `.csv` file.

---

### `_validate_file()`

Internal method to check:

* The file exists.
* The file extension is supported.

---

### `_parse_file()`

Dispatches to appropriate parsing method based on file extension.

---

### `_parse_sor()`

Parses `.sor` or `.msor` binary file using the `otdrparser` module.

---

### `_parse_csv()`

Parses `.csv` file expected to contain `Distance` and `Backscatter` columns.

---

### `extract_axis(adjust: bool = False)`

Extracts the X and Y axis signal data from the raw readings.

**Parameters:**

* `adjust`: If `True`, normalize Y-axis data to start from zero.

---

### `dump(file_name: str)`

Exports parsed data (`X`, `Y`) into `.csv` or `.tsv` file formats.

**Parameters:**

* `file_name`: Name of output file (must end with `.csv` or `.tsv`).

---

### `dump_all(file_name: str)`

Dumps raw parsed metadata into a text file.

**Parameters:**

* `file_name`: File where raw metadata is saved.

---

### `plot(file_name: str, vertical_lines: dict = {})`

Creates and saves a static plot using `matplotlib`.

**Parameters:**

* `file_name`: Path to save the image (PNG, PDF, etc.).
* `vertical_lines`: Dictionary of `{label: [x_pos]}` for marking events.

---

### `interactive_plot(...) -> go.Figure`

Generates an interactive Plotly figure of the signal.

**Parameters:**

* `title`: Title of the plot.
* `xaxis_title`: X-axis label.
* `yaxis_title`: Y-axis label.
* `vertical_lines`: Optional dictionary `{label: x_pos}`.
* `show`: Whether to show the plot immediately.
* `save_path`: Optional path to save plot as HTML.

**Returns:**

* `plotly.graph_objects.Figure`

---

### `classify_reflections(...) -> Tuple[Optional[int], Optional[int]]`

Detects signal peaks and classifies them based on file type.

**Parameters:**

* `file_type`: Either `'E'` or `'C'` to determine classification rules.
* `x_range`: (min\_x, max\_x) range to restrict peak detection.
* `prominence`: Required prominence of peaks.
* `height_threshold`: Minimum height of peaks.

**Returns:**

* A tuple of `(peak_x, peak_y)` representing peak location and value.

**Raises:**

* `ValueError` if an unsupported `file_type` is provided.

---

## **Function: bulk**

```python
def bulk(directory: str, filter: callable = lambda x: True)
```

Iterates over files in a directory and yields parsed `SOR` objects that satisfy the provided filter.

**Parameters:**

* `directory`: Path to the directory containing trace files.
* `filter`: Callable to filter filenames. Defaults to accepting all.

**Yields:**

* `SOR` object for each matching file.

---

## **Dependencies**

* `pandas`
* `numpy`
* `scipy`
* `matplotlib`
* `plotly`
* `otdrparser` (external library)
* Custom modules: `dump_csv`, `dump_tsv`
