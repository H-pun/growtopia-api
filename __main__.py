import sys
import json
from pprint import pprint

from growtopia.itemsdat_parser import *
# from growtopia.dataminer import download_latest_growtopia, extract_growtopia_binary, extract_items, extract_version, load_previous_version_data, save_new_version_data
from growtopia.growtopia_info import GrowtopiaItem, search_item
from growtopia.rttex_converter import rttex_pack, rttex_unpack

# vold = input("Previous Version (Example: 4.64): ")
# # Load previous version data
# old_items = load_previous_version_data(vold)
# # Download and extract the latest Growtopia binary
# # download_latest_growtopia()
# extract_growtopia_binary()
# # Read and process the binary file
# with open("tmp/Growtopia", "rb") as file:
#     binary_data = file.read().decode("latin-1")
# items = extract_items(binary_data)
# version = extract_version(binary_data)
# # Save new version data and display differences
# save_new_version_data(version, items)
# new_items = get_new_items(items, old_items)
# print("New items:")
# for item in new_items:
#     print(item)

# Run the parser. # Usage: python itemsdat-parser <info|parse> <items.dat path>
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python growtopia-api <datamine|itemsdat> [<info|parse> <items.dat path>]", file=sys.stderr)
        exit(1)
    command = sys.argv[1].lower()
    if command == "wiki":
        if len(sys.argv) < 3:
            print("Usage: python growtopia-api wiki <search|item>", file=sys.stderr)
            exit(1)
        subcommand = sys.argv[2].lower()
        if subcommand not in ["search", "item"]:
            print("Invalid subcommand. Use 'search' to search for an item or 'item' to get item details.", file=sys.stderr)
            exit(1)
        item_name = input("Item name: ")
        data = search_item(item_name) if subcommand == "search" else GrowtopiaItem(item_name).get_item_data()
        pprint(data)
    # elif command == "datamine":
    #     vold = input("Previous Version (Example: 4.64): ")
    #     # Load previous version data
    #     old_items = load_previous_version_data(vold)
    #     # Download and extract the latest Growtopia binary
    #     # download_latest_growtopia()
    #     binary_data = extract_growtopia_binary()
    #     # Read and process the binary file
    #     items = extract_items(binary_data)
    #     version = extract_version(binary_data)
    #     # Save new version data and display differences
    #     save_new_version_data(version, items)
    #     new_items = get_new_items(items, old_items)
    #     print("New items:")
    #     for item in new_items:
    #         print(item)

    elif command == "itemsdat":
        if len(sys.argv) < 4:
            print("Usage: python growtopia-api itemsdat <info|parse> <items.dat path>", file=sys.stderr)
            exit(1)
        subcommand = sys.argv[2].lower()
        if subcommand not in ["info", "parse"]:
            print("Invalid subcommand. Use 'info' to get items.dat info or 'parse' to parse the items.dat file.", file=sys.stderr)
            exit(1)
        with open(sys.argv[3], "rb") as f:
            if subcommand == "info":
                data = itemsdat_info(f)
                print(f"Version: {data['version']}", file=sys.stderr)
                print(f"Item count: {data['item_count']}", file=sys.stderr)
                print(f"First entry size: {data['first_entry_size']}", file=sys.stderr)
            elif subcommand == "parse":
                data = parse_itemsdat(f)
                # Output to stdout.
                json.dump(data, sys.stdout, indent=4)
    elif command == "rttex-converter":
        if len(sys.argv) < 4:
            print("Usage: python growtopia-api rttex-converter <pack|unpack> <file path>", file=sys.stderr)
            exit(1)
        subcommand = sys.argv[2].lower()
        file_path = sys.argv[3]
        if subcommand == "unpack":
            with open(file_path, "rb") as rttex_file:
                unpacked_png = rttex_unpack(rttex_file)
                output_path = file_path.replace(".rttex", ".png")
                with open(output_path, "wb") as f:
                    f.write(unpacked_png)
            print(f"Unpacked PNG saved to {output_path}")
        elif subcommand == "pack":
            with open(file_path, "rb") as png_file:
                packed_data = rttex_pack(png_file)
                output_path = file_path.replace(".png", ".rttex")
                with open(output_path, "wb") as f:
                    f.write(packed_data)
            print(f"Packed RTTEX saved to {output_path}")
        else:
            print("Invalid subcommand. Use 'pack' to pack a PNG file into RTTEX or 'unpack' to unpack an RTTEX file into PNG.", file=sys.stderr)
            exit(1)
    else:
        print("Invalid command. Use 'datamine' or 'itemsdat'.", file=sys.stderr)
        exit(1)
