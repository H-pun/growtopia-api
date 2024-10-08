from growtopia.dataminer import *
# import growtopia.growtopia_items


def main():
    # item = GrowtopiaItem("Dirt")
    # print(item.get_item_data())

    vold = input("Previous Version (Example: 4.64): ")
    
    # Load previous version data
    old_items = load_previous_version_data(vold)
    
    # Download and extract the latest Growtopia binary
    download_latest_growtopia()
    extract_growtopia_binary()
    
    # Read and process the binary file
    with open("tmp/Growtopia", "rb") as file:
        binary_data = file.read().decode("latin-1")
    
    items = extract_items(binary_data)
    version = extract_version(binary_data)
    
    # Save new version data and display differences
    save_new_version_data(version, items)
    display_new_items(items, old_items)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
