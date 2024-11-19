## Growtopia Dataminer

The `growtopia-api` includes a dataminer tool from [Dataminer](https://github.com/Bolwl/Dataminer) by @Bolwl. This tool helps you discover upcoming items in Growtopia.

### Get the Latest Upcoming Item

To use the dataminer to get the latest item name, follow this example:

> [!WARNING]
> Sometimes the result may not be a real item; it could be a new Growtopia system like [Trade-Scan](https://growtopia.fandom.com/wiki/Trade-Scan).

This process will download fresh binary data from the official Growtopia website and unpack it to the `tmp` folder.
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

### Get Latest Item Sprites

You can additionally get the latest Growtopia RTTEX assets by using the following code:

```python
from growtopia.dataminer import extract_growtopia_assets

extract_growtopia_assets()
```

This will save the latest RTTEX files to the `tmp/game` folder.

### Item Icons

You can also immediately get the icon files for clothes textures using the following code:

```python
from growtopia.dataminer import extract_item_icons

icon_list = [
    "player_handitem.rttex",
    "player_handitem5.rttex",
    "player_longhanditem3.rttex",
]

extract_item_icons(icon_list)
```

This will automatically look for each file in the list with the `_icon` suffix and save it to the `tmp/dest` folder by default.

#### Parameters

- `file_list` (list[str]): The names of the items to search for.
- `source_folder` (str, optional): The source path to the folder containing the list of RTTEX files. Defaults to `tmp/game`.
- `destination_folder` (str, optional): The destination folder for the filtered icons. Defaults to `tmp/dest`.
