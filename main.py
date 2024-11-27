from PIL import Image
import interpolation as inter
import os

def calculate_luminance(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b

def bmp_to_luminance_txt(bmp_path, txt_path):
    image = Image.open(bmp_path)
    width, height = image.size
    pixels = image.load()

    with open(txt_path, 'w') as txt_file:
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y][:3]
                luminance = calculate_luminance(r, g, b)
                txt_file.write(f"{luminance:.0f},")
            txt_file.write("\n")

def luminance_txt_to_bmp(txt_path, bmp_path):
    with open(txt_path, 'r') as txt_file:
        lines = txt_file.readlines()
        height = len(lines)
        width = len(lines[0].split(',')) - 1

    image = Image.new("RGB", (width, height))
    pixels = image.load()

    with open(txt_path, 'r') as txt_file:
        for y, line in enumerate(txt_file):
            luminance_values = line.split(',')[:-1]
            for x, luminance in enumerate(luminance_values):
                luminance = int(luminance)
                pixels[x, y] = (luminance, luminance, luminance)

    image.save(bmp_path)
def comp(uncmprsd_file_name, cmprsd_file_name):
    with open(uncmprsd_file_name, "r",encoding="utf-8") as uncompressed_file, open(cmprsd_file_name, "w",encoding="utf-8") as compressed_file:
        for line in uncompressed_file:
            for ch in line.split(','):
                if ch.strip().isdigit():
                    num = int(ch)
                    if num != 10 and num != 3:
                        compressed_file.write(chr(num))

def decomp(cmprsd_file_name, output_file_name):
    with open(output_file_name, "w",encoding="utf-8") as uncompressed_file, open(cmprsd_file_name, "r",encoding="utf-8") as compressed_file:
        count = 0
        line = 0
        while True:
            ch = compressed_file.read(1)
            if not ch:
                break
            uncompressed_file.write(f"{ord(ch)},")
            count += 1
            if count == 800:
                uncompressed_file.write("\n")
                line += 1
                count = 0
        print(f"Line: {line}")

if __name__ == "__main__":
    
    folder_ascii = "ascii"
    # create folder if not exists
    if not os.path.exists(folder_ascii):
        os.makedirs(folder_ascii)
    
    original_bmp = 'xp_800_600.bmp'
    unencoded_txt = os.path.join(folder_ascii, 'uncompressed_temp.txt')
    compressed_txt = os.path.join(folder_ascii, 'compressed_temp.txt')
    
    output_txt = os.path.join(folder_ascii, 'output.txt')
    output_bmp = os.path.join(folder_ascii, 'output.bmp')
    
    bmp_to_luminance_txt(original_bmp, unencoded_txt)
    comp(unencoded_txt, compressed_txt)
    decomp(compressed_txt, output_txt)
    luminance_txt_to_bmp(output_txt, output_bmp)
    inter.interpolation(original_bmp, 2)
    