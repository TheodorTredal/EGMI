from PIL import Image
import czifile
import xml.etree.ElementTree as ET



'''
This files crop a .tiff image to a smaller size so we can run faster inference.
'''


# # # 1. Last inn bildet
def crop_image_first_method():

    img_path = "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
    img = Image.open(img_path)

    # 2. Definer øverste venstre hjørne (x, y) for utsnittet du vil ha
    x_start = 3000  # Endre disse koordinatene ut fra hvor det er interessant
    y_start = 3500

    # 3. Definer boks: (left, upper, right, lower)
    crop_box = (x_start, y_start, x_start + 2000, y_start + 2000)

    # 4. Beskjær og lagre
    cropped_img = img.crop(crop_box)
    cropped_img.save("he_crop_3000x3000.tif")
    print("Bilde beskjært til 3000x3000 px!")


def crop_and_resize_image_using_bicubic():
    img = Image.open(
        "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
    )

    x_start = 3000
    y_start = 3500

    # Beskjær 1500x1500 fra 20x-bildet
    crop_20x = img.crop((x_start, y_start, x_start + 2000, y_start + 2000))

    # For H&E-vevsbilde: Bruk BICUBIC
    crop_40x = crop_20x.resize((3000, 3000), resample=Image.Resampling.NEAREST)

    crop_40x.save("he_crop_3000x3000_NEAREST.tif")
    crop_20x.save("he_crop_3000x3000_bicubic.tif")



def some_meta_data_function():
    import tifffile

    filename = (
        "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
    )

    with tifffile.TiffFile(filename) as tif:
        # Hent TIFF-tags for oppløsning
        page = tif.pages[0]

        # XResolution og YResolution er gitt i antall piksler per enhet (ofte cm eller cm-fraksjoner)
        x_res = page.tags.get("XResolution")
        unit = page.tags.get("ResolutionUnit")

        print(f"XResolution Tag: {x_res}")
        print(f"Resolution Unit: {unit}")

        # For mange mikroskopifiler ligger detaljert metadata i image_description:
        description = page.description
        print("\n--- Image Description Metadata ---")
        print(description[:1000] if description else "Ingen ekstra metadata funnet.")


# Installer czifile dersom du ikke har det: pip install czifile




def downsample_image():
    '''Reduces the Zenodo image to a lesser pixel density closer to what is expected by ROSIE'''

    img_path = (
        "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
    )
    img = Image.open(img_path)

    # 1. Velg startkoordinat
    x_start = 3000
    y_start = 3500

    # 2. Hent ut et utsnitt på 5148x5148 piksler på din 0.22 µm/px-skala
    crop_orig = img.crop((x_start, y_start, x_start + 2000, y_start + 2000))

    # 3. Skaler ned til 3000x3000 piksler for å treffe ROSIE sin skala (0.3775 µm/px)
    crop_rosie_scale = crop_orig.resize(
        (1748, 1748), resample=Image.Resampling.BICUBIC
    )

    # 4. Lagre
    crop_rosie_scale.save("he_crop_3000x3000_downsampled_03775_um_px_scale.tif")
    print("Bilde skalert og lagret med perfekt mpp for ROSIE!")



def crop_image():
    # 1. Last inn bildet
    img_path = (
        "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
    )
    img = Image.open(img_path)

    # 2. Definer øverste venstre hjørne (x, y) for utsnittet
    x_start = 3000
    y_start = 3500

    # 3. Beskjær 3000x3000 piksler direkte (uten skalering)
    crop_box = (x_start, y_start, x_start + 2000, y_start + 2000)
    cropped_img = img.crop(crop_box)

    # 4. Lagre bildet
    output_path = "he_crop_3000x3000_native_02200um_px.tif"
    cropped_img.save(output_path)

    print(
        f"Ferdig! Lagret {output_path} med dimensjoner {cropped_img.size[0]}x{cropped_img.size[1]} px."
    )



