import os
import json

base_dir = "ROTOR"
output_file = "../files-manifest.json"
other_files_path = "../files-manifest-other.json"

# Load existing entries from other-files.json
if os.path.exists(other_files_path):
    with open(other_files_path, "r", encoding="utf-8") as f:
        try:
            combined_list = json.load(f)
        except json.JSONDecodeError:
            print("Warning: other-files.json is not a valid JSON list. Starting with empty list.")
            combined_list = []
else:
    combined_list = []

# Add ROTOR files
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        filepath = os.path.join(root, filename)
        normalized_path = filepath.replace("\\", "/")  # Normalize Windows-style backslashes
        file_entry = {
            "path": normalized_path,
            "url": f"/ROTOR/files/{normalized_path}"
        }
        combined_list.append(file_entry)

# Write to output JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(combined_list, f, indent=4)

print(f"{output_file} created with {len(combined_list)} file entries.")
