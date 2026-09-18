import tifffile


def extract_channel_1(input_path, output_path):
    print(f"Åpner stor TIFF-fil (memmapped): {input_path}...")

    # Åpner filen uten å laste hele 17 GB inn i RAM
    with tifffile.TiffFile(input_path) as tif:
        # Henter minneavbildning (memmap) av bildematrisen
        image_data = tif.asarray(out="memmap")

        print(f"Bildeform (shape): {image_data.shape}")
        print(f"Datatype: {image_data.dtype}")

        # Håndterer shape om det er (C, H, W) eller (H, W, C)
        if image_data.ndim == 3:
            # Sjekker om kanalene ligger først (f.eks. (50, H, W))
            if image_data.shape[0] < image_data.shape[2]:
                channel_1 = image_data[1]  # Henter kanal 1 (andre kanal)
            else:
                # Hvis kanalene ligger til slutt (f.eks. (H, W, 50))
                channel_1 = image_data[:, :, 1]  # Henter kanal 1 (andre kanal)
        else:
            raise ValueError(f"Uventet antall dimensjoner: {image_data.ndim}")

        print("Lagrer kanal 1 til ny fil...")
        tifffile.imwrite(output_path, channel_1, compression="zlib")

    print(f"Suksess! Kanal 1 lagret til: {output_path}")


if __name__ == "__main__":
    input_file = "output_results/Registered_HE_HE_PS15.19650-B3_Slide2_20210517_ROSIE_1.tiff"
    output_file = (
        "output_results/Registered_HE_HE_PS15.19650-B3_Slide2_20210517_ROSIE_1_channel1.tiff"
    )

    extract_channel_1(input_file, output_file)