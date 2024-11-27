import numpy as np
from PIL import Image
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





def load_image_from_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    rows = data.strip().split('\n')
    image = []
    for row in rows:
        row_values = row.split(',')
        int_values = []
        for value in row_values:
            if value:
                int_values.append(int(value))
        image.append(int_values)
    image = np.array(image, dtype=np.uint8)
    return image

def bilinear_interpolation(image, scale_factor):
    original_height, original_width = image.shape
    new_height, new_width = original_height * scale_factor, original_width * scale_factor
    new_image = np.zeros((new_height, new_width), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            x = i / scale_factor
            y = j / scale_factor

            x1 = int(x)
            y1 = int(y)
            x2 = min(x1 + 1, original_height - 1)
            y2 = min(y1 + 1, original_width - 1)

            r1 = (x2 - x) * image[x1, y1] + (x - x1) * image[x2, y1]
            r2 = (x2 - x) * image[x1, y2] + (x - x1) * image[x2, y2]

            new_image[i, j] = int((y2 - y) * r1 + (y - y1) * r2)

    return new_image

def save_image_to_bmp(image, file_path):
    img = Image.fromarray(image)
    img.save(file_path)
    
    
    
def downscale_image(full_image_path, downscale_factor, output_image_path):
    image = Image.open(full_image_path)
    width, height = image.size
    new_width = width // downscale_factor
    new_height = height // downscale_factor
    image = image.resize((new_width, new_height))
    image.save(output_image_path)
    
    
def np_array_to_txt(image, txt_path):
    with open(txt_path, 'w') as txt_file:
        for row in image:
            for value in row:
                txt_file.write(f"{value},")
            txt_file.write("\n")


def interpolation(original_bmp = 'xp_800_600.bmp', scale_factor = 2):
    folder_name = 'interpolation'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    

    not_compressed_bmp =  original_bmp
    not_compressed_txt = os.path.join(folder_name, f"{os.path.splitext(original_bmp)[0]}_not_compressed.txt")
    compressed_bmp = os.path.join(folder_name, f"{os.path.splitext(original_bmp)[0]}_compressed.bmp")
    compressed_txt = os.path.join(folder_name, f"{os.path.splitext(original_bmp)[0]}_compressed.txt")
    resulting_txt = os.path.join(folder_name, f"{os.path.splitext(original_bmp)[0]}_decompressed.txt")
    output_bmp_file = os.path.join(folder_name, f"{os.path.splitext(original_bmp)[0]}_decompressed.bmp")
    bmp_to_luminance_txt(not_compressed_bmp, not_compressed_txt)
    downscale_image(not_compressed_bmp, scale_factor, compressed_bmp)
    bmp_to_luminance_txt(compressed_bmp, compressed_txt)
    
    
    image = load_image_from_txt(compressed_txt)
    interpolated_image = bilinear_interpolation(image, scale_factor)
    np_array_to_txt(interpolated_image, resulting_txt)
    save_image_to_bmp(interpolated_image, output_bmp_file)



if __name__ == "__main__":
    interpolation()
    print("Done")