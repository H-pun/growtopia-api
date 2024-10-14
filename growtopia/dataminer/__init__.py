import os
import requests
from tqdm import tqdm

def download_latest_growtopia():
    """Download the latest Growtopia .dmg file for data mining."""
    url = "https://growtopiagame.com/Growtopia-mac.dmg"
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    print("Downloading Latest Growtopia for datamining..")
    
    os.makedirs("tmp", exist_ok=True)
    with open("tmp/Growtopia.dmg", 'wb') as file, tqdm(
        total=total_size, unit='B', unit_scale=True, desc="Growtopia", ncols=80
    ) as progress_bar:
        for data in response.iter_content(1024):
            file.write(data)
            progress_bar.update(len(data))

    print("Download Completed!")

def extract_growtopia_binary():
    """Extract Growtopia binary using 7zip."""
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "7z.exe")
    os.system(f"{bin_path} e ./tmp/Growtopia.dmg Growtopia.app/Contents/MacOS/Growtopia -otmp -aoa")

def load_previous_version_data(version: str | bytes):
    """Load item data from the previous version file or an uploaded file."""
    if isinstance(version, str):
        file_path = f"bol_V{version}.txt"
        
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read().splitlines()
        else:
            exit("Previous version not found!")
    else:
        return version.decode("utf-8").splitlines()

def remove_non_ascii(text):
    """Remove non-ASCII characters from the text."""
    return ''.join([s for s in text if 31 < ord(s) < 127])

def extract_items(data):
    """Extract and clean item data from the binary."""
    items = []
    
    for line in data.split("\n"):
        line = line.replace("ITEM_ID_", "splitherelolITEM_ID_")
        
        for part in line.split("splitherelol"):
            if "ITEM_ID_" in part:
                if len(part) > 500:
                    part = part.split("solid")[0]
                items.append(remove_non_ascii(part[:-1]))  # Remove last character

    # Clean the last item
    items[-1] = items[-1][:items[-1].find("ALIGNMENT")]
    return items

def extract_version(data):
    """Extract version information from the binary."""
    version_start = data.find("www.growtopia1.com") + 18
    version_info = data[version_start:data.find("Growtopia", version_start)]
    return remove_non_ascii(version_info)

def save_new_version_data(version, items):
    """Save new version item data to a file."""
    with open(f"bol_{version}.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(items))

def compare_new_items(items, old_items):
    """Display newly added item names."""
    # print("================================================================")
    # print("Upcoming Item Names (Note: Some items may not be named properly)")
    # print("================================================================")
    
    new_items = []

    # Identify and display items that are present in the new list but not in the old one
    for item in items:
        if item not in old_items:
            # Convert the item ID format to a readable name (e.g., ITEM_ID_XYZ -> Xyz)
            readable_item = item.replace("ITEM_ID_", "").replace("_", " ").title()
            new_items.append(readable_item)

    return new_items
