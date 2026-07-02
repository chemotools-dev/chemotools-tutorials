"""
Helper function to read .csv files into Spectrum objects.
"""

import re
from datetime import datetime
from pathlib import Path

import numpy as np

from src.spectrum import Spectrum

_CALIBRATION_PATTERN = re.compile(
    r"^sample-(\d+)-(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.csv$"
)


def csv_file_reader(
    path_to_csv: str, x_axis_column: int = 0, y_axis_column: int = 1
) -> tuple[np.ndarray, np.ndarray]:
    """
    Reads a .csv file and returns the x and y axis data as numpy arrays.

    Args:
        path_to_csv (str): Path to the .csv file.
        x_axis_column (int): Column index for the x-axis data. Default is 0.
        y_axis_column (int): Column index for the y-axis data. Default is 1.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing the x and y axis data as numpy arrays.
    """
    data = np.loadtxt(path_to_csv, delimiter=",")
    x_data = data[:, x_axis_column]
    y_data = data[:, y_axis_column]

    return Spectrum(x=x_data, y=y_data, metadata={})


def read_calibration_spectra(folder: str) -> list[Spectrum]:
    """
    Reads all calibration spectra from a folder.

    Expects files named sample-{nr}-{YYYY-MM-DDTHH:MM:SS}.csv.
    The sample number and datetime are stored in each Spectrum's metadata.

    Args:
        folder (str): Path to the folder containing calibration CSV files.

    Returns:
        list[Spectrum]: Spectra sorted by sample number, each with
            metadata keys 'sample_nr' (int) and 'datetime' (datetime).
    """
    matches = []
    for file in Path(folder).iterdir():
        m = _CALIBRATION_PATTERN.match(file.name)
        if m:
            matches.append((int(m.group(1)), datetime.fromisoformat(m.group(2)), file))

    matches.sort(key=lambda t: t[0])

    spectra = []
    for sample_number, sample_datetime, file in matches:
        spectrum = csv_file_reader(str(file))
        spectrum.metadata["sample_nr"] = sample_number
        spectrum.metadata["datetime"] = sample_datetime
        spectra.append(spectrum)

    return spectra
