# import matplotlib.pyplot as plt
# import numpy as np
# import tifffile

# # Liste over kanalnavn i rekkefølge
# channel_names = [
#     "DAPI", "CD45", "CD68", "CD14", "PD1", "FoxP3", "CD8", "HLA-DR",
#     "PanCK", "CD3e", "CD4", "aSMA", "CD31", "Vimentin", "CD45RO", "Ki67",
#     "CD20", "CD11c", "Podoplanin", "PDL1", "GranzymeB", "CD38", "CD141",
#     "CD21", "CD163", "BCL2", "LAG3", "EpCAM", "CD44", "ICOS", "GATA3",
#     "Gal3", "CD39", "CD34", "TIGIT", "ECad", "CD40", "VISTA", "HLA-A",
#     "MPO", "PCNA", "ATM", "TP63", "IFNg", "Keratin8/18", "IDO1", "CD79a",
#     "HLA-E", "CollagenIV", "CD66"
# ]

# # 1. Les inn bildet
# img = tifffile.imread(
#     'output_results/Registered_HE_HE_PS15.19650-B3_Slide2_20210517_ROSIE.tiff'
# )
# num_channels = img.shape[0]

# print(img.shape)

# # Standard startkanal
# current_channel = 0

# # 2. Sett opp Matplotlib figuren
# fig, ax = plt.subplots(figsize=(8, 8))


# def update_display():
#     """Hjelpefunksjon for å oppdatere visningen med gjeldende kanal og navn"""
#     ax.clear()

#     # Hent og normaliser den valgte kanalen
#     ch_data = img[current_channel, ::3, ::3]
#     max_val = np.max(ch_data)
#     if max_val > 0:
#         ch_data = ch_data / max_val

#     # Hent kanalnavn dersom det finnes i listen
#     name = (
#         channel_names[current_channel]
#         if current_channel < len(channel_names)
#         else "Ukjent marker"
#     )

#     # Vis kanalen i fargetone
#     ax.imshow(ch_data, cmap='gray')
#     ax.set_title(
#         f'{name}\n(Kanal {current_channel} av {num_channels - 1})\nBruk venstre/høyre piltast for å bla',
#         fontsize=12,
#         fontweight='bold',
#     )
#     ax.axis('off')
#     fig.canvas.draw_idle()


# def on_key(event):
#     """Lytter til tastaturtrykk"""
#     global current_channel

#     if event.key == 'right':
#         if current_channel < num_channels - 1:
#             current_channel += 1
#             update_display()

#     elif event.key == 'left':
#         if current_channel > 0:
#             current_channel -= 1
#             update_display()


# # Koble tastaturlytteren til Matplotlib-vinduet
# fig.canvas.mpl_connect('key_press_event', on_key)

# # Vis den første kanalen
# update_display()
# plt.show()


#----------------------------------------------------------------------------------------

# channel_names = [
#     "DAPI", "CD45", "CD68", "CD14", "PD1", "FoxP3", "CD8", "HLA-DR",
#     "PanCK", "CD3e", "CD4", "aSMA", "CD31", "Vimentin", "CD45RO", "Ki67",
#     "CD20", "CD11c", "Podoplanin", "PDL1", "GranzymeB", "CD38", "CD141",
#     "CD21", "CD163", "BCL2", "LAG3", "EpCAM", "CD44", "ICOS", "GATA3",
#     "Gal3", "CD39", "CD34", "TIGIT", "ECad", "CD40", "VISTA", "HLA-A",
#     "MPO", "PCNA", "ATM", "TP63", "IFNg", "Keratin8/18", "IDO1", "CD79a",
#     "HLA-E", "CollagenIV", "CD66"
# ]

# # 0 = DAPI, 1 = CD45, 

# import numpy as np
# from PIL import Image
# import tifffile



# def adjust_contrast(img, p_low=0.2, p_high=99.8, gamma=0.8):
#     """Justerer kontrast og lysstyrke på et kanalbilde for mikroskopi.

#     - p_high: Klipper toppprosenten av verdier (f.eks. 99.8%) så ikke alt blir
#     mørkt pga. få sterke piksler.
#     - gamma: Verdi < 1.0 gjør mørke/svake signalområder lysere og lettere å se.
#     """
#     img = img.astype(np.float32)

#     # Finn lav og høy terskel basert på prosentiler
#     v_min, v_max = np.percentile(img, (p_low, p_high))

