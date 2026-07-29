import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA = BASE_DIR / "data" / "raw"

def load_resume_data():
    file_path = RAW_DATA / "Resume.csv"

    df = pd.read_csv(
        file_path,
        usecols=["Resume_str", "Category"]
    )

    return df