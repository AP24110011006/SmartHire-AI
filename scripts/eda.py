import sys
from pathlib import Path

# =====================================================
# Add project root (SmartHire) to Python path
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from src.data.load_data import load_resume_data
from src.data.preprocess import clean_text


def main():
    print("=" * 60)
    print("SMARTHIRE - EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # Load dataset
    df = load_resume_data()

    # Dataset information
    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nNumber of Categories:")
    print(df["Category"].nunique())

    print("\nCategories:")
    print(df["Category"].unique())

    print("\nCategory Counts:")
    print(df["Category"].value_counts())

    # Clean resumes
    print("\nCleaning Resume Text...")
    df["Clean_Resume"] = df["Resume_str"].apply(clean_text)

    print("\nFirst Cleaned Resume (First 500 Characters):")
    print("-" * 60)
    print(df["Clean_Resume"].iloc[0][:500])
    print("-" * 60)

    print("\nEDA Completed Successfully!")


if __name__ == "__main__":
    main()