#     if v_max > v_min:
#         # Klipp og skaler til 0.0 - 1.0
#         img = np.clip(img, v_min, v_max)
#         img = (img - v_min) / (v_max - v_min)
#     else:
#         img = np.zeros_like(img)

#     # Bruk gammakorreksjon for å heve de svake signalene (f.eks. gamma=0.7 eller 0.8)
#     if gamma != 1.0:
#         img = img**gamma

#     return (img * 255.0).astype(np.uint8)


# # 1. Les inn kanalene
# dapi = tifffile.imread("images/ROI001_035_PS15.19650-B3_DAPI.tif")
# ecad = tifffile.imread("images/ROI001_035_PS15.19650-B3_Ecad.tif")
# cd45 = tifffile.imread("images/ROI001_035_PS15.19650-B3_CD45.tif")

# # 2. Juster kontrast/lysstyrke for hver kanal individuelt
# # (Du kan eksperimentere med p_high f.eks. 99.0 til 99.9, eller gamma 0.5-0.8)
# dapi_adj = adjust_contrast(dapi, p_high=99.5, gamma=0.7)
# ecad_adj = adjust_contrast(ecad, p_high=99.5, gamma=0.7)
# cd45_adj = adjust_contrast(cd45, p_high=99.5, gamma=0.7)

# # 3. Sett sammen til RGB (Rød: CD45, Grønn: Ecad, Blå: DAPI)
# rgb_array = np.stack([cd45_adj, ecad_adj, dapi_adj], axis=-1)

# # 4. Konverter til PIL og lagre som PDF
# pil_img = Image.fromarray(rgb_array, mode="RGB")
# pil_img.save("ROI001_035_RGB_bright.pdf", "PDF", resolution=300.0)

# print("Lagret ROI001_035_RGB_bright.pdf med økt lysstyrke!")

#----------------------------------------------------------------------------------------


# import tifffile
# import numpy as np

# file_path = "Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"

# # 1. Les inn bildematrisen
# img = tifffile.imread(file_path)
# print("Bilde-shape:", img.shape)

# # 2. Sjekk metadata for pikselstørrelse (µm/px)
# with tifffile.TiffFile(file_path) as tif:
#     for page in tif.pages:
#         # Sjekk om OME-XML eller ImageDescription inneholder skaleringsdata
#         description = page.tags.get('ImageDescription')
#         if description:
#             desc_text = str(description.value)
#             print("\n--- Funnet metadata i ImageDescription ---")
            
#             # Søk etter typiske nøkkelord for skala
#             for line in desc_text.split('\n'):
#                 if any(k in line.lower() for k in ['scaling', 'pixel', 'mpp', 'micron', 'sizeX', 'resolution']):
#                     print(line)

#         # Sjekk direkte XResolution og YResolution hvis tilstede
#         x_res = page.tags.get('XResolution')
#         unit = page.tags.get('ResolutionUnit')
#         if x_res and unit:
#             print(f"\nXResolution: {x_res.value}, Enhet: {unit.value}")












# import cv2
# import matplotlib.pyplot as plt

# file_path = "Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"

# # Les bildet
# img = cv2.imread(file_path)
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # Hent et utsnitt fra midten av vevet
# h, w, _ = img_rgb.shape
# crop = img_rgb[h // 2 : h // 2 + 500, w // 2 : w // 2 + 500]

# # Vis utsnittet med aksenumre
# plt.figure(figsize=(8, 8))
# plt.imshow(crop)
# plt.title("Utsnitt 500x500 px – Sjekk diameter på cellekjerner")
# plt.xlabel("Piksler")
# plt.ylabel("Piksler")
# plt.grid(True, which='both', color='white', linestyle='--', linewidth=0.5)
# plt.show()



# import tifffile
# import cv2

# input_file = "Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
# output_file = "HE_for_ROSIE_20x.tif"

# print("Leser inn bildet med tifffile...")
# img = tifffile.imread(input_file)
# print(f"Opprinnelig størrelse: {img.shape}")

# # Dersom bildet har en ekstra dimensjon eller feil akser, verifiserer vi H, W, C
# if img.ndim == 3 and img.shape[0] == 3:  # Hvis formen er (C, H, W)
#     img = img.transpose(1, 2, 0)         # Endre til (H, W, C)

# h, w = img.shape[:2]

# print("Oppskalerer 2x med cv2.resize...")
# # cv2.resize tåler store arrays i minnet så lenge inn/ut er numpy-arrays
# img_rosie_input = cv2.resize(img, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)

