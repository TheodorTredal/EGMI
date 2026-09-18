import os
import numpy as np
import tifffile
from PIL import Image

# 1. Stier til flerkanals-TIFF og ut-fil
INPUT_FILE = "images/test_bilde_ROSIE.tiff"  # Oppdater denne med din filsti!
OUTPUT_FILE = "TEST_IMAGE_rgb_overlay_DAPI_CD45_ECAD.png"

# Kanalindekser
CH_BLUE = 0   # DAPI
CH_RED = 1    # CD45
CH_GREEN = 35 # ECad

# Tillat at Pillow lagrer og behandler ekstremt store bilder uten feil
Image.MAX_IMAGE_PIXELS = None


def normalize_to_8bit(img, gain=1.0, p_low=0.2, p_high=99.9):
    """Spreder intensiteten over 0-255 skalaen og påfører gain for å balansere fargene."""
    p_low_val, p_high_val = np.percentile(img, (p_low, p_high))
    if p_high_val == p_low_val:
        return np.zeros(img.shape, dtype=np.uint8)
    
    clipped = np.clip(img, p_low_val, p_high_val)
    norm = (clipped - p_low_val) / (p_high_val - p_low_val)
    
    # Påfør gain og hindre overskridelse av 255
    scaled = np.clip(norm * gain * 255.0, 0, 255)
    return scaled.astype(np.uint8)


def load_channel_from_tiff(file_path, channel_idx):
    """Leser kun ut spesifisert kanal ved hjelp av memory mapping."""
    print(f"Leser ut kanal {channel_idx} fra {os.path.basename(file_path)}...")
    store = tifffile.imread(file_path, aszarr=False, out="memmap")

    # Sjekk dimensjonsrekkefølge (kanaler først eller sist)
    if store.ndim == 3 and store.shape[0] < store.shape[1]:
        # Shape er [Kanaler, Høyde, Bredde]
        return np.array(store[channel_idx], copy=True)
    elif store.ndim == 3:
        # Shape er [Høyde, Bredde, Kanaler]
        return np.array(store[..., channel_idx], copy=True)
    else:
        raise ValueError(f"Forventet et 3D-bilde med kanaler, men fikk dimensjoner: {store.shape}")


# 2. Leser inn de tre spesifikke kanalene fra 50-kanalers bildet
dapi_blue = load_channel_from_tiff(INPUT_FILE, CH_BLUE)
cd45_red = load_channel_from_tiff(INPUT_FILE, CH_RED)
ecad_green = load_channel_from_tiff(INPUT_FILE, CH_GREEN)

print("Justerer kontrast og fargebalanse for hver enkelt kanal...")
# Her justerer du gain og persentiler per fargekanal:
r_8bit = normalize_to_8bit(cd45_red, gain=0.5, p_low=0.1, p_high=99.99)   # Rød (CD45)
g_8bit = normalize_to_8bit(ecad_green, gain=0.5, p_high=99.95) # Grønn (ECad)
b_8bit = normalize_to_8bit(dapi_blue, gain=2.0, p_high=99.8)  # Blå (DAPI - dempet for å hindre utvasking)

# Frigjør minne fra opprinnelige arrays
del cd45_red, ecad_green, dapi_blue

print("Sammensetter til RGB-bilde (Rød=Kanal 1, Grønn=Kanal 35, Blå=Kanal 0)...")
rgb_array = np.stack([r_8bit, g_8bit, b_8bit], axis=-1)

del r_8bit, g_8bit, b_8bit

print(f"Lagrer sammensatt RGB-bilde til: {OUTPUT_FILE}...")
pil_img = Image.fromarray(rgb_array, mode="RGB")
pil_img.save(OUTPUT_FILE)

print("Ferdig!")