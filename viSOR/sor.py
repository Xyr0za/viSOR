from os.path import isfile
import os


from typing import List, Tuple, Dict, Any
import csv
import otdrparser
from .dump import dump_csv, dump_tsv

from matplotlib import pyplot as plt

accepted_parsing_headers: Tuple[str, ...] = (".sor", ".msor", ".csv")
accepted_saving_headers: Tuple[str, ...] = (".csv", ".tsv")



def grab_name(data, name):

    for item in data:
        if item["name"] == name:
            return item

    return None



class SOR:
    def __init__(self, file_path: str) -> None:
        """
        Initializes the SOR object with data from either SOR or CSV files.
        """
        self.file_path: str = file_path
        self.file_header = '.' + file_path.split(".")[-1].lower()
        self.raw: List[Dict[str, Any]] = []
        self.raw_readings: List[Tuple[float, float]] = []
        self.X: List[float] = []
        self.Y: List[float] = []
        self.C: float = 0.0

        self._validate_file()
        self._parse_file()

    def _validate_file(self) -> None:
        """Validate file existence and extension."""
        assert self.file_header in accepted_parsing_headers, f"Unsupported file type: {self.file_header}"
        assert isfile(self.file_path), f"File not found: {self.file_path}"

    def _parse_file(self) -> None:
        """Parse the file based on its type."""
        if self.file_header in (".sor", ".msor"):
            self._parse_sor()
        elif self.file_header == ".csv":
            self._parse_csv()

    def _parse_sor(self) -> None:
        """Parse SOR/MSOR file using otdrparser."""
        with open(self.file_path, 'rb') as fp:
            self.raw = otdrparser.parse(fp)
        self.raw_readings = grab_name(self.raw, "DataPts")["data_points"]

    def _parse_csv(self) -> None:
        """Parse CSV file with X,Y data points."""
        with open(self.file_path, 'r') as fp:
            reader = csv.reader(fp)
            # Skip header if exists
            try:
                float(next(reader)[0])
                fp.seek(0)  # Reset if first value is numeric
            except (ValueError, StopIteration):
                pass  # Header exists or empty file

            self.raw_readings = []
            for row in reader:
                if len(row) >= 2:
                    try:
                        x = float(row[0])
                        y = float(row[1])
                        self.raw_readings.append((x, y))
                    except ValueError:
                        continue  # Skip non-numeric rows

    def extract_axis(self, adjust: bool = False) -> None:
        """
        Extracts X and Y axes from the raw readings.

        :param adjust: If True, center the Y values around zero.
        """
        if adjust and self.raw_readings:
            self.C = self.raw_readings[0][1]
        else:
            self.C = 0.0

        self.X = [data_p[0] for data_p in self.raw_readings]
        self.Y = [data_p[1] - self.C for data_p in self.raw_readings]

    def dump(self, file_name: str) -> None:
        """
        Dumps the parsed and processed data to a file.

        :param file_name: The target filename to dump the data into.
        """
        file_header = '.' + file_name.split(".")[-1].lower()
        assert file_header in accepted_saving_headers, f"Unsupported output format: {file_header}"

        if file_header == ".csv":
            dump_csv(file_name, self)
        elif file_header == ".tsv":
            dump_tsv(file_name, self)

    def plot(self, file_name: str) -> None:
        """
        Plots the current raw readings

        :param file_name:
        :return:
        """

        os.makedirs(
            '/'.join(file_name.split("/")[:-1])
        , exist_ok=True)

        plt.figure(figsize=(10, 6))

        # Plot signal line
        plt.plot(self.X, self.Y, label="Signal", color='tab:blue', linewidth=2)

        # Titles and labels
        plt.title(f"Attenuation vs Distance | {file_name}", fontsize=16, weight='bold')
        plt.xlabel("Distance (m)", fontsize=14)
        plt.ylabel("Attenuation (dB/km)", fontsize=14)

        # Add grid and legend
        plt.grid(visible=True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12, loc='best')

        # Tight layout to prevent overlaps
        plt.tight_layout()

        plt.savefig(file_name, dpi=300)
        plt.close()