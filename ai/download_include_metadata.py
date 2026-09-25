
from pathlib import Path

from datasets import load_dataset

OUTPUT = Path("datasets/INCLUDE/metadata")
OUTPUT.mkdir(parents=True, exist_ok=True)

dataset = load_dataset("ai4bharat/INCLUDE")

for split_name, split_data in dataset.items():
    output_file = OUTPUT / f"{split_name}.csv"
    split_data.to_csv(str(output_file))

    include50_count = sum(split_data["include_50"])

    print(f"{split_name}: {len(split_data)} records")
    print(f"INCLUDE-50 records: {include50_count}")
    print(f"Saved: {output_file}")
