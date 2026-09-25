from pathlib import Path
from remotezip import RemoteZip
import pandas as pd
import shutil
BASE = Path("datasets/INCLUDE")
METADATA = BASE / "metadata"
OUTPUT = BASE / "videos"
URL = (
    "https://zenodo.org/api/records/4010759/"
    "files/{}/content"
)
ARCHIVES = {
    "Greetings_1of2.zip": ["hello", "goodmorning"],
    "Greetings_2of2.zip": ["thankyou"],
    "Adjectives_1of8.zip": ["happy"],
    "Adjectives_7of8.zip": ["good"],
}
# Safety limit per extracted recording: 500 MiB.
MAX_VIDEO_BYTES = 500 * 1024 * 1024
frames = []
for split in ["train", "val", "test"]:
    df = pd.read_csv(METADATA / f"{split}.csv")
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
selected_signs = {
    sign
    for signs in ARCHIVES.values()
    for sign in signs
}
selected = metadata[
    metadata["clean_label"].isin(selected_signs)
].copy()
if len(selected) != 105:
    raise SystemExit(
        f"Expected 105 records, found {len(selected)}"
    )
print("SIGNSYNC selective downloader")
print(f"Selected recordings: {len(selected)}")
answer = input(
    "Download the 105 selected videos? Type YES: "
)
if answer != "YES":
    print("Cancelled. No downloads started.")
    raise SystemExit(0)
downloaded = 0
skipped = 0
failed = []
for archive_name, signs in ARCHIVES.items():
    rows = selected[
        selected["clean_label"].isin(signs)
    ]
    print(f"\nOpening {archive_name}...", flush=True)
    try:
        with RemoteZip(URL.format(archive_name)) as archive:
            available = {
                info.filename: info
                for info in archive.infolist()
            }
            for row in rows.itertuples():
                source = row.video_path
                # The output path is constructed from trusted
                # split and label values, not ZIP folder paths.
                filename = Path(source).name
                if (
                    filename != Path(filename).name
                    or not filename.lower().endswith(".mov")
                ):
                    failed.append(source)
                    continue
                destination = (
                    OUTPUT
                    / row.split
                    / row.clean_label
                    / filename
                )
                info = available.get(source)
                if (
                    info is None
                    or info.file_size <= 0
                    or info.file_size > MAX_VIDEO_BYTES
                ):
                    print(f"INVALID OR MISSING: {source}")
                    failed.append(source)
                    continue
                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )
                if destination.exists():
                    if destination.stat().st_size == info.file_size:
                        print(f"SKIPPED: {destination}")
                        skipped += 1
                        continue
                temporary = destination.with_suffix(".part")
                print(
                    f"Downloading: {row.split}/"
                    f"{row.clean_label}/{filename}",
                    flush=True
                )
                try:
                    with archive.open(source) as remote:
                        with temporary.open("wb") as local:
                            shutil.copyfileobj(
                                remote,
                                local,
                                length=1024 * 1024
                            )
                    if temporary.stat().st_size != info.file_size:
                        raise ValueError(
                            "Downloaded file size mismatch"
                        )
                    temporary.replace(destination)
                    downloaded += 1
                except Exception as error:
                    print(f"FAILED: {source}: {error}")
                    failed.append(source)
                    temporary.unlink(missing_ok=True)
    except Exception as error:
        print(f"ARCHIVE ERROR: {error}")
        failed.extend(
            row.video_path for row in rows.itertuples()
            if not (
                OUTPUT
                / row.split
                / row.clean_label
                / Path(row.video_path).name
            ).exists()
        )
print("\nDOWNLOAD SUMMARY")
print(f"Downloaded: {downloaded}")
print(f"Already present: {skipped}")
print(f"Failed: {len(failed)}")
if failed:
    print("\nFailed recordings:")
    for path in sorted(set(failed)):
        print(path)
    raise SystemExit(1)
print("SUCCESS: Selected videos downloaded.")
