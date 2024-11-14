from pprint import pprint
from unittest.mock import patch

from growtopia.growtopia_info import search_item, GrowtopiaItem
from tests.utils.growtopia_info import assert_item_data


def test_wiki_search():
    data = search_item("angel")

    assert isinstance(data, list)
    assert "Title" in data[0]
    assert "Url" in data[0]


def test_wiki_search_not_found():
    data = search_item("notfound")

    assert data == []


def test_wiki_item():
    item = GrowtopiaItem("angel").get_item_data()

    assert_item_data(item)
    assert "Url" in item


def test_wiki_item_rarity_number():
    item = GrowtopiaItem("dirt").get_item_data()

    assert isinstance(item["Rarity"], int)


def test_wiki_item_rarity_none():
    item = GrowtopiaItem("angel").get_item_data()

    assert isinstance(item["Rarity"], str)
    assert item["Rarity"] == "None"


def test_wiki_item_has_sub_type():
    item = GrowtopiaItem("angel wing").get_item_data()

    assert len(item["Type"]) == 2
    assert "Clothes" in item["Type"]
    assert "Back" in item["Type"]


def test_wiki_item_has_sub_items():
    item = GrowtopiaItem("ancestral lens").get_item_data(include_subitems=True)

    assert "SubItems" in item
    assert len(item["SubItems"]) > 1
    for subitem in item["SubItems"]:
        assert_item_data(subitem)
