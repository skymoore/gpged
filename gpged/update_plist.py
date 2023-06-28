import plistlib

plist_file_path = "dist/gpged.app/Contents/Info.plist"

with open(plist_file_path, "rb") as f:
    plist_data = plistlib.load(f)

plist_data["LSEnvironment"] = {"PATH": "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:"}

with open(plist_file_path, "wb") as f:
    plistlib.dump(plist_data, f)
