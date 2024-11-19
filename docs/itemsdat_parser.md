## Growtopia `items.dat` Parser

The `growtopia-api` includes a Python parser for the `items.dat` file from [gt-itemsdat-json](https://github.com/houzeyhoo/gt-itemsdat-json) by @houzeyhoo. This tool allows you to parse and manipulate the `items.dat` file used in Growtopia.

### Parse to JSON
To parse Growtopia's `items.dat` file into a JSON format, use the following example:

```python
import sys
import json
from growtopia.itemsdat_parser import parse_itemsdat

# Path to your items.dat
file_dir = "/path/to/items.dat"
with open(file_dir, "rb") as f:
    data = parse_itemsdat(f)
    json.dump(data, sys.stdout, indent=4)
```

To output the result to a file, use:

```python
import json
from growtopia.itemsdat_parser import parse_itemsdat

# Path to your items.dat
file_dir = "/path/to/items.dat"
# Path to your output file
output_file = "items.json"
with open(file_dir, "rb") as f:
    data = parse_itemsdat(f)
with open(output_file, "w") as outfile:
    json.dump(data, outfile, indent=4)
```

### Troubleshooting & Items.dat Info

If you encounter any issues, the parser may be outdated. Consider editing the `template.py` file to accommodate any changes. Additionally, you can use the `itemsdat_info` script to check for changes in the new version:

```python
from growtopia.itemsdat_parser import itemsdat_info

# Path to your items.dat
file_dir = "/path/to/items.dat"
with open(file_dir, "rb") as f:
    data = itemsdat_info(f)
print(f"Version: {data['version']}")
print(f"Item count: {data['item_count']}")
print(f"First entry size: {data['first_entry_size']}")
```

### Documentation

For detailed information about Growtopia's `items.dat` file format, refer to the following source:
- [growtopia-docs items.dat](https://github.com/H-pun/growtopia-docs/tree/master/items_dat)
