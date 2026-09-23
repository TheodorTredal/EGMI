TESTS:


## T1
Input image: 
    images/input_images/Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif
    - **Input specification**:
    - Dimensions: 6646 x 13819 px
    - Resolution / magnification:
    - Color space: RGB
    - size: 172 mb


output image:

**Execution settings:**
    --exclude_background \
    --stride_size 8

Before testing note:
    - Testing the original image from Zenodo to check what output ROSIE gives.

Results:
    - The image does not look at all like the ground truth. I compared DAPI (channel 0) to the ground truth DAPI and the ROSIE output is highlighted in areas where the concentration of DAPI is low.


## T2
Input image:
    images/input_images/HE_for_ROSIE_20x.tif
    - **Input specification**:
    - Dimensions: 13292 x 27638 px
    - Resolution / magnification:
    - Color space: RGB
    - size: 377.9 mb

Output image: 

Settings:
    --exclude_background \
    --stride_size 8


Before testing note:
    - Check if an inhanced version of input image from T1 will help improve ROSIE output

Results:
    - The image does not look the same as the ground truth, it looks a lot darker than what was expected.



## T3
Input folder:
    images/OG_split_images
    - **Input specification**:
    - Dimensions: 6646 x 13819 px
    - Resolution / magnification:
    - Color space: RGB
    - size: 76.9 mb

Output image: 

Settings:
    --input_dir  images/OG_split_images/... 4 different parts of the same image \
    --output_name OG_part_bottom_left \
    --output_dir images/result_images \
    --model_path ROSIECODE/best_model_single.pth \
    --log_output log \
    --exclude_background \
    --stride_size 4


Before testing note:
    - Check if increasing the step from 8 to 4 will increase the resolution of the output image of ROSIE. I have split the original HE.ciz.tif image into 4 parts to make it possible to process on the springfield cluster, i will later recombine the image and compare it to the ground truth image from Zenodo.

Results:
    - 