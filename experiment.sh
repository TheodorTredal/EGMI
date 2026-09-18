#!/bin/sh

# This file runs the actual ROSIE script
    # --input_dir "/Users/theodortredal/Desktop/IF_images/2. IF/2021_06_11_PS15.19650-B3_Slide1_EcadAF647_CD45AF488IFDAPI.tif" \

mkdir -p output_results

# INPUT
python3 ROSIECODE/evaluate.py \
    --input_dir  Registered_HE_HE_PS15.19650-B3_Slide2_20210517.czi.tif \
    --output_dir output_results \
    --model_path ROSIECODE/best_model_single.pth \
    --exclude_background \
    --stride_size 8


