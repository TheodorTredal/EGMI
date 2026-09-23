import tifffile
import cv2

input_file = "Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
output_file = "HE_for_ROSIE_20x.tif"

print("Leser inn bildet med tifffile...")
img = tifffile.imread(input_file)
print(f"Opprinnelig størrelse: {img.shape}")

# Dersom bildet har en ekstra dimensjon eller feil akser, verifiserer vi H, W, C
if img.ndim == 3 and img.shape[0] == 3:  # Hvis formen er (C, H, W)
    img = img.transpose(1, 2, 0)         # Endre til (H, W, C)

h, w = img.shape[:2]

print("Oppskalerer 2x med cv2.resize...")
# cv2.resize tåler store arrays i minnet så lenge inn/ut er numpy-arrays
img_rosie_input = cv2.resize(img, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)

print(f"Ny dimensjon: {img_rosie_input.shape}")

print(f"Lagrer direkte til {output_file} med tifffile (BigTIFF-støtte)...")
# bigtiff=True sikrer at filer over 4GB blir lagret riktig
tifffile.imwrite(
    output_file, 
    img_rosie_input, 
    photometric='rgb', 
    bigtiff=True,
    compression='zlib'  # Komprimerer for å spare diskplass (valgfritt)
)

print("Ferdig! Bildet er lagret korrekt.")