# print(f"Ny dimensjon: {img_rosie_input.shape}")

# print(f"Lagrer direkte til {output_file} med tifffile (BigTIFF-støtte)...")
# # bigtiff=True sikrer at filer over 4GB blir lagret riktig
# tifffile.imwrite(
#     output_file, 
#     img_rosie_input, 
#     photometric='rgb', 
#     bigtiff=True,
#     compression='zlib'  # Komprimerer for å spare diskplass (valgfritt)
# )

# print("Ferdig! Bildet er lagret korrekt.")






# # if __name__ == "__main__":

#     pass







import numpy as np
from PIL import Image
import tifffile


def adjust_contrast(img, p_low=0.2, p_high=99.8, gamma=0.8):
    """Justerer kontrast og lysstyrke på et kanalbilde for mikroskopi."""
    img = img.astype(np.float32)

    v_min, v_max = np.percentile(img, (p_low, p_high))

    if v_max > v_min:
        img = np.clip(img, v_min, v_max)
        img = (img - v_min) / (v_max - v_min)
    else:
        img = np.zeros_like(img)

    if gamma != 1.0:
        img = img**gamma

    return (img * 255.0).astype(np.uint8)


def generate_rgb_from_multichannel(
    tiff_path,
    output_path,
    channel_names,
    red_channel="CD45",
    green_channel="ECad",
    blue_channel="DAPI",
    p_high=99.5,
    gamma=0.7,
):
    """Leser inn et flerkanals TIFF-bilde og genererer et RGB-bilde (eller PDF)

    basert på tre spesifikke markører.
    """
    # 1. Finn indeksene til de ønskede markørene
    r_idx = channel_names.index(red_channel)
    g_idx = channel_names.index(green_channel)
    b_idx = channel_names.index(blue_channel)

    # 2. Les inn flerkanalsbildet (forventer form (kanaler, høyde, bredde))
    multi_img = tifffile.imread(tiff_path)

    # Hent ut de spesifikke kanalene
    red_img = multi_img[r_idx]
    green_img = multi_img[g_idx]
    blue_img = multi_img[b_idx]

    # 3. Juster kontrast/lysstyrke for hver kanal individuelt
    red_adj = adjust_contrast(red_img, p_high=p_high, gamma=gamma)
    green_adj = adjust_contrast(green_img, p_high=p_high, gamma=gamma)
    blue_adj = adjust_contrast(blue_img, p_high=p_high, gamma=gamma)

    # 4. Sett sammen til RGB (Rød, Grønn, Blå)
    rgb_array = np.stack([red_adj, green_adj, blue_adj], axis=-1)

    # 5. Konverter til PIL og lagre som PDF (eller .png/.tif avhengig av filending)
    pil_img = Image.fromarray(rgb_array, mode="RGB")

    if output_path.lower().endswith(".pdf"):
        pil_img.save(output_path, "PDF", resolution=300.0)
    else:
        pil_img.save(output_path)

    print(f"Lagret RGB-bilde til {output_path}!")


# --- Eksempel på bruk ---

channel_names = [
    "DAPI",
    "CD45",
    "CD68",
    "CD14",
    "PD1",
    "FoxP3",
    "CD8",
    "HLA-DR",
    "PanCK",
    "CD3e",
    "CD4",
    "aSMA",
    "CD31",
    "Vimentin",
    "CD45RO",
    "Ki67",
    "CD20",
    "CD11c",
    "Podoplanin",
    "PDL1",
    "GranzymeB",
    "CD38",
    "CD141",
    "CD21",
    "CD163",
    "BCL2",
    "LAG3",
    "EpCAM",
    "CD44",
    "ICOS",
    "GATA3",
    "Gal3",
    "CD39",
    "CD34",
    "TIGIT",
    "ECad",
    "CD40",
    "VISTA",
    "HLA-A",
    "MPO",
    "PCNA",
    "ATM",
    "TP63",
    "IFNg",
    "Keratin8/18",
    "IDO1",
    "CD79a",
    "HLA-E",
    "CollagenIV",
    "CD66",
]

# Kjør funksjonen på 50-kanals filen din:
generate_rgb_from_multichannel(
    tiff_path="images/test_bilde_ROSIE.tiff",
    output_path="images/test_bilde_ROSIE_RBG_CD45_ECad_DAPI.pdf",
    channel_names=channel_names,
    red_channel="CD45",
    green_channel="ECad",
    blue_channel="DAPI",
    p_high=99.5,
    gamma=0.7,
)