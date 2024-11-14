import os
import shutil
import requests
from tqdm import tqdm


def download_latest_growtopia() -> None:
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


def extract_growtopia_binary() -> None:
    """Extract Growtopia binary using 7zip."""
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "7z.exe")
    os.system(f"{bin_path} e ./tmp/Growtopia.dmg Growtopia.app/Contents/MacOS/Growtopia -otmp -aoa")


def extract_growtopia_assets() -> None:
    """Extract Growtopia assets using 7zip."""
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "7z.exe")
    os.system(f"{bin_path} x ./tmp/Growtopia.dmg Growtopia.app/Contents/Resources/game -otmp/temp_extracted -aoa")
    shutil.copytree("tmp/temp_extracted/Growtopia.app/Contents/Resources/game", "tmp/game", dirs_exist_ok=True)
    shutil.rmtree("tmp/temp_extracted")


def load_previous_version_data(version: str | bytes) -> list[str]:
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


def remove_non_ascii(text: str) -> str:
    """Remove non-ASCII characters from the text."""
    return ''.join([s for s in text if 31 < ord(s) < 127])


def extract_items(data: str) -> list[str]:
    """Extract and clean item data from the binary."""
    items: list[str] = []

    for line in data.split("\n"):
        line = line.replace("ITEM_ID_", "splitherelolITEM_ID_")

        for part in line.split("splitherelol"):
            if "ITEM_ID_" in part:
                if len(part) > 500:
                    part = part.split("solid")[0]
                # Remove last character
                items.append(remove_non_ascii(part[:-1]))

    # Clean the last item
    items[-1] = items[-1][:items[-1].find("ALIGNMENT")]
    return items


def extract_item_icons(file_list: list[str], source_folder: str = "tmp/game", destination_folder: str = "tmp/dest") -> None:
    os.makedirs(destination_folder, exist_ok=True)
    for file_name in file_list:
        destination_file = os.path.join(destination_folder, file_name)
        # check if file_icon exists and copy it instead
        if "_icon" not in file_name:
            icon_file_name = file_name.replace(".rttex", "_icon.rttex")
            icon_source_file = os.path.join(source_folder, icon_file_name)
            if os.path.exists(icon_source_file):
                file_name = icon_file_name
        source_file = os.path.join(source_folder, file_name)
        if os.path.exists(source_file):
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            shutil.copy2(source_file, destination_file)
            print(f"Copied: {file_name}")
        else:
            print(f"File not found: {file_name}")


def extract_version(data: str) -> str:
    """Extract version information from the binary."""
    version_start = data.find("www.growtopia1.com") + 18
    version_info = data[version_start:data.find("Growtopia", version_start)]
    return remove_non_ascii(version_info)


def save_new_version_data(version: str, items: list[str]) -> None:
    """Save new version item data to a file."""
    with open(f"bol_{version}.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(items))


def compare_new_items(items: list[str], old_items: list[str]) -> list[str]:
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
