# growtopia-tools
Unofficial 🌲 Growtopia API, featuring advanced tools for accessing item data, sprites, and various other resources.

## Installing the Library

You can easily install `growtopia-api` from PyPI using the following command:

```console
$ pip install growtopia-api
```

The `growtopia-api` library officially supports Python 3.10 and above.

## Example Code

### Growtopia Info

To search for an item in the Growtopia wiki, you can use the following example:

```python
from pprint import pprint
from growtopia.growtopia_info import search_item

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

**Note:** The `allow_partial_match` feature is still experimental and may occasionally return unexpected results. If you encounter any issues, please open an issue on the project's GitHub repository.

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

#### Growtopia Detailed Item Information

To get detailed item information, you can use the following example:

```python
from pprint import pprint
from growtopia.growtopia_info import GrowtopiaItem

item_name = "Angel"
item = GrowtopiaItem(item_name)

# To get full data
pprint(item.get_item_data())

# To get sprite only
pprint(item.get_item_sprite())
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
  "Sprite": {
    "Item": "https://static.wikia.nocookie.net/growtopia/images/8/8f/ItemSprites.png/...",
    "Seed": "https://static.wikia.nocookie.net/growtopia/images/9/9c/SeedSprites.png/...",
    "Tree": "https://static.wikia.nocookie.net/growtopia/images/e/e5/TreeSprites.png/..."
  },
  "URL": "https://growtopia.fandom.com/wiki/Angel_Wings"    
}
```
If you use only `get_item_sprite`, it will only output the sprite's value and it has the property to include the title.

The `get_item_sprite` function accepts the following parameters:

- `include_title` (bool, optional): If set to `True`, the output will include the title of the item along with the sprite. Defaults to `False`.

Example:

```python
# To get sprite only
pprint(item.get_item_sprite(include_title=Trues))
```

This will output:

```json
{
    "Title": "Angel Wings",
    "Sprite": {
        "Item": "https://static.wikia.nocookie.net/growtopia/images/8/8f/ItemSprites.png/...",
        "Seed": "https://static.wikia.nocookie.net/growtopia/images/9/9c/SeedSprites.png/...",
        "Tree": "https://static.wikia.nocookie.net/growtopia/images/e/e5/TreeSprites.png/..."
    }
}
```

### Items.dat Parser (Docs coming soon)

The `growtopia-api` includes a Python items.dat parser from [gt-itemsdat-json](https://github.com/houzeyhoo/gt-itemsdat-json) by @houzeyhoo. This tool allows you to parse and manipulate the items.dat file used in Growtopia.

### Upcoming Items Dataminer (Docs coming soon)

The `growtopia-api` also includes an upcoming items dataminer from [Dataminer](https://github.com/Bolwl/Dataminer) by @Bolwl. This tool helps you to discover upcoming items in Growtopia. 

## Acknowledgements

- Python items.dat parser from [gt-itemsdat-json](https://github.com/houzeyhoo/gt-itemsdat-json) by @houzeyhoo
- Base wiki scrapper from [growtopia-info](https://github.com/Gabrielbjb/growtopia-info) by @Gabrielbjb 
- Upcoming items [Dataminer](https://github.com/Bolwl/Dataminer) by @Bolwl
- GrowDocs by [@iProgramMC](https://github.com/iProgramMC/GrowDocs) (forked from [@GrowtopiaNoobs](https://github.com/GrowtopiaNoobs/GrowDocs))

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or would like to contribute code, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.