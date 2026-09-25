from remotezip import RemoteZip
base_url = (
    "https://zenodo.org/api/records/4010759/"
    "files/Adjectives_{}of8.zip/content"
)
targets = {
    "94. good": [],
    "3. happy": [],
}
for number in range(1, 9):
    archive_name = f"Adjectives_{number}of8.zip"
    url = base_url.format(number)
    print(f"\nInspecting {archive_name}...", flush=True)
    try:
        with RemoteZip(url) as archive:
            files = archive.namelist()
            for target in targets:
                matches = [
                    name for name in files
                    if name.lower().endswith(".mov")
                    and target.lower() in [
                        part.lower()
                        for part in name.split("/")
                    ]
                ]
                print(f"{target}: {len(matches)} videos")
                if matches:
                    targets[target].append(
                        (archive_name, matches)
                    )
    except Exception as error:
        print(f"ERROR: {error}")
print("\nFINAL RESULTS")
for sign, archives in targets.items():
    print(f"\n{sign}")
    for archive_name, files in archives:
        print(f"  {archive_name}: {len(files)} videos")
        print(f"  Example: {files[0]}")
