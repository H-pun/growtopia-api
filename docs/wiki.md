## Growtopia Wiki

### Search Item
To search for an item in the Growtopia wiki, you can use the following example:

```python
from pprint import pprint
from growtopia.wiki import search_item

item_name = "Angel"
data = search_item(item_name)
pprint(data)
```

This will output:

```json
[
    {
        "Title": "Angel and Devil",
        "Url": "https://growtopia.fandom.com/wiki/Angel_and_Devil"
    },
    {
        "Title": "Angel of Mercy's Wings",
        "Url": "https://growtopia.fandom.com/wiki/Angel_of_Mercy's_Wings"
    },
    {
        "Title": "Angelic Aura",
        "Url": "https://growtopia.fandom.com/wiki/Angelic_Aura"
    },
    {
        "Title": "Angel Wings",
        "Url": "https://growtopia.fandom.com/wiki/Angel_Wings"
    }
    // Additional results...
]
```

#### Parameters

The `search_item` function accepts the following parameters:

- `item_name` (str): The name of the item to search for.
- `allow_partial_match` (bool, optional): If set to `True`, the search will allow partial matches. Defaults to `True`.
- `show_url` (bool, optional): If set to `True`, the search results will include URLs. Defaults to `True`.

>[!WARNING]
>The `allow_partial_match` feature is still experimental and may occasionally return unexpected results. If you encounter any issues, please open an issue on the project's GitHub repository.

Example usage:

```python
data = search_item(item_name="Angel", allow_partial_match=True, show_url=True)
```

#### Partial Match Example

If `allow_partial_match` is set to `True`, the search can return items like "Digital Dirt" when searching for "Dirt". If set to `False`, it will only return items that start with "Dirt".

Example:

```python
# Partial match enabled
data = search_item(item_name="Dirt", allow_partial_match=True)
# Possible output: ["Digital Dirt", "Dirt", ...]

# Partial match disabled
# Possible output: ["Dirt", ...]
```

### Get Detailed Item Information

To get detailed item information, you can use the following example:

```python
from pprint import pprint
from growtopia.wiki import get_item_data

item_name = "Angel"
item = get_item_data(item_name)
```

This will output:

```json
{
  "Title": "Angel Wings",
  "Description": "Better than a Halo, these will actually let you double jump!",
  "Properties": [
    "This item never drops any seeds.",
    "This item can be transmuted."
  ],
  "Rarity": "None",
  "Type": [
    "Back",
    "Clothes"
  ],
  "Chi": "None",
  "TextureType": "Single",
  "CollisionType": "Full Collision",
  "Hardness": {
    "Fist": 0,
    "Pickaxe": 0,
    "Restore": 0
  },
  "SeedColor": [
    "#EFEFEF",
    "#FFFFFF"
  ],
  "GrowTime": "1h 0m 0s",
  "DefaultGemsDrop": "N/A",
  "Recipe": ["Valentine Loot"],
  "Sprite": {
    "Item": "https://static.wikia.nocookie.net/growtopia/images/8/8f/ItemSprites.png/...",
    "Seed": "https://static.wikia.nocookie.net/growtopia/images/9/9c/SeedSprites.png/...",
    "Tree": "https://static.wikia.nocookie.net/growtopia/images/e/e5/TreeSprites.png/..."
  },
  "URL": "https://growtopia.fandom.com/wiki/Angel_Wings"    
}
```