from remotezip import RemoteZip
url = (
    "https://zenodo.org/api/records/4010759/"
    "files/Greetings_2of2.zip/content"
)
print("Connecting to the remote archive...")
with RemoteZip(url) as archive:
    files = archive.namelist()
    print(f"Total entries: {len(files)}")
    print("\nFirst 15 entries:")
    for filename in files[:15]:
        print(filename)
    targets = ["48. Hello", "51. Good Morning", "55. Thank you"]
    print("\nMatching video files:")
    for target in targets:
        matches = [
            name for name in files
            if target.lower() in name.lower()
            and name.lower().endswith(".mov")
        ]
        print(f"\n{target}: {len(matches)} files")
        for name in matches[:5]:
            print(" ", name)
