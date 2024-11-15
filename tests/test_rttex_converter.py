import hashlib
from unittest.mock import patch
from PIL import Image, ImageChops
from growtopia.rttex_converter import rttex_unpack, rttex_pack

def get_file_hash(content):
    hasher = hashlib.sha256()
    hasher.update(content)
    return hasher.hexdigest()

def files_are_similar(content1, content2):
    return get_file_hash(content1) == get_file_hash(content2)
                                                    
def test_rttex_unpack():
    with open("tests/data/tiles_page1.rttex", "rb") as f:
        data = f.read()

    unpacked = rttex_unpack(data)
    img_test = Image.open("tests/data/tiles_page1.png")
    img_result = Image.open(unpacked)

    diff = ImageChops.difference(img_test, img_result)

    assert diff.getbbox() is None

# TODO: find a way to test rttex_pack
# def test_rttex_pack():
#     with open("tests/data/tiles_page1.png", "rb") as f:
#         data = f.read()

#     packed = rttex_pack(data)
#     hash_packed = get_file_hash(packed.getvalue())

    
#     with open("tests/data/tiles_page1.rttex", "rb") as f:
#         assert get_file_hash(f.read()) == hash_packed
