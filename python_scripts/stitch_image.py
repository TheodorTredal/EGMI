import argparse
import os
import sys
import numpy as np
import tifffile
from PIL import Image

'''
Må prøve

1. Farge hver hjørnedel av bildet RBG også sy det sammen
2. Finne ut hvorfor hver bilde del ble så gigantisk
3. Lagrer jeg bildet riktig?
4. Hvorfor blir bildet så svart? Har det noe med oppløsningen å gjøre?
5. Hva er egentlig riktig oppløsning for ROSIE?
6. sammenlign pixel verdier / oppløsning på Registered HE.czi.tif bildet med DAPI bildet, er det forskjellig oppløsning her?



'''


def split_images():
    input_file = "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
    output_dir = "OG_split_images"
    os.makedirs(output_dir, exist_ok=True)

    print("Leser inn det store bildet...")
    img = tifffile.imread(input_file)
    h, w = img.shape[:2]

    # 256px overlapp sikrer at PATCH_SIZE (128) og stride går rent opp i skjøtene
    overlap = 256

    half_h = h // 2
    half_w = w // 2

    # Definerer de 4 kvadrantene med overlapp
    crops = {
        "top_left": img[0 : half_h + overlap, 0 : half_w + overlap],
        "top_right": img[0 : half_h + overlap, half_w - overlap : w],
        "bottom_left": img[half_h - overlap : h, 0 : half_w + overlap],
        "bottom_right": img[half_h - overlap : h, half_w - overlap : w],
    }

    for name, crop in crops.items():
        out_path = os.path.join(output_dir, f"part_{name}.tif")
        print(f"Lagrer {name} ({crop.shape}) til {out_path}...")
        tifffile.imwrite(out_path, crop, photometric='rgb', bigtiff=True)

    print("Ferdig med å dele opp bildet i 4 deler!")



def split_image_into_8(num_rows=2, num_cols=4, overlap=256):
    input_file = "images/input_images/HE_for_ROSIE_40x.tif"
    output_dir = "OG_split_image_into_8_40x"
    os.makedirs(output_dir, exist_ok=True)

    print("Leser inn det store bildet...")
    img = tifffile.imread(input_file)
    h, w = img.shape[:2]

    # Beregn basis-størrelse per del uten overlapp
    h_step = h // num_rows
    w_step = w // num_cols

    print(f"Opprinnelig størrelse: {w}x{h} px")
    print(f"Deler inn i {num_rows}x{num_cols} ({num_rows * num_cols} deler) med {overlap}px overlapp...")

    for r in range(num_rows):
        for c in range(num_cols):
            # Y-koordinater (høyde) med overlapp
            y1 = 0 if r == 0 else (r * h_step) - overlap
            y2 = h if r == num_rows - 1 else ((r + 1) * h_step) + overlap

            # X-koordinater (bredde) med overlapp
            x1 = 0 if c == 0 else (c * w_step) - overlap
            x2 = w if c == num_cols - 1 else ((c + 1) * w_step) + overlap

            crop = img[y1:y2, x1:x2]

            # Lagrer med navneformat: part_r1_c1.tif, part_r1_c2.tif osv.
            name = f"r{r+1}_c{c+1}"
            out_path = os.path.join(output_dir, f"part_{name}_40x.tif")
            
            print(f"Lagrer rad {r+1}, kolonne {c+1} ({crop.shape}) til {out_path}...")
            tifffile.imwrite(out_path, crop, photometric='rgb', bigtiff=True)

    print(f"Ferdig! Lagret {num_rows * num_cols} deler.")



def get_available_image_filename(
    output_dir: str, base_name: str, extension: str = ".tiff"
) -> str:
    candidate = os.path.join(output_dir, f"{base_name}_ROSIE{extension}")
    if not os.path.exists(candidate):
        return candidate

    i = 1
    while os.path.exists(
        os.path.join(output_dir, f"{base_name}_ROSIE_{i}{extension}")
    ):
        i += 1
    return os.path.join(output_dir, f"{base_name}_ROSIE_{i}{extension}")


def get_available_log_filename(output_dir, base_name="baserun", extension=".log"):
    if not os.path.exists(f"{output_dir}/{base_name}{extension}"):
        return f"{output_dir}/{base_name}{extension}"
    i = 1
    while os.path.exists(f"{output_dir}/{base_name}_{i}{extension}"):
        i += 1
    return f"{output_dir}/{base_name}_{i}{extension}"


def load_channel(file_path, channel_idx):
    """Leser ut KUN valgt kanal ved hjelp av memory mapping."""
    print(f"Leser kanal {channel_idx} fra: {os.path.basename(file_path)}")
    store = tifffile.imread(file_path, aszarr=False, out="memmap")

    if store.ndim == 3 and store.shape[0] < store.shape[1]:
        channel_data = np.array(store[channel_idx], copy=True)
    elif store.ndim == 3:
        channel_data = np.array(store[..., channel_idx], copy=True)
    else:
        channel_data = np.array(store, copy=True)

    return channel_data


def normalize_to_8bit(image):
    """Spreder bildets intensiteter ut over heile 0-255 skalaen for optimal visualisering."""
    img_min = image.min()
    img_max = image.max()
    print(f"Normaliserer bilde: Opprinnelig Min={img_min}, Maks={img_max}")

    if img_max == img_min:
        return np.zeros(image.shape, dtype=np.uint8)

    # Min-Max skalering til 0-255
    normalized = (image - img_min) / (img_max - img_min) * 255.0
    return normalized.astype(np.uint8)