def get_czi_metadata():
    czi_path = (
        "images/input_images/HE_PS15.19650-B3_Slide2_20210517.czi"  # Tilpass stien
    )

    with czifile.CziFile(czi_path) as czi:
        xml_metadata = czi.metadata()

    # Søk etter forstørrelse eller pikselstørrelse i XML-metadataene
    root = ET.fromstring(xml_metadata)

    for elem in root.iter():
        if "Scaling" in elem.tag or "Magnification" in elem.tag:
            print(f"{elem.tag.split('}')[-1]}: {elem.text}")



def get_pixel_scale():
    czi_path = "images/input_images/HE_PS15.19650-B3_Slide2_20210517.czi"

    with czifile.CziFile(czi_path) as czi:
        root = ET.fromstring(czi.metadata())

    for elem in root.iter():
        # Søk etter Distance-noder (som ofte representerer X, Y og Z akser)
        if elem.tag.endswith("Distance"):
            dist_id = elem.attrib.get("Id", "Ukjent")
            value_node = elem.find("./Value") or elem.find(
                ".//{*}Value"
            )  # Håndterer eventuelle XML-namespaces

            if value_node is not None and value_node.text:
                m_per_px = float(value_node.text)
                um_per_px = m_per_px * 1e6  # Konverter fra meter til mikrometer (µm)
                print(f"Akse {dist_id}: {m_per_px:.2e} m/px ({um_per_px:.4f} µm/px)")



def match():
    czi_path = "images/input_images/HE_PS15.19650-B3_Slide2_20210517.czi"
    tif_path = (
        "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif"
    )

    # 1. Les dimensjoner fra CZI via asarray().shape
    with czifile.CziFile(czi_path) as czi:
        # czifile returnerer f.eks. shape som (1, 1, 3, Y, X, 1) eller (Y, X, C)
        czi_array = czi.asarray()
        czi_shape = czi_array.shape

    # 2. Les dimensjoner fra TIFF
    with Image.open(tif_path) as tif:
        tif_width, tif_height = tif.size

    print(f"CZI Form (Shape): {czi_shape}")
    print(f"TIFF Dimensjoner (Bredde x Høyde): {tif_width} x {tif_height} px")


def get_cropped_from_czi_original_image():
    # Fjern pikselbegrensning for store TIFF/CZI-filer
    Image.MAX_IMAGE_PIXELS = None

    czi_path = "images/input_images/HE_PS15.19650-B3_Slide2_20210517.czi"
    # output_path = "images/input_images/he_crop_3000x3000_from_czi_direct.tif"
    output_path = "he_crop_3000x3000_from_czi_direct.tif"

    # 1. Les CZI-data direkte som et NumPy-array
    print("Leser inn CZI-originalfilen...")
    with czifile.CziFile(czi_path) as czi:
        # czifile returnerer vanligvis en matrise med form (1, 1, C, Y, X, 1) eller (Y, X, C)
        img_data = czi.asarray()

    # Fjerner ekstra dimensjoner (slik at vi står igjen med Y, X, C)
    img_data = img_data.squeeze()

    # Dersom fargekanalene ligger først (C, Y, X), flytter vi dem til sist (Y, X, C)
    if img_data.shape[0] == 3 or img_data.shape[0] == 4:
        img_data = img_data.transpose(1, 2, 0)

    # Konverter til PIL Image
    full_img = Image.fromarray(img_data)

    # 2. Sett startkoordinater på CZI-skalaen
    x_start = 15000
    y_start = 16000

    # 3. Klipp ut 5148x5148 piksler fra CZI-originalen (0.2200 µm/px)
    crop_5148 = full_img.crop((x_start, y_start, x_start + 5148, y_start + 5148))

    # 4. Skaler én gang ned til 3000x3000px for å treffe 0.3775 µm/px for ROSIE
    crop_3000 = crop_5148.resize((3000, 3000), resample=Image.Resampling.BICUBIC)

    # 5. Lagre som ren TIFF for ROSIE
    crop_3000.save(output_path)
    print(f"Suksess! RENT bilde lagret til: {output_path}")


if __name__ == "__main__":
    # get_pixel_scale()
    # crop_image()
    # downsample_image()
    # match()
    get_cropped_from_czi_original_image()