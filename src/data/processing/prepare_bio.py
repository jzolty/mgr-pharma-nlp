import json
import os
import spacy

def convert_to_bio(input_file, output_file):
    nlp = spacy.blank("pl")
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    bio_dataset = []
    
    for sample in data:
        text = sample["text"]
        entities = sample["entities"]
        
        doc = nlp(text)
        tokens = []
        ner_tags = []
        
        for token in doc:
            tokens.append(token.text)
            
            token_start = token.idx
            token_end = token.idx + len(token.text)
            
            tag = "O" 
            for ent in entities:
                ent_start = ent["start"]
                ent_end = ent["end"]
                label = ent["label"]
                
                # Sprawdzenie, czy słowo znajduje się wewnątrz oznaczonej encji
                if token_start >= ent_start and token_end <= ent_end:
                    if token_start == ent_start:
                        tag = f"B-{label}"
                    else:
                        tag = f"I-{label}"
                    break
                    
            ner_tags.append(tag)
            
        bio_dataset.append({
            "id": sample["id"],
            "tokens": tokens,
            "ner_tags": ner_tags
        })
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bio_dataset, f, ensure_ascii=False, indent=2)
    
    print(f"Przekonwertowano {len(data)} zdań do formatu BIO: {output_file}")

if __name__ == "__main__":
    processed_dir = os.path.join("data", "processed")
    
    # Konwersja wszystkich trzech zbiorów (odczyt z json_spans, zapis do bio)
    convert_to_bio(
        os.path.join(processed_dir, "json_spans", "train.json"), 
        os.path.join(processed_dir, "bio", "train_bio.json")
    )
    convert_to_bio(
        os.path.join(processed_dir, "json_spans", "val.json"), 
        os.path.join(processed_dir, "bio", "val_bio.json")
    )
    convert_to_bio(
        os.path.join(processed_dir, "json_spans", "test.json"), 
        os.path.join(processed_dir, "bio", "test_bio.json")
    )