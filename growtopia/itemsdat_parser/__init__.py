from .template import *
from typing import BinaryIO

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


# Calculate the size of the first entry in the items.dat file by finding the second entry
# via a known string. Useful for figuring out what changed in a new items.dat version.
def calculate_first_entry_size(buffer: BinaryIO) -> int:
    item_data = buffer.read()
    start = item_data.find(b"tiles_page1.rttex")
    # There are 22 bytes before the 'tiles_page1.rttex' string in 2nd entry.
    return item_data.find(b"tiles_page1.rttex", start + 1) - 22


def itemsdat_info(buffer: BinaryIO, calculate=True) -> dict:
    version = parse_number(buffer, 2)
    item_count = parse_number(buffer, 4)
    result = {
        "version": version,
        "item_count": item_count
    }
    if calculate:
        result["first_entry_size"] = calculate_first_entry_size(buffer)
    return result


def parse_itemsdat(buffer: BinaryIO) -> dict:
    info = itemsdat_info(buffer, calculate=False)
    version = info["version"]
    item_count = info["item_count"]
    template = get_generic_template()
    root = {"version": version, "item_count": item_count, "items": []}
    # Parse all items.
    for i in range(item_count):
        item = {}
        for key, value in template.items():
            if value["version"] > version:
                continue
            if "id" in item and item["id"] != i:
                raise AssertionError(f"Item ID mismatch! The parser might be out of date. (item_id={item['id']}, expected={i}), version={version}")
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
