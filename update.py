import os
import shutil

metatiles_filename = "metatiles.bin"
palette_dir = "palettes"

def adjust_metatiles():
    with open(metatiles_filename, "rb") as file:
        data = file.read()

    tiles = list(data)

    for i in range(0, len(tiles), 2):
        tile_value = (tiles[i + 1] << 8) | tiles[i]
        if tile_value != 0:
            tile_value += 0x200
            tiles[i] = tile_value & 0xFF
            tiles[i + 1] = (tile_value >> 8) & 0xFF

    new_data = bytes(tiles)

    with open("metatiles_adjusted.bin", "wb") as file:
        file.write(new_data)

    print("metatiles.bin upgrade to use in secondary tile")

def create_empty_palette(palette_path):
    with open(palette_path, "w") as f:
        f.write("JASC-PAL\n")
        f.write("0100\n")
        f.write("16\n")
        for _ in range(16):
            f.write("0 0 0\n")

def move_palettes():
    for i in range(6):
        src_palette = f"{palette_dir}/{i:02}.pal"
        dst_palette = f"{palette_dir}/{i + 6:02}.pal"
        
        shutil.move(src_palette, dst_palette)
        
        create_empty_palette(src_palette)

    print("Moving palettes 00-05 to 06-11...")


def modify_metatiles():
    with open("metatiles_adjusted.bin", "rb") as file:
        tiles_data = list(file.read())

    for i in range(1, len(tiles_data), 2):
        if i % 2 == 1: 
            palette_info = tiles_data[i]

            palette_index = palette_info >> 4 

            if 0 <= palette_index <= 5:
                new_palette_index = palette_index + 6
                tiles_data[i] = (new_palette_index << 4) | (palette_info & 0x0F) 

    with open("metatiles.bin", "wb") as file:
        file.write(bytes(tiles_data))

    print("Palette mapping complete...")

if __name__ == "__main__":
    adjust_metatiles()
    move_palettes()
    modify_metatiles()
