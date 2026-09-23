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