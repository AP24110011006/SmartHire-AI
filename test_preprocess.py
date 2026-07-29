from src.data.load_data import load_resume_data
from src.data.preprocess import clean_text

df = load_resume_data()

print("Before Cleaning:\n")
print(df["Resume_str"][0][:500])

print("\n" + "="*60 + "\n")

cleaned = clean_text(df["Resume_str"][0])

print("After Cleaning:\n")
print(cleaned[:500])