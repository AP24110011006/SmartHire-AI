import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.parsing.resume_parser import extract_text

# Change this to the path of your test resume
resume_path = input("Enter resume file path: ")

text = extract_text(resume_path)

print("\n" + "=" * 60)
print("Extracted Resume Text")
print("=" * 60)

print(text[:2000])

print("\nExtraction Successful!")