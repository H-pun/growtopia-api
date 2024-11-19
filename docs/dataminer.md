### Growtopia Dataminer

The `growtopia-api` includes a dataminer tool from [Dataminer](https://github.com/Bolwl/Dataminer) by @Bolwl. This tool helps you discover upcoming items in Growtopia.

To use the dataminer, follow this example:

```python
from growtopia.dataminer import (
    download_latest_growtopia,
    extract_growtopia_binary,
    extract_items,
    extract_version,
    load_previous_version_data,
    save_new_version_data,
    compare_new_items
)

# Previous Version (Example: 4.64)
prev_ver = 4.64
old_items = load_previous_version_data(prev_ver)

# Download and extract the latest Growtopia binary
download_latest_growtopia()
extract_growtopia_binary()

# Read the binary data
with open("tmp/Growtopia", "rb") as file:
    binary_data = file.read().decode("latin-1")

# Extract items and version from the binary data
items = extract_items(binary_data)
version = extract_version(binary_data)

# Save the new version data
save_new_version_data(version, items)

# Compare new items with the old items
new_items = compare_new_items(items, old_items)

# Print new items
print("New items:")
for item in new_items:
    print(item)
```