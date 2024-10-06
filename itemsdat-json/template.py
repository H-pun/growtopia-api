# Special field size constants.
STRING = -1
STRING_XOR = -2


def field(size: int, *, version: int = 0) -> dict:
    return {"size": size, "version": version}


# Each field is a dictionary containing two keys: size and version. Fields starting with 
# an underscore are skipped when parsing.
def get_generic_template() -> dict:
    return {
        "id": field(4),
        "properties": field(2),
        "type": field(1),
        "material": field(1),
        "name": field(STRING_XOR),
        "file_name": field(STRING),
        "file_hash": field(4),
        "visual_type": field(1),
        "cook_time": field(4),
        "tex_x": field(1),
        "tex_y": field(1),
        "storage_type": field(1),
        "layer": field(1),
        "collision_type": field(1),
        "hardness": field(1),
        "regen_time": field(4),
        "clothing_type": field(1),
        "rarity": field(2),
        "max_hold": field(1),
        "alt_file_path": field(STRING),
        "alt_file_hash": field(4),
        "anim_ms": field(4),
        "pet_name": field(STRING, version=4),
        "pet_prefix": field(STRING, version=4),
        "pet_suffix": field(STRING, version=4),
        "pet_ability": field(STRING, version=5),
        "seed_base": field(1),
        "seed_over": field(1),
        "tree_base": field(1),
        "tree_over": field(1),
        "bg_col": field(4),
        "fg_col": field(4),
        "seed1": field(2),
        "seed2": field(2),
        "bloom_time": field(4),
        "anim_type": field(4, version=7),
        "anim_string": field(STRING, version=7),
        "anim_tex": field(STRING, version=8),
        "anim_string2": field(STRING, version=8),
        "dlayer1": field(4, version=8),
        "dlayer2": field(4, version=8),
        "properties2": field(2, version=9),
        "_unk": field(62, version=9),
        "tile_range": field(4, version=10),
        "pile_range": field(4, version=10),
        "custom_punch": field(STRING, version=11),
        "_unk2": field(13, version=12),
        "clock_div": field(4, version=13),
        "parent_id": field(4, version=14),
        "_unk3": field(25, version=15),
        "alt_sit_path": field(STRING, version=15),
        "_unk4": field(STRING, version=16),
        "_unk5": field(4, version=17),
        "_unk6": field(4, version=18),
    }
