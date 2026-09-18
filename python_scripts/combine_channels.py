import os
import numpy as np
from PIL import Image

# 1. Stier til de tre enkeltkanalbildene
INPUT_DIR = "images/stitched_images"
FILE_DAPI = os.path.join(INPUT_DIR, "combined_image_ch0_ROSIE.png")  # Blå
FILE_CD45 = os.path.join(INPUT_DIR, "combined_image_ch1_ROSIE.png")  # Rød
FILE_ECAD = os.path.join(INPUT_DIR, "combined_image_ch35_ROSIE.png")  # Grønn

OUTPUT_FILE = os.path.join(INPUT_DIR, "rgb_overlay_DAPI_CD45_ECAD.png")

# Tillat åpning og lagring av ekstremt store PNG-bilder
Image.MAX_IMAGE_PIXELS = None


def normalize_to_8bit(img):
    """Spreder intensiteten over 0-255 skalaen så bildet blir tydelig."""
    p_low, p_high = np.percentile(img, (0.2, 99.8))
    if p_high == p_low:
        return np.zeros(img.shape, dtype=np.uint8)
    clipped = np.clip(img, p_low, p_high)
    return ((clipped - p_low) / (p_high - p_low) * 255.0).astype(np.uint8)


def load_png_as_array(file_path):
    """Åpner PNG-bilde og konverterer det til en NumPy-matrise."""
    print(f"Leser inn: {os.path.basename(file_path)}")
    with Image.open(file_path) as img:
        return np.asarray(img)


print("Leser inn 2D PNG-enkeltkanalbilder...")
dapi_blue = load_png_as_array(FILE_DAPI)
cd45_red = load_png_as_array(FILE_CD45)
ecad_green = load_png_as_array(FILE_ECAD)

print("Justerer kontrast (normaliserer til 8-bit)...")
r_8bit = normalize_to_8bit(cd45_red)
g_8bit = normalize_to_8bit(ecad_green)
b_8bit = normalize_to_8bit(dapi_blue)

# Frigjør minne
del cd45_red, ecad_green, dapi_blue

print("Sammensetter fargekanaler (R=CD45, G=ECad, B=DAPI)...")
rgb_array = np.stack([r_8bit, g_8bit, b_8bit], axis=-1)

del r_8bit, g_8bit, b_8bit

print(f"Lagrer RGB-bilde til {OUTPUT_FILE}...")
pil_img = Image.fromarray(rgb_array, mode="RGB")
pil_img.save(OUTPUT_FILE)

print("Ferdig!")