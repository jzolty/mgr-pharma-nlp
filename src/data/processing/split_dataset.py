# Skrypt dzieli wygenerowany korpus na zbiory: treningowy (70%), walidacyjny (15%) i testowy (15%).
# Utrzymuje stałe ziarno losowości (seed), zapewniając powtarzalność eksperymentów naukowych do pracy magisterskiej.

import json
import os
import random

def split_data(train_ratio=0.7, val_ratio=0.15, seed=42):
    random.seed(seed)
    
    # Ścieżka wejściowa i wyjściowa zaktualizowana o podfolder "json_spans"
    input_path = os.path.join("data", "processed", "json_spans", "dataset_raw.json")
    processed_dir = os.path.join("data", "processed", "json_spans")
    
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    random.shuffle(data)
    
    total = len(data)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_set = data[:train_end]
    val_set = data[train_end:val_end]
    test_set = data[val_end:]
    
    splits = {
        "train.json": train_set,
        "val.json": val_set,
        "test.json": test_set
    }
    
    print(f"Łącznie dokumentów: {total}")
    for filename, split_data in splits.items():
        out_file = os.path.join(processed_dir, filename)
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(split_data, f, ensure_ascii=False, indent=2)
        print(f" - {filename}: {len(split_data)} próbek ({len(split_data)/total*100:.1f}%)")

if __name__ == "__main__":
    split_data()