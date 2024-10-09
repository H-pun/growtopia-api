import sys
from typing import BinaryIO


# Calculate the size of the first entry in the items.dat file by finding the second entry 
# via a known string. Useful for figuring out what changed in a new items.dat version.
def calculate_first_entry_size(buffer: BinaryIO) -> int:
    item_data = buffer.read()
    start = item_data.find(b"tiles_page1.rttex")
    # There are 22 bytes before the 'tiles_page1.rttex' string in 2nd entry.
    return item_data.find(b"tiles_page1.rttex", start + 1) - 22

def itemsdat_info(buffer: BinaryIO) -> dict:
    version = int.from_bytes(buffer.read(2), byteorder="little")
    item_count = int.from_bytes(buffer.read(4), byteorder="little")
    first_entry_size = calculate_first_entry_size(buffer)
    
    return {
        "version": version,
        "item_count": item_count,
        "first_entry_size": first_entry_size
    }
