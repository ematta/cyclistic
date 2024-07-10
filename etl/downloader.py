import os
import pandas as pd
import requests
import shutil
import sqlite3
import zipfile
from pathlib import Path
from tqdm import tqdm

download_url = "https://divvy-tripdata.s3.amazonaws.com/"
download_files = [
    "202307-divvy-tripdata.zip",
    "202308-divvy-tripdata.zip",
    "202309-divvy-tripdata.zip",
    "202310-divvy-tripdata.zip",
    "202311-divvy-tripdata.zip",
    "202312-divvy-tripdata.zip",
    "202401-divvy-tripdata.zip",
    "202402-divvy-tripdata.zip",
    "202403-divvy-tripdata.zip",
    "202404-divvy-tripdata.zip",
    "202405-divvy-tripdata.zip",
    "202406-divvy-tripdata.zip"
]
working_directory = "data/"
db_url = "cyclistic.db"


def unzip(filename):
    """Unzips a zip file and displays a progress bar."""
    with zipfile.ZipFile(filename, "r") as zip_ref:
        total_size = sum((info.file_size for info in zip_ref.infolist()))

        with zipfile.ZipFile(filename, "r") as zip_ref:
            with tqdm(
                desc=filename,
                total=total_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for info in zip_ref.infolist():
                    zip_ref.extract(info, path=os.path.dirname(filename))

def download_zip(url, filename):
    """Downloads a zip file from the given URL and displays a progress bar."""
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes

    total_size = int(response.headers.get("content-length", 0))

    with open(filename, "wb") as f, tqdm(
        desc=filename,
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))


if __name__ == "__main__":
    # Delete directory if it already exists
    if os.path.exists(working_directory):
        shutil.rmtree(working_directory)
    # If file exists delete it
    if os.path.exists("cyclistic.db"):
        os.remove(db_url)
    conn = sqlite3.connect(db_url)
    # Create the working directory if it doesn't exist
    Path(working_directory).mkdir(parents=True, exist_ok=True)
    # Download the files
    for file in download_files:
        download_zip(download_url + file, working_directory + file)
        unzip(working_directory + file)
        os.remove(working_directory + file)
        pd.read_csv(
            working_directory + file.replace(".zip", ".csv")).to_sql(
                "cyclistic", conn, if_exists="append")
