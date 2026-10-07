TESTS:


#-------------------------------------------------------------------------------

## Template

## T
Input folder:
    images/OG_split_images
    - **Input specification**:
    - Dimensions: 
    - Resolution / magnification: 40X
    - Color space: RGB
    - size:

Output image: 

Settings:

INPUT_DIR=""
OUTPUT_DIR=""
MODEL_PATH="ROSIECODE/best_model_single.pth"
LOG_DIR="log"

        --input_dir "$img" \
        --output_name "$name_no_ext" \
        --output_dir "$OUTPUT_DIR" \
        --model_path "$MODEL_PATH" \
        --log_output "$LOG_DIR" \
        --exclude_background \
        --stride_size x \
        --postprocess_image \
        --smooth_sigma x


Before testing note:


Results:

#-------------------------------------------------------------------------------


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
    images/input_images/HE_for_ROSIE_40x.tif
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
    - Increasing the step from 8 to 4 did not make the model predict DAPI in the correct places, it did however increase the resolution a bit. From the paper it seems like ROSIE expects a 40x magnified H&E image, meanwhile it seems like the image i have been given is only a 20x magnification. Which have led me to the next test, T4. Also i learned to name the result images after the configuration in the execute file, nice..

## T4
Input folder:
    images/OG_split_images
    - **Input specification**:
    - Dimensions: 
    - Resolution / magnification: 40X
    - Color space: RGB
    - size:

Output image: 

Settings:

INPUT_DIR="images/input_images/OG_split_image_into_8_40x"
OUTPUT_DIR="images/result_images/OG_split_image_into_8_40x"
MODEL_PATH="ROSIECODE/best_model_single.pth"
LOG_DIR="log"

        --input_dir "$img" \
        --output_name "$name_no_ext" \
        --output_dir "$OUTPUT_DIR" \
        --model_path "$MODEL_PATH" \
        --log_output "$LOG_DIR" \
        --exclude_background \
        --stride_size 4 \
        --postprocess_image \
        --smooth_sigma 0.5


Before testing note:
    - Increased the resolution from 20x to 40x and increased the step size from 8 to 4. In T2 the image were 40x but with a step size of 8, the resulting image were dark. I hope this test will decrease the darkness seen from T2 and hopefully the resulting DAPI will be more like the ground truth.

Results:



## T5
Input folder:
    images/OG_split_images
    - **Input specification**:
    - Dimensions: 
    - Resolution / magnification: 20X
    - Color space: RGB
    - size:

Output image: 

Settings:

INPUT_DIR=""
OUTPUT_DIR=""
MODEL_PATH="ROSIECODE/best_model_single.pth"
LOG_DIR="log"
img="he_crop_3000x3000_from_czi_direct.tiff"

        --input_dir "$img" \
        --output_name "he_crop_3000x3000_from_czi_direct" \
        --output_dir "$OUTPUT_DIR" \
        --model_path "$MODEL_PATH" \
        --log_output "$LOG_DIR" \
        --stride_size 1 \
        --smooth_sigma 0.5


Before testing note:
So i finally managed to find the meta data for the Zenodo image, the image is taken at 20X zoom and not 40X, this however does not matter for ROSIE model, what matters however is the pixel per µm. ROSIE expects an resolution of about ≈ 0.3775 µm/px, meanwhile the Zenodo .czi image has a resolution of about ≈ 0.2200 µm/px. 

Another thing is that i have used the wrong image, i have been fooled! i have been using the "Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif" image which is a downsampled (does not have the correct resolution) version of the original image which is called "HE_PS15.19650-B3_Slide2_20210517.czi". The image i have been using did not have any meta data connected to it (red flag), while the .czi file has meta data. Not only have i been using the wrong image i have also upscaled this wrong image and been expecting results. The .czi.tiff (which i unfortunately have been using uptil now) is only 6646 x 13819 px while the .czi file (the correct original image) has a resolution of about 26103 x 60601 px.

the .czi image has a better resolution than what ROSIE needs (which is great!) i have downsampled the image to the exact resolution which is expected by ROSIE (from 0.2200µm/px to 0.3775µm/px). Since processing the entire image takes too long of a time (up to 80 hours with a step size of 4!) i am now trying to "re-create" the results from ROSIE by using a 3000x3000 px cropped version of the original image. 


Results:





## T6
Input folder:
    images/OG_split_images
    - **Input specification**:
    - Dimensions: 
    - Resolution / magnification: 20X
    - Color space: RGB
    - size:

Output image: 

Settings:

INPUT_DIR=""
OUTPUT_DIR=""
MODEL_PATH="ROSIECODE/best_model_single.pth"
LOG_DIR="log"
img="he_crop_3000x3000_from_czi_direct.tiff"

        --input_dir "$img" \
        --output_name "he_crop_3000x3000_from_czi_direct_ex_background_smooth_sigma" \
        --output_dir "$OUTPUT_DIR" \
        --model_path "$MODEL_PATH" \
        --log_output "$LOG_DIR" \
        --exclude_background \
        --stride_size 1 \
        --postprocess_image \
        --smooth_sigma 0.5


Before testing note:
This is the same as T5 but now i am adding smooth_sigma, post_process_image and exclude_background, i am doing this test to compare it against T5


Results: