from src.data.load_data import load_resume_data

df = load_resume_data()

print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)