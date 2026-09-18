from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tifffile


def get_channel_pixels(image_path, channel_names=None, target_channel=None):
    """Leser inn et TIFF-bilde og returnerer alle piksler som en 1D numpy-array.

    Håndterer både 2D-bilder (enkeltkanal) og 3D-bilder (flerkanal).
    """
    img = tifffile.imread(image_path)

    # Tilfelle 1: Bildet er 2D (f.eks. uthentet enkeltkanal)
    if img.ndim == 2:
        return img.flatten()

    # Tilfelle 2: Bildet er 3D (flerkanal, f.eks. (50, H, W))
    elif img.ndim == 3:
        if channel_names is None or target_channel is None:
            raise ValueError(
                "Må oppgi channel_names og target_channel for 3D-bilder."
            )
        idx = channel_names.index(target_channel)
        return img[idx].flatten()

    else:
        raise ValueError(f"Uventet bildeformat: {img.shape}.")


def plot_single_image_histogram(
    image_path,
    channel_names=None,
    target_channel="DAPI",
    title="Histogram",
    color="blue",
    bins=100,
    log_scale=True,
    output_path="histogram.png",
):
    """Genererer og lagrer et histogram for et TIFF-bilde."""
    print(f"Henter data fra: {image_path}...")
    pixels = get_channel_pixels(image_path, channel_names, target_channel)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot histogram med normering
    sns.histplot(
        pixels, bins=bins, color=color, ax=ax, kde=False, stat="density"
    )

    ax.set_title(
        f"{title} – Kanal: {target_channel}", fontsize=14, fontweight="bold"
    )
    ax.set_xlabel("Pixel intensity")
    ax.set_ylabel("Density (Normalized)")

    if log_scale:
        ax.set_yscale("log")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Lagret histogram til {output_path}")


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

# Kjør for én fil av gangen:

# # # 1. ROSIE
# plot_single_image_histogram(
#     image_path="Registered_HE_HE_PS15.19650-B3_Slide2_20210517_ROSIE_1_channel1.tiff",
#     channel_names=channel_names,
#     target_channel="CD45",
#     title="ROSIE Output",
#     color="blue",
#     output_path="ROSIE_CD45_histogram.png",
# )

# 2. IMC
# plot_single_image_histogram(
#     image_path="path/to/imc_image.tif",
#     channel_names=channel_names,
#     target_channel="CD45",
#     title="IMC",
#     color="green",
#     output_path="IMC_CD45_histogram.png",
# )

# X 3. IF
plot_single_image_histogram(
    image_path="images/ROI001_035_PS15.19650-B3_CD45.tif",
    channel_names=channel_names,
    target_channel="CD45",
    title="IF",
    color="orange",
    output_path="IF_DAPI_histogram.png",
)






# from pathlib import Path
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# import tifffile


# def get_channel_pixels(image_path, channel_names=None, target_channel=None):
#     """Leser inn et TIFF-bilde og returnerer alle piksler som en 1D numpy-array."""
#     img = tifffile.imread(image_path)

#     if img.ndim == 2:
#         return img.flatten()
#     elif img.ndim == 3:
#         if channel_names is None or target_channel is None:
#             raise ValueError(
#                 "Må oppgi channel_names og target_channel for 3D-bilder."
#             )
#         idx = channel_names.index(target_channel)
#         return img[idx].flatten()
#     else:
#         raise ValueError(f"Uventet bildeformat: {img.shape}.")


# def get_dataset_pixels(path_input, channel_names=None, target_channel="CD45"):
#     """Henter piksler fra enten en enkeltfil eller alle TIFF-filer i en mappe."""
#     path = Path(path_input)

#     # Tilfelle 1: Hvis stien er en enkelt fil
#     if path.is_file():
#         return get_channel_pixels(path, channel_names, target_channel)

#     # Tilfelle 2: Hvis stien er en mappe (itererer over alle TIFF-filer)
#     elif path.is_dir():
#         all_pixels = []
#         # Finner alle .tif og .tiff filer i mappen
#         image_paths = sorted(
#             list(path.glob("*.tif")) + list(path.glob("*.tiff"))
#         )

#         if not image_paths:
#             raise FileNotFoundError(f"Ingen TIFF-filer funnet i {path_input}")

#         print(
#             f"Leser {len(image_paths)} bilder fra mappen: {path_input}..."
#         )
#         for img_path in image_paths:
#             pixels = get_channel_pixels(img_path, channel_names, target_channel)
#             all_pixels.append(pixels)

#         return np.concatenate(all_pixels)

#     else:
#         raise FileNotFoundError(f"Ugyldig sti: {path_input}")


# def plot_combined_histogram(
#     datasets,
#     channel_names=None,
#     target_channel="CD45",
#     bins=100,
#     log_scale=True,
#     output_path="combined_histogram.png",
# ):
#     """Genererer et samlet histogram som sammenligner flere modaliteter (f.eks.

#     ROSIE, IMC, IF).
#     """
#     fig, ax = plt.subplots(figsize=(10, 6))

#     for label, config in datasets.items():
#         print(f"Prosesserer dataset for: {label}...")
#         print(f"CONFIG: {config}")
#     #     pixels = get_dataset_pixels(
#     #         config["path"], channel_names, target_channel
#     #     )

