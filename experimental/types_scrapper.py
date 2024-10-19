import os
import json
import requests
from bs4 import BeautifulSoup


def get_item_data(item_name):
    response = requests.get(f"https://growtopia.fandom.com/wiki/{item_name}")
    gt_card = BeautifulSoup(response.text, "html.parser").select_one("div.gtw-card.item-card > table")
    el = gt_card.find('td')
    sprite = el.find('img')['src']
    title = el.get_text(strip=True).split('-')[0]
    return title, sprite


def get_item_types(folder_path):
    item_types = []
    # Get all files in the specified folder
    for filename in os.listdir(folder_path):
        # Split the filename into ID and name
        parts = filename.split('_')
        id = int(parts[0])  # Convert the ID to an integer
        # Join the rest as name and remove extension
        name, _ = os.path.splitext(' '.join(parts[1:]))
        # Create a dictionary for the item
        item = {
            "id": id,
            "name": name,
            "flag": ""  # Set flag to empty string by default
        }
        item_types.append(item)
    # Sort the item_types list by ID
    item_types.sort(key=lambda x: x["id"])
    return item_types


# Define the path to the assets folder
assets_folder = "assets"
os.makedirs(assets_folder, exist_ok=True)

# Load JSON data from file and print it
with open("types_template.json", "r") as file:
    data = json.load(file)

# Print loaded JSON data
for item in data["Types"]:
    # Skip if the item_name is seed or gems
    if not item["item_name"]: continue
    title, sprite = get_item_data(item["item_name"])
    img_response = requests.get(sprite)
    if img_response.status_code == 200:
        # Create a file path using the title
        file_path = os.path.join(assets_folder, f"{item["id"]}_{title.replace(' ', '_')}.png")  # Change extension if needed
        with open(file_path, 'wb') as f:
            # Write the image content to the file
            f.write(img_response.content)
        print(f"Image saved as: {file_path}")
    else:
        print("Failed to retrieve the image.")

# Specify your folder path
result = get_item_types(assets_folder)

# Create the final JSON structure
final_result = {"item_types": result}

# Optionally, print or save the result as JSON
# print(json.dumps(final_result, indent=4))  # Print the result nicely formatted
with open("output.json", "w") as outfile:
    json.dump(final_result, outfile, indent=4)  # Save to a JSON file
