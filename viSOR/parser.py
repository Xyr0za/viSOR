from os.path import isfile
from typing import List, Tuple, Dict, Any

import otdrparser
from .dump import dump_csv, dump_tsv
from .helper import grab_name

accepted_parsing_headers: Tuple[str, ...] = (".sor", ".msor")
accepted_saving_headers: Tuple[str, ...] = (".csv", ".tsv")


class Parser:
    def __init__(self, file_path: str) -> None:
        """
        Initializes the parser with the given file path.
        Validates the file header and existence.
        Parses the raw OTDR data and extracts raw readings.
        """
        file_header = '.' + file_path.split(".")[-1]
        assert file_header in accepted_parsing_headers
        assert isfile(file_path)

        self.file_path: str = file_path

        with open(self.file_path, 'rb') as fp:
            blocks: List[Dict[str, Any]] = otdrparser.parse(fp)

        self.raw: List[Dict[str, Any]] = blocks
        self.raw_readings: List[Tuple[float, float]] = grab_name(self.raw, "DataPts")["data_points"]

        self.X: List[float] = []
        self.Y: List[float] = []
        self.C: float = 0.0

    def extract_axis(self, adjust: bool = False) -> None:
        """
        Extracts X and Y axes from the raw readings.

        :param adjust: If True, center the Y values around zero.
        """
        if adjust:
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
        file_header = '.' + file_name.split(".")[-1]
        assert file_header in accepted_saving_headers

        match file_header:
            case ".csv":
                dump_csv(file_name, self)
            case ".tsv":
                dump_tsv(file_name, self)
            case _:
                raise Exception("File header is not valid")
