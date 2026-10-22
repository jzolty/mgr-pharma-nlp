import os
import json
import pandas as pd

def build_dictionaries():
    raw_path = os.path.join("data", "raw", "rpl.csv")
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    print(f"Wczytywanie: {raw_path}...")
    try:
        df = pd.read_csv(raw_path, sep=';', encoding='utf-8', low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(raw_path, sep=';', encoding='cp1250', low_memory=False)

    # 1. Filtrujemy tylko preparaty przeznaczone dla ludzi
    if "Rodzaj preparatu" in df.columns:
        df = df[df["Rodzaj preparatu"].str.strip().str.lower() == "ludzki"]

    print(f"Pozycje dla ludzi: {len(df)}")

    # 2. Wyciągamy i czyścimy unikalne wartości
    def clean_series(series):
        return sorted(list(set(
            series.dropna().astype(str).str.strip().tolist()
        )))

    drugs = clean_series(df["Nazwa Produktu Leczniczego"]) if "Nazwa Produktu Leczniczego" in df.columns else []
    substances = clean_series(df["Substancja czynna"]) if "Substancja czynna" in df.columns else []
    doses = clean_series(df["Moc"]) if "Moc" in df.columns else []
    forms = clean_series(df["Postać farmaceutyczna"]) if "Postać farmaceutyczna" in df.columns else []
    manufacturers = clean_series(df["Podmiot odpowiedzialny"]) if "Podmiot odpowiedzialny" in df.columns else []

    # 3. Zapisujemy w zwięzłym słowniku JSON
    dictionary = {
        "drugs": drugs,
        "substances": substances,
        "doses": doses,
        "forms": forms,
        "manufacturers": manufacturers
    }

    out_file = os.path.join(processed_dir, "dictionary", "pharma_entities.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"\nSukces! Słownik dziedzinowy zapisano w: {out_file}")
    print(f" - Unikalnych nazw handlowych: {len(drugs)}")
    print(f" - Unikalnych substancji czynnych: {len(substances)}")
    print(f" - Unikalnych dawek: {len(doses)}")
    print(f" - Unikalnych postaci leku: {len(forms)}")
    print(f" - Unikalnych producentów: {len(manufacturers)}")

if __name__ == "__main__":
    build_dictionaries()