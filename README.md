# viSOR

A Python parser to read, process, and export Optical Time-Domain Reflectometer (OTDR) data from .sor and .msor files into CSV or TSV formats.
Features

    Parse .sor and .msor OTDR raw data files using otdrparser.

    Extract and center X (distance) and Y (signal) axis data.

    Export parsed data to CSV or TSV files.

    Simple API with validation of input and output file types.

# Installation

Make sure you have the otdrparser package installed and other dependencies:

``` bash
pip install otdrparser
```

# Usage

```py
from viSOR import Parser

# Initialize the parser with an OTDR file path (.sor or .msor)
parser = Parser("example.sor")

# Extract X and Y axes data, optionally center the Y values around zero
parser.extract_axis(adjust=True)

# Dump the processed data to a CSV or TSV file
parser.dump("output.csv")

```
# API Reference

## Parser(file_path: str)

    Initializes the parser by loading and parsing the OTDR file.

    Validates that the file exists and has a supported extension.

## extract_axis(adjust: bool = False) -> None

    Extracts X and Y axis data from the parsed raw readings.

    If adjust=True, centers the Y values by subtracting the first Y value.

## dump(file_name: str) -> None

    Saves the parsed and processed data into the specified file.

    Supports .csv and .tsv formats.

    Raises an exception for unsupported output file types.

## Supported File Extensions

    Input: .sor, .msor

    Output: .csv, .tsv

# Dependencies

    otdrparser

    Python standard libraries: os.path, typing

# License

MIT License

Copyright (c) 2025 Euan Baldwin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
