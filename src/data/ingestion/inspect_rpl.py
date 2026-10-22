import pandas as pd
import os

csv_path = os.path.join("data", "raw", "rpl.csv")

print(f"Wczytywanie pliku: {csv_path}...")

# Pliki z e-zdrowia często używają średnika jako separatora
try:
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8', low_memory=False)
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, sep=';', encoding='cp1250', low_memory=False)

print("\n--- Informacje o zbiorze ---")
print(f"Liczba zarejestrowanych pozycji: {len(df)}")
print(f"Dostępne kolumny ({len(df.columns)}):")
for col in df.columns:
    print(f" - {col}")

print("\n--- Przykładowe 3 wiersze ---")
# Wyświetlamy najważniejsze kolumny, jeśli istnieją
print(df.head(3).T)