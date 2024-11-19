from unittest.mock import patch

from growtopia.wiki import search_item, get_item_data
from tests.utils.wiki import assert_item_data


def test_wiki_search():
    data = search_item("Bountiful Corpse Flower")
    assert len(data) > 0
    assert "Title" in data[0]
    assert "Url" in data[0]
    assert all("Growganoth" not in item["Title"] and "Legendary Quest" not in item["Title"] for item in data)
    assert all("bountiful" in item["Title"].lower() for item in data)


def test_wiki_search_not_found():
    data = search_item("notfound")
    assert data == []


def test_wiki_search_disable_partial_match():
    data = search_item("Bountiful Corpse Flower", allow_partial_match=False)
    assert len(data) > 0
    assert all("Growganoth" not in item["Title"] and "Legendary Quest" not in item["Title"] for item in data)
    assert all(item["Title"].startswith("Bountiful") for item in data)


def test_wiki_search_disable_url():
    data = search_item("angel", show_url=False)
    assert all("Url" not in item for item in data)


def test_wiki_item():
    item = get_item_data("Bountiful Corpse Flower")
    assert_item_data(item)
    assert "Url" in item


def test_wiki_item_rarity_number():
    item = get_item_data("dirt")
    assert isinstance(item["Rarity"], int)


def test_wiki_item_rarity_none():
    item = get_item_data("angel")
    assert isinstance(item["Rarity"], str)
    assert item["Rarity"] == "None"


def test_wiki_item_has_sub_type():
    item = get_item_data("angel wing")
    assert len(item["Type"]) == 2
    assert "Clothes" in item["Type"]
    assert "Back" in item["Type"]


def test_wiki_item_has_sub_items():
    item = get_item_data("Bountiful Jungle Temple", include_subitems=True)
    assert_item_data(item)
    assert "SubItems" in item
    assert len(item["SubItems"]) > 1
    for subitem in item["SubItems"]:
        assert_item_data(subitem)
