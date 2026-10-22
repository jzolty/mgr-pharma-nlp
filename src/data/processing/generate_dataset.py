# Skrypt generuje syntetyczny korpus tekstów farmaceutycznych (np. zamówień i notatek HIS), łącząc autentyczne dane z rejestru RPL z szablonami zdań.
# Dzięki automatycznemu wyznaczaniu pozycji znaków dla encji (leki, dawki, ilości) tworzy zbiór uczący niezbędny do wytrenowania i ewaluacji modeli NER.
import json
import os
import random

def load_entities():
    dict_path = os.path.join("data", "processed", "dictionary", "pharma_entities.json")
    with open(dict_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_samples(count=500):
    entities = load_entities()
    drugs = entities.get("drugs", [])
    doses = entities.get("doses", [])
    forms = entities.get("forms", [])
    manufacturers = entities.get("manufacturers", [])

    quantities = ["1 op.", "2 op.", "5 op.", "10 op.", "20 op.", "50 szt.", "100 szt.", "3 amp."]

    # Szablony zdań: {zmienna} zostanie zastąpiona wartością
    templates = [
        # Styl 1: Zamówienie / e-mail apteczny
        "Dzień dobry, proszę o pilne zamówienie {QUANTITY} leku {DRUG_NAME} w dawce {DOSE}.",
        "Zapotrzebowanie na oddział: {DRUG_NAME} {DOSE}, postać {FORM}, w ilości {QUANTITY}.",
        "Zamawiam {QUANTITY} preparatu {DRUG_NAME} ({MANUFACTURER}), moc: {DOSE}.",
        
        # Styl 2: Notatka ze zleceniem w systemie HIS
        "Zlecono podanie pacjentowi {DRUG_NAME} {DOSE} {FORM} doraźnie w liczbie {QUANTITY}.",
        "Podano choremu: {DRUG_NAME} w dawce {DOSE}.",
        
        # Styl 3: Zapis magazynowy / skrótowy
        "Poz. magazynowa: {DRUG_NAME} {DOSE} | {FORM} | {MANUFACTURER} | sztuk: {QUANTITY}."
    ]

    dataset = []

    for idx in range(count):
        template = random.choice(templates)
        
        # Losujemy wartości
        chosen_drug = random.choice(drugs)
        chosen_dose = random.choice(doses)
        chosen_form = random.choice(forms)
        chosen_manuf = random.choice(manufacturers)
        chosen_qty = random.choice(quantities)

        values = {
            "DRUG_NAME": chosen_drug,
            "DOSE": chosen_dose,
            "FORM": chosen_form,
            "MANUFACTURER": chosen_manuf,
            "QUANTITY": chosen_qty
        }

        # Budujemy tekst i śledzimy pozycje znaków
        # Zastępujemy kolejno etykiety, obliczając ich indeks start i end
        text = template
        entity_spans = []

        # Aby pozycje się nie rozjeżdżały, wstawiamy unikalne tokeny i szukamy ich
        # Najprostszy bezpieczny mechanizm:
        for label, val in values.items():
            placeholder = "{" + label + "}"
            if placeholder in text:
                start_char = text.find(placeholder)
                text = text[:start_char] + val + text[start_char + len(placeholder):]
                end_char = start_char + len(val)
                entity_spans.append({
                    "start": start_char,
                    "end": end_char,
                    "label": label,
                    "text": val
                })

        # Sortujemy encje po indeksie startowym
        entity_spans.sort(key=lambda x: x["start"])

        dataset.append({
            "id": f"sample_{idx+1:04d}",
            "text": text,
            "entities": entity_spans
        })

    out_path = os.path.join("data", "processed", "json_spans", "dataset_raw.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Wygenerowano {len(dataset)} przykładowych zdań do: {out_path}")
    print("\nPrzykładowe pierwsze wygenerowane zdanie:")
    print(f"Tekst: {dataset[0]['text']}")
    print(f"Encje: {dataset[0]['entities']}")

if __name__ == "__main__":
    generate_samples(500)