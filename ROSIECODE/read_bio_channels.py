import tifffile
# import numpy as np
# import os

# path = os.path.expanduser("~/Downloads/test_bilde_ROSIE.tiff")
# im = tifffile.imread(path)
# print(im.shape)  # expect (50, H, W)

# # Compare a couple of channels to confirm they're not identical
# for c in [0, 1, 2]:
#     print(f"channel {c}: mean={im[c].mean():.2f}, std={im[c].std():.2f}")
# print("channel 0 vs 1 identical?", np.array_equal(im[0], im[1]))

#-----------------#-----------------#-----------------#-----------------

# import tifffile
# import numpy as np

# BIOMARKER_LABELS = [
#     'DAPI','CD45','CD68','CD14','PD1','FoxP3','CD8','HLA-DR','PanCK','CD3e',
#     'CD4','aSMA','CD31','Vimentin','CD45RO','Ki67','CD20','CD11c','Podoplanin','PDL1',
#     'GranzymeB','CD38','CD141','CD21','CD163','BCL2','LAG3','EpCAM','CD44','ICOS',
#     'GATA3','Gal3','CD39','CD34','TIGIT','ECad','CD40','VISTA','HLA-A','MPO',
#     'PCNA','ATM','TP63','IFNg','Keratin8/18','IDO1','CD79a','HLA-E','CollagenIV','CD66'
# ]

# im = tifffile.imread("/Users/theodortredal/Downloads/test_bilde_ROSIE.tiff")  # (50, H, W)

# # Tissue mask: any pixel where at least one channel is nonzero
# tissue_mask = np.any(im != 0, axis=0)
# print(f"Tissue pixels: {tissue_mask.sum()} / {tissue_mask.size} ({100*tissue_mask.mean():.1f}%)")

# results = []
# for c, name in enumerate(BIOMARKER_LABELS):
#     vals = im[c][tissue_mask]
#     results.append((name, vals.mean(), vals.std(), vals.max()))

# results.sort(key=lambda r: r[1], reverse=True)  # sort by mean expression, strongest first
# for name, mean, std, mx in results:
#     print(f"{name:15s} mean={mean:.4f}  std={std:.4f}  max={mx:.4f}")



#-----------------#-----------------#-----------------#-----------------




# import tifffile

# img = tifffile.imread("/Users/theodortredal/Downloads/test_bilde_ROSIE.tiff")
# print("Bilde-shape:", img.shape)  # Bør vise (50, høyde, bredde)
# print("Min-verdi:", img.min(), "Max-verdi:", img.max())


#-----------------#-----------------#-----------------#-----------------

# from PIL import Image
# import tifffile

# jpg = Image.open("images/test_bilde.jpg")
# print("JPEG size:", jpg.size)  # (width, height)

# tif = tifffile.imread("Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif")
# print("TIF shape:", tif.shape)


#-----------------#-----------------#-----------------#-----------------

# import tifffile

# with tifffile.TiffFile("Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif") as tf:
#     page = tf.pages[0]
#     for tag in page.tags:
#         print(tag.name, ":", tag.value)

#-----------------#-----------------#-----------------#-----------------


# from pathlib import Path
# import json
# import re

# rosie_dir = Path("/Users/theodortredal/Desktop/ EGMI/ROSIECODE")

# print("--- Søker etter markørlister i ROSIE-koden ---")

# # 1. Søk etter .json, .csv eller .txt filer som kan inneholde kanaler
# for file_path in rosie_dir.rglob("*"):
#     if file_path.suffix in [".json", ".csv", ".txt", ".yaml"]:
#         try:
#             content = file_path.read_text(errors="ignore")
#             # Sjekk om filen inneholder kjente markørnavn som DAPI, CD3, Pan-CK e.l.
#             if any(
#                 m in content.upper()
#                 for m in ["DAPI", "CD3", "CD20", "PAN-CK", "PANCK", "CD68"]
#             ):
#                 print(f"\n[FUNNET I FIL]: {file_path}")
#                 if file_path.suffix == ".json":
#                     data = json.loads(content)
#                     print(json.dumps(data, indent=2)[:500])
#                 else:
#                     print(content[:500])
#         except Exception:
#             pass

# # 2. Søk i Python-skript (.py) etter lister med 50 elementer
# for py_file in rosie_dir.rglob("*.py"):
#     try:
#         content = py_file.read_text(errors="ignore")
#         # Søk etter variabeldefinisjoner som f.eks. MARKERS =, CHANNELS =, PANEL =
#         matches = re.findall(
#             r"(MARKERS|CHANNELS|PANEL|TARGETS)\s*=\s*\[(.*?)\]",
#             content,
#             re.DOTALL | re.IGNORECASE,
#         )
#         for var_name, list_str in matches:
#             items = [item.strip("'\" ") for item in list_str.split(",")]
#             if len(items) >= 10:  # Dersom listen inneholder mange markører
#                 print(f"\n[FUNNET VARIABEL '{var_name}' I {py_file.name}]:")
#                 for idx, item in enumerate(items[:50]):
#                     print(f"Kanal {idx}: {item}")
#     except Exception:
#         pass



# import torch

# # Erstatt med din faktiske sti til .pth-filen
# model_path = "ROSIECODE/best_model_single.pth"

# checkpoint = torch.load(model_path, map_location="cpu")

# print("--- Nøkler funnet i modellfilen ---")
# print(checkpoint.keys())

# # Sjekk om noen nøkler inneholder ord som 'marker', 'channel', 'name' eller 'label'
# for key in checkpoint.keys():
#     if any(
#         k in key.lower() for k in ["marker", "channel", "name", "label", "target"]
#     ):
#         print(f"\nFunnet relevante data under nøkkelen '{key}':")
#         print(checkpoint[key])
