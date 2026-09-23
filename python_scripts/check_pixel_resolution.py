import czifile
import xml.etree.ElementTree as ET

# Banen til den opprinnelige .czi-filen (ikke .tif)
czi_path = "images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi"

with czifile.CziFile(czi_path) as czi:
    xml_metadata = czi.metadata()
    root = ET.fromstring(xml_metadata)

    # Søk etter skaleringsverdier (ScaleX / ScaleY)
    for elem in root.iter():
        if 'Distance' in elem.tag and elem.attrib.get('Id') == 'X':
            for child in elem:
                if 'Value' in child.tag:
                    mpp = float(child.text) * 1e6 # Omgjør fra meter til µm
                    print(f"Ekte pikselstørrelse (Scale X): {mpp:.4f} µm/px")