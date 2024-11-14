def assert_item_data(item):
    assert isinstance(item, dict)
    assert "Title" in item
    assert "Description" in item
    assert "Properties" in item
    assert "Rarity" in item
    assert "Type" in item
    assert "Chi" in item
    assert "TextureType" in item
    assert "CollisionType" in item
    assert "Hardness" in item
    assert "Fist" in item["Hardness"]
    assert "Pickaxe" in item["Hardness"]
    assert "Restore" in item["Hardness"]
    assert "SeedColor" in item
    assert isinstance(item["SeedColor"], list)
    assert all(isinstance(color, str) for color in item["SeedColor"])
    assert "GrowTime" in item
    assert "DefaultGemsDrop" in item
    assert "Sprite" in item
    assert "Item" in item["Sprite"]
    assert "Seed" in item["Sprite"]
    assert "Tree" in item["Sprite"]
