import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.parsing.resume_parser import extract_text
from src.analysis.resume_analyzer import analyze_resume

resume = input("Resume Path: ")

text = extract_text(resume)

result = analyze_resume(text)

print("\n")

for key, value in result.items():

    print("=" * 60)

    print(key.upper())

    print(value)