#     #     # Plotter tetthetsfordelingen for modaliteten
#     #     sns.histplot(
#     #         pixels,
#     #         bins=bins,
#     #         color=config.get("color"),
#     #         ax=ax,
#     #         kde=False,
#     #         stat="density",
#     #         label=label,
#     #         element="step",  # 'step' gjør det lett å se overlappende linjer
#     #         alpha=0.3,
#     #     )

#     # ax.set_title(
#     #     f"Pikselintensitet fordeling – Kanal: {target_channel}",
#     #     fontsize=14,
#     #     fontweight="bold",
#     # )
#     # ax.set_xlabel("Pikselintensitet")
#     # ax.set_ylabel("Tetthet (Normalized)")
#     # ax.legend(title="Modalitet")

#     # if log_scale:
#     #     ax.set_yscale("log")

#     # plt.tight_layout()
#     # plt.savefig(output_path, dpi=300)
#     # plt.close()

#     # print(f"\nSuksess! Lagret kombinert histogram til: {output_path}")


# # --- Eksempel på kjøring ---

# channel_names = [
#     "DAPI",
#     "CD45",
#     "CD68",
#     "CD14",
#     "PD1",
#     "FoxP3",
#     "CD8",
#     "HLA-DR",
#     "PanCK",
#     "CD3e",
#     "CD4",
#     "aSMA",
#     "CD31",
#     "Vimentin",
#     "CD45RO",
#     "Ki67",
#     "CD20",
#     "CD11c",
#     "Podoplanin",
#     "PDL1",
#     "GranzymeB",
#     "CD38",
#     "CD141",
#     "CD21",
#     "CD163",
#     "BCL2",
#     "LAG3",
#     "EpCAM",
#     "CD44",
#     "ICOS",
#     "GATA3",
#     "Gal3",
#     "CD39",
#     "CD34",
#     "TIGIT",
#     "ECad",
#     "CD40",
#     "VISTA",
#     "HLA-A",
#     "MPO",
#     "PCNA",
#     "ATM",
#     "TP63",
#     "IFNg",
#     "Keratin8/18",
#     "IDO1",
#     "CD79a",
#     "HLA-E",
#     "CollagenIV",
#     "CD66",
# ]

# # Definer stiene (kan være enten en enkeltfil ELLER en hel mappe)
# datasets = {
#     # "ROSIE": {"path": "path/to/rosie_directory_or_file", "color": "blue"},
#     "IMC": {"path": "/Users/theodortredal/Desktop/zenodo/3. TIFF", "color": "green"},
#     # "IF": {"path": "images/", "color": "orange"},
# }

# plot_combined_histogram(
#     datasets=datasets,
#     channel_names=channel_names,
#     target_channel="CD45",
#     bins=100,
#     log_scale=True,
#     output_path="CD45_ROSIE_IMC_IF_histogram.png",
# )








# Brukes for å lage et histogram over IMC bildene i zenodo bilde mappen.
# def get_cd45_pixels_from_folder(folder_path, target_string="CD45"):
#     """Søker rekursivt i mappen og alle undermapper (f.eks. ROI001, ROI002)

#     etter TIFF-filer som har 'CD45' i filnavnet, og slår dem sammen.
#     """
#     path = Path(folder_path)
#     all_pixels = []

#     # rglob('*') søker gjennom mappen OG alle undermapper (som ROI001)
#     # matching_files = [
#     #     f
#     #     for f in path.rglob("*")
#     #     if f.is_file()
#     #     and f.suffix.lower() in [".tif", ".tiff"]
#     #     and target_string.lower() in f.name.lower()
#     # ]


#     matching_files = [
#     f
#     for f in path.rglob("*")
#     if f.is_file()
#     and f.suffix.lower() in [".tif", ".tiff"]
#     and "CD45" in f.name
#     and "CD45RO" not in f.name  # Ekskluderer CD45RO
#     ]

#     if not matching_files:
#         raise FileNotFoundError(
#             f"Fant ingen filer med '{target_string}' i navnet under {folder_path}"
#         )

#     print(
#         f"Fant {len(matching_files)} CD45-filer under {folder_path}. Leser data..."
#     )

#     for img_path in sorted(matching_files):
#         img = tifffile.imread(img_path)
#         # Siden dette er 2D-enkeltkanalfiler, flater vi dem ut direkte
#         all_pixels.append(img.flatten())

#     return np.concatenate(all_pixels)


# # --- Bruk ---
# tiff_mappe = "/Users/theodortredal/Desktop/zenodo/3. TIFF"

# # Hent alle CD45-piksler fra hele TIFF-strukturen
# cd45_piksler = get_cd45_pixels_from_folder(tiff_mappe, target_string="CD45")

# # Plott histogrammet
# fig, ax = plt.subplots(figsize=(8, 6))
# sns.histplot(
#     cd45_piksler, bins=100, color="green", ax=ax, kde=False, stat="density"
# )

# ax.set_title(
#     "Pixel intensity for CD45 IMC", fontsize=14, fontweight="bold"
# )
# ax.set_xlabel("Pixel intensity")
# ax.set_ylabel("Density (Normalized)")
# ax.set_yscale("log")

# plt.tight_layout()
# plt.savefig("IMC_CD45_histogram.png", dpi=300)
# plt.close()

# print("Ferdig! Histogrammet er lagret som CD45_histogram_all_rois.png")