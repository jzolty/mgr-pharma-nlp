import json
import os
import sys

# Dodanie ścieżki, aby móc zaimportować model bazowy z innego folderu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.baseline.spacy_baseline import build_baseline_model

def evaluate_baseline():
    print("Ładowanie modelu i danych testowych...")
    model = build_baseline_model()
    test_path = os.path.join("data", "processed", "json_spans", "test.json")
    
    with open(test_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for sample in test_data:
        text = sample["text"]
        
        # Zbiór unikalnych krotek (tekst, etykieta) dla oczekiwanych i przewidzianych wyników
        expected_ents = {(ent["text"], ent["label"]) for ent in sample["entities"]}
        
        doc = model(text)
        predicted_ents = {(ent.text, ent.label_) for ent in doc.ents}

        true_positives += len(expected_ents.intersection(predicted_ents))
        false_positives += len(predicted_ents - expected_ents)
        false_negatives += len(expected_ents - predicted_ents)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n--- Wyniki Ewaluacji Modelu Słownikowego (Baseline) ---")
    print(f"Precyzja (Precision): {precision:.4f}")
    print(f"Czułość (Recall):     {recall:.4f}")
    print(f"F1-Score:             {f1:.4f}")
    
    # Wyjaśnienie metryki QUANTITY
    print("\nUwaga: Recall jest obniżony, ponieważ baseline z założenia nie wykrywa encji QUANTITY.")

if __name__ == "__main__":
    evaluate_baseline()