def combine_images(
    input_dir,
    output_dir,
    channel_idx,
    overlap=256,
    output_format="tiff",
    normalize=True,
):
    os.makedirs(output_dir, exist_ok=True)

    ext = f".{output_format.lower()}"
    base_name = f"combined_image_ch{channel_idx}"
    out_file = get_available_image_filename(output_dir, base_name, extension=ext)

    tl = load_channel(
        os.path.join(input_dir, "OG_part_top_left_ROSIE.tiff"), channel_idx
    )
    tr = load_channel(
        os.path.join(input_dir, "OG_part_top_right_ROSIE.tiff"), channel_idx
    )
    bl = load_channel(
        os.path.join(input_dir, "OG_part_bottom_left_ROSIE.tiff"), channel_idx
    )
    br = load_channel(
        os.path.join(input_dir, "OG_part_bottom_right_ROSIE.tiff"), channel_idx
    )

    # Skjær bort overlappende områder
    tl_crop = tl[: tl.shape[0] - overlap, : tl.shape[1] - overlap]
    tr_crop = tr[: tr.shape[0] - overlap, overlap:]
    bl_crop = bl[overlap:, : bl.shape[1] - overlap]
    br_crop = br[overlap:, overlap:]

    del tl, tr, bl, br

    print("Syr sammen bildene...")
    top_row = np.hstack((tl_crop, tr_crop))
    del tl_crop, tr_crop

    bottom_row = np.hstack((bl_crop, br_crop))
    del bl_crop, br_crop

    full_image = np.vstack((top_row, bottom_row))
    del top_row, bottom_row

    print(
        f"Råbilde statistikk - Type: {full_image.dtype}, Min: {full_image.min()}, Maks: {full_image.max()}, Snitt: {full_image.mean():.2f}"
    )

    # Kontrastjustering / Normalisering dersom bildet ser altfor mørkt ut
    if normalize:
        full_image = normalize_to_8bit(full_image)

    print(f"Lagrer sammensydd bilde ({output_format.upper()}) til: {out_file}")

    if output_format.lower() in ["png", "jpg", "jpeg"]:
        # PIL støtter lagring av store PNG/JPEG-filer
        Image.MAX_IMAGE_PIXELS = None  # Fjern pikselgrense for PIL
        pil_img = Image.fromarray(full_image)
        pil_img.save(out_file)
    else:
        # Standard TIFF-lagring
        tifffile.imwrite(out_file, full_image, bigtiff=True)

    print(f"Vellykket lagret til: {out_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Syr sammen oppdelte TIFF-bilder for en bestemt kanal."
    )

    parser.add_argument(
        "--channel",
        "-c",
        type=int,
        default=0,
        help="Kanalindeks som skal prosesseres (f.eks. 0)",
    )
    parser.add_argument(
        "--input_dir",
        "--input-dir",
        "-i",
        type=str,
        default="split_images_results",
        help="Mappe hvor delbildene ligger",
    )
    parser.add_argument(
        "--output_dir",
        "--output-dir",
        "-o",
        type=str,
        default="output_results",
        help="Mappe hvor det ferdige bildet og loggen skal lagres",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=256,
        help="Antall piksler med overlapp (default: 256)",
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        default="tiff",
        choices=["tiff", "png", "jpg"],
        help="Filformat for det sammensydde bildet (default: tiff)",
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Strekk kontrasten (0-255) slik at bildet ikke blir mørkt i bildevisere",
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    log_filename = get_available_log_filename(args.output_dir)
    logfile = open(log_filename, "w", buffering=1)
    sys.stdout = logfile
    sys.stderr = logfile
    print("Logging to file: ", log_filename)

    combine_images(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        channel_idx=args.channel,
        overlap=args.overlap,
        output_format=args.format,
        normalize=args.normalize,
    )

    print("Filen er opprettet og skrevet til disken!")



def stitch_tiff_tiles(
    folder_path: str,
    output_filename: str = "stitched_output.tiff",
    num_rows: int = 2,
    num_cols: int = 4,
    channel_index: int = 0,
    prefix: str = "part_r",
    suffix: str = "_40x_ROSIE.tiff",
) -> np.ndarray:
    """Syr sammen TIFF-bildebrikker i et rutenett og henter ut én spesifikk kanal."""

    # Legg til kanalnummeret i ut-filnavnet dersom det slutter på '_' (f.eks. 'step_4_channel_.tiff')
    if output_filename.endswith("_.tiff"):
        name, ext = os.path.splitext(output_filename)
        output_filename = f"{name}{channel_index}{ext}"  # Blir 'step_4_channel_0.tiff'

    rows_images = []

    for r in range(1, num_rows + 1):
        row_tiles = []
        for c in range(1, num_cols + 1):
            # Bruk det opprinnelige suffix-et for å finne kildefilene
            filename = f"{prefix}{r}_c{c}{suffix}"
            filepath = os.path.join(folder_path, filename)

            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Fant ikke filen: {filepath}")

            img = tifffile.imread(filepath)

            # Hent ut spesifisert kanal
            if img.ndim == 3:
                if img.shape[0] < img.shape[2]:
                    ch = img[channel_index, :, :]
                else:
                    ch = img[:, :, channel_index]
            else:
                ch = img

            row_tiles.append(ch)

        rows_images.append(np.hstack(row_tiles))

    full_stitched_image = np.vstack(rows_images)

    output_path = os.path.join(folder_path, output_filename)
    tifffile.imwrite(output_path, full_stitched_image)

    print(f"Sammensying fullført! Lagret til: {output_path}")
    print(f"Endelig bildestørrelse: {full_stitched_image.shape}")

    return full_stitched_image


if __name__ == "__main__":
    stitch_tiff_tiles(
        folder_path="images/result_images/OG_split_image_into_8_40x",
        output_filename="step_4_channel_.tiff",
        channel_index=0
    )