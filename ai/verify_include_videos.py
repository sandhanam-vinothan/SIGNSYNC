import pandas as pd
from remotezip import RemoteZip
BASE = "datasets/INCLUDE/metadata/"
URL = "https://zenodo.org/api/records/4010759/files/{}/content"
archives = {
    "Greetings_1of2.zip": ["hello", "goodmorning"],
    "Greetings_2of2.zip": ["thankyou"],
    "Adjectives_1of8.zip": ["happy"],
    "Adjectives_7of8.zip": ["good"],
}
frames = []
for split in ["train", "val", "test"]:
    df = pd.read_csv(BASE + split + ".csv")
    df = df[df["include_50"] == True].copy()
    df["clean_label"] = (
        df["label"]
        .str.replace(r"^\d+\.\s*", "", regex=True)
        .str.lower()
        .str.replace(r"[^a-z]", "", regex=True)
    )
    df["split"] = split
    frames.append(df)
metadata = pd.concat(frames, ignore_index=True)
verified = 0
missing = []
for archive_name, signs in archives.items():
    selected = metadata[
        metadata["clean_label"].isin(signs)
    ]
    print(f"\nChecking {archive_name}...", flush=True)
    with RemoteZip(URL.format(archive_name)) as archive:
        available = set(archive.namelist())
        for _, row in selected.iterrows():
            path = row["video_path"]
            if path in available:
                verified += 1
            else:
                missing.append((archive_name, path))
    print(f"Expected recordings: {len(selected)}")
print(f"\nVerified recordings: {verified}/105")
print(f"Missing recordings: {len(missing)}")
for archive_name, path in missing:
    print(f"MISSING: {archive_name} -> {path}")
if missing or verified != 105:
    raise SystemExit("Verification failed")
print("SUCCESS: All 105 video paths verified.")
