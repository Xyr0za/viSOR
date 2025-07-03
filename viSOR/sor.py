import os
from os.path import isfile
from typing import List, Tuple, Dict, Any, Optional

import pandas as pd
import numpy as np
import scipy.signal as signal

import otdrparser
from .dump import dump_csv, dump_tsv

from matplotlib import pyplot as plt
import plotly.graph_objects as go


# Accepted file headers
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
        Initializes the SOR object with !data from either SOR or CSV files.
        """
        self.file_path: str = file_path
        self.file_name: str = file_path.split("/")[-1]
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
        """Parse CSV file with X,Y !data points."""
        df = pd.read_csv(self.file_path)
        x = list(df["Distance"] * 1000)
        y = list(df["Backscatter"])
        self.raw = list(df)
        self.raw_readings = [i for i in zip(x, y)][14:]

    def extract_axis(self, adjust: bool = False) -> None:
        """
        Extracts X and Y axes from the raw readings.

        :param adjust: If True, center the Y values around zero.
        """
        self.C = self.raw_readings[0][1] if adjust and self.raw_readings else 0.0
        self.X = [data_p[0] for data_p in self.raw_readings]
        self.Y = [data_p[1] - self.C for data_p in self.raw_readings]

    def dump(self, file_name: str) -> None:
        """
        Dumps the parsed and processed !data to a file.

        :param file_name: The target filename to dump the !data into.
        """
        file_header = '.' + file_name.split(".")[-1].lower()
        assert file_header in accepted_saving_headers, f"Unsupported output format: {file_header}"

        if file_header == ".csv":
            dump_csv(file_name, self)
        elif file_header == ".tsv":
            dump_tsv(file_name, self)

    def dump_all(self, file_name: str) -> None:
        """Dump all raw metadata to a file."""
        try:
            with open(file_name, "w") as fp:
                for box in self.raw:
                    fp.write(str(box) + "\n\n")
        except Exception:
            raise Exception(f"Failed to dump raw !data to {file_name}")

    def plot(self, file_name: str, vertical_lines: dict = {}) -> None:
        """
        Plots the current raw readings using matplotlib.

        :param file_name: Output filename for the plot
        :param vertical_lines: Dictionary with vertical line labels and their positions
        """
        os.makedirs('/'.join(file_name.split("/")[:-1]), exist_ok=True)
        plt.figure(figsize=(10, 6))

        plt.plot(self.X, self.Y, label="Signal", color='tab:blue', linewidth=2)
        plt.title(f"Attenuation vs Distance | {file_name}", fontsize=16, weight='bold')
        plt.xlabel("Distance (m)", fontsize=14)
        plt.ylabel("Attenuation (dB/km)", fontsize=14)

        for label, x_point in vertical_lines.items():
            plt.axvline(x=x_point, label=label, color="red")

        plt.grid(visible=True, linestyle='--', alpha=0.6)
        plt.legend(fontsize=12, loc='best')
        plt.tight_layout()
        plt.savefig(file_name, dpi=300)
        plt.close()

    def interactive_plot(self,
                         title: str = "OTDR Trace",
                         xaxis_title: str = "Distance (m)",
                         yaxis_title: str = "Attenuation (dB)",
                         vertical_lines: Optional[Dict[str, float]] = None,
                         show: bool = True,
                         save_path: Optional[str] = None) -> go.Figure:
        """
        Creates an interactive Plotly visualization of the !data with optional vertical lines.

        :param title: Title of the plot
        :param xaxis_title: Label for x-axis
        :param yaxis_title: Label for y-axis
        :param vertical_lines: Dictionary of {label: x_position} for vertical lines to add
        :param show: Whether to immediately show the plot
        :param save_path: Optional path to save the HTML file
        :return: plotly.graph_objects.Figure
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.X,
            y=self.Y,
            mode='lines',
            name='OTDR Trace',
            line=dict(color='royalblue', width=2)
        ))

        if vertical_lines:
            for label, x_pos in vertical_lines.items():
                fig.add_vline(
                    x=x_pos,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=label,
                    annotation_position="top right"
                )

        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center'),
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            hovermode='x unified',
            template='plotly_white',
            height=700,
            margin=dict(l=50, r=50, b=50, t=80, pad=4)
        )

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=[
                    dict(count=1000, label="1km", step="all"),
                    dict(count=5000, label="5km", step="all"),
                    dict(count=10000, label="10km", step="all"),
                    dict(step="all")
                ]
            )
        )

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            fig.write_html(save_path)

        if show:
            fig.show()

        return fig

    def classify_reflections(self,
                             file_type: str,
                             x_range: Optional[Tuple[float, float]] = None,
                             prominence: float = 3.0,
                             height_threshold: float = None) -> Tuple[Optional[int], Optional[int]]:
        """
        Classify peaks in the signal based on file type ('E' or 'C').

        :param file_type: Either 'E' or 'C' to specify classification criteria
        :param x_range: Optional tuple (min_x, max_x) to restrict peak search range
        :param prominence: Minimum prominence of peaks (default: 3.0)
        :param height_threshold: Minimum height threshold for peaks (optional)
        :return: Tuple of (peak_x, peak_y)
        :raises ValueError: If file_type is not 'E' or 'C'
        """
        if file_type.upper() not in ('E', 'C'):
            raise ValueError("file_type must be either 'E' or 'C'")

        y_adjusted = np.array([y - self.Y[0] for y in self.Y])
        x_data = np.array(self.X)

        if x_range:
            mask = (x_data >= x_range[0]) & (x_data <= x_range[1])
            x_roi = x_data[mask]
            y_roi = y_adjusted[mask]
        else:
            x_roi = x_data
            y_roi = y_adjusted

        peaks, properties = signal.find_peaks(y_roi, prominence=prominence, height=height_threshold)
        peak_x = x_roi[peaks]
        peak_y = y_roi[peaks]

        if file_type.upper() == 'E':
            return (int(peak_x[0]), int(peak_y[0])) if len(peak_x) > 0 else (None, None)
        else:  # 'C'
            if len(peak_y) > 0:
                max_idx = np.argmax(peak_y)
                return int(peak_x[max_idx]), int(peak_y[max_idx])
            else:
                return None, None
