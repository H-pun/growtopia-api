import os
import shutil

# Daftar file yang ingin disalin
file_list = [
    "bf_begchmp_icon.rttex",
    "comhr.rttex",
    "d_aura.rttex",
    "es_egchmp.rttex",
    "gui_board.rttex",
    "gui_board2.rttex",
    "gui_rol_1.rttex",
    "gui_rol_2.rttex",
    "gui_rol_3.rttex",
    "gui_rol_4.rttex",
    "gui_rol_5.rttex",
    "gui_rol_6.rttex",
    "io_rif_icon.rttex",
    "io_rif_wing_icon.rttex",
    "pets/p_tononab.rttex",
    "player_face.rttex",
    "player_hater.rttex",
    "player_pants_monthly1.rttex",
    "st_caura_icon.rttex",
    "player_hair_monthly1.rttex",
    "player_hater_icon.rttex",
    "tiles_gch.rttex",
    "amorkolg.rttex",
    "player_feet_monthly1.rttex",
    "player_longhanditem4.rttex",
    "player_shirt_monthly1.rttex",
    "player_hair5.rttex",
    "player_pants3.rttex",
    "player_feet13.rttex",
    "player_faceitem5.rttex",
    "player_faceitem6.rttex",
    "player_faceitem3.rttex",
    "player_feet15.rttex",
    "player_back3.rttex",
    "player_faceitem4.rttex",
    "player_feet12.rttex",
    "player_feet14.rttex",
    "player_feet10.rttex",
    "player_feet11.rttex",
    "player_feet5.rttex",
    "player_feet7.rttex",
    "player_feet8.rttex",
    "player_feet9.rttex",
    "player_handitem7.rttex",
    "player_feet6.rttex",
    "player_longhanditem1.rttex",
    "player_faceitem2.rttex",
    "player_feet.rttex",
    "player_feet3.rttex",
    "player_longhanditem2.rttex",
    "player_chestitem2.rttex",
    "player_feet4.rttex",
    "player_hair3.rttex",
    "player_faceitem7.rttex",
    "player_feet2.rttex",
    "player_artifact.rttex",
    "player_back2.rttex",
    "player_hair4.rttex",
    "tiles_page17.rttex",
    "player_shirt4.rttex",
    "fish_page1.rttex",
    "player_shirt3.rttex",
    "player_hair.rttex",
    "player_handitem6.rttex",
    "player_faceitem.rttex",
    "player_back.rttex",
    "player_longhanditem3.rttex",
    "player_handitem5.rttex",
    "player_handitem.rttex",
    "player_pants2.rttex",
    "player_hairhair.rttex",
    "player_handitem2.rttex",
    "vilpix.rttex",
    "gd_page2.rttex",
    "player_chestitem.rttex",
    "player_shirt.rttex",
    "player_hair2.rttex",
    "player_hairhair2.rttex",
    "player_handitem3.rttex",
    "player_pants.rttex",
    "stopia_page1.rttex",
    "gd_page1.rttex",
    "player_shirt2.rttex",
    "tiles_page12.rttex",
    "tiles_page9.rttex",
    "player_feet16.rttex",
    "player_handitem4.rttex",
    "tiles_page3.rttex",
    "tiles_page5.rttex",
    "tiles_page10.rttex",
    "tiles_page8.rttex",
    "tiles_page6.rttex",
    "tiles_page11.rttex",
    "tiles_page4.rttex",
    "tiles_page7.rttex",
    "tiles_page13.rttex",
    "tiles_page2.rttex",
    "gd_page3.rttex",
    "tiles_page1.rttex",
    "tiles_page14.rttex",
    "tiles_page15.rttex",
    "tiles_page16.rttex",
    "player_cosmetics3.rttex",
    "player_cosmetics1.rttex",
    "player_cosmetics2.rttex",
]

# Folder sumber dan tujuan
source_folder = "tmp/game"  # Ganti dengan folder sumber
destination_folder = "tmp/dest"  # Ganti dengan folder tujuan

# Pastikan folder tujuan ada, jika tidak ada buat folder
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Loop untuk menyalin file
for file_name in file_list:
    destination_file = os.path.join(destination_folder, file_name)
    if "_icon" not in file_name:
        icon_file_name = file_name.replace(".rttex", "_icon.rttex")
        icon_source_file = os.path.join(source_folder, icon_file_name)
        if os.path.exists(icon_source_file):
            file_name = icon_file_name
    source_file = os.path.join(source_folder, file_name)

    # Cek apakah file ada di folder sumber
    if os.path.exists(source_file):
        # Buat folder jika ada subdirektori dalam nama file
        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
        # Salin file ke folder tujuan
        shutil.copy2(source_file, destination_file)
        print(f"Copied: {file_name}")
    else:
        print(f"File not found: {file_name}")
