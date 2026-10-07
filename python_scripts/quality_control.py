import numpy as np
import cv2
from scipy.stats import wasserstein_distance

def get_image_histogram(image_path):
    # Les inn H&E-bildet
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Beregn histogram med 256 bins for bildet (f.eks. på gråtone eller per fargekanal)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    hist, _ = np.histogram(gray, bins=256, range=(0, 256), density=True)
    return hist

def calculate_w1_distance(test_image_path, training_histograms):
    """
    test_image_path: Stien til ditt H&E-bilde
    training_histograms: En liste/array med forhåndsberegnede histogrammer fra treningssettet
    """
    test_hist = get_image_histogram(test_image_path)
    
    distances = []
    for train_hist in training_histograms:
        # Beregn Wasserstein-distanse mellom histogrammene
        dist = wasserstein_distance(test_hist, train_hist)
        distances.append(dist)
        
    # Snittet av W1-distansene mot alle treningsbildene (som beskrevet i artikkelen)
    average_w1 = np.mean(distances)
    return average_w1



if __name__ == "__main__":

    calculate_w1_distance("images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif", )
