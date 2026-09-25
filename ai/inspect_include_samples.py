import pandas as pd
base = "datasets/INCLUDE/metadata/"
targets = [
    "hello",
    "goodmorning",
    "thankyou",
    "good",
    "happy"
]
for split in ["train", "val", "test"]:
    df = pd.read_csv(base + split + ".csv")
    df = df[df["include_50"] == True].copy()
    df["clean_label"] = (
        df["label"]
        .str.replace(r"^\d+\.\s*", "", regex=True)
        .str.lower()
        .str.replace(r"[^a-z]", "", regex=True)
    )
    selected = df[df["clean_label"].isin(targets)]
    print(f"\n{split.upper()}")
    print("Matching videos:", len(selected))
    print(
        selected.groupby(
            ["parent_label", "clean_label"]
        ).size().to_string()
    )
    print("\nExample video paths:")
    print(selected["video_path"].head(10).to_string(index=False))
