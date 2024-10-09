from .template import *
from .itemsdat_info import *
from typing import BinaryIO
import json
import sys


# Parse a numeric field of a given size.
def parse_number(buffer: BinaryIO, size: int) -> int:
    return int.from_bytes(buffer.read(size), byteorder="little")


# Parse a string.
def parse_string(buffer: BinaryIO) -> str:
    len = parse_number(buffer, 2)
    return buffer.read(len).decode("utf-8")


# Decrypt item name via XOR cipher + itemID offset.
def decrypt_item_name(name: str, id: int) -> str:
    key = "PBG892FXX982ABC*"
    key_len = len(key)
    result = []
    for i in range(len(name)):
        result += chr(ord(name[i]) ^ ord(key[(i + id) % key_len]))
    return "".join(result)


def parse_itemsdat(buffer: BinaryIO) -> dict:
    version = parse_number(buffer, 2)
    item_count = parse_number(buffer, 4)
    template = get_generic_template()
    root = {"version": version, "item_count": item_count, "items": []}
    # Parse all items.
    for i in range(item_count):
        item = {}
        for key, value in template.items():
            if value["version"] > version:
                continue
            if "id" in item and item["id"] != i:
                raise AssertionError(
                    f"Item ID mismatch! The parser might be out of date. (item_id={item['id']}, expected={i}), version={version}"
                )
            field_value = None
            if value["size"] == STRING_XOR and version >= 3:
                # STRING_XOR is encrypted from version onwards.
                field_value = decrypt_item_name(parse_string(buffer), item["id"])
            elif value["size"] == STRING:
                field_value = parse_string(buffer)
            else:
                field_value = parse_number(buffer, value["size"])
            # Skip underscored fields.
            if not key.startswith("_"):
                item[key] = field_value
        root["items"].append(item)
    return root


# Run the parser. # Usage: python itemsdat-parser <items.dat path>
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python itemsdat-parser <items.dat path>", file=sys.stderr)
        exit(1)
    data = parse_itemsdat(open(sys.argv[1], "rb"))
    # Output to stdout.
    with open("items.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

# if __name__ == "__main__":
#     if len(sys.argv) <= 1:
#         print("Usage: python itemsdat-info <items.dat path>", file=sys.stderr)
#         exit(1)
#     with open(sys.argv[1], "rb") as f:
#         data = itemsdat_info(f)
#         print(f"Version: {data['version']}", file=sys.stderr)
#         print(f"Item count: {data['item_count']}", file=sys.stderr)
#         print(f"First entry size: {data['first_entry_size']}", file=sys.stderr)
