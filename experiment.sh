#!/bin/sh


# INPUT
python3 ROSIECODE/evaluate.py \
    --input_dir  images/OG_split_images/part_bottom_left.tif \
    --output_name OG_part_bottom_left \
    --output_dir images/result_images \
    --model_path ROSIECODE/best_model_single.pth \
    --log_output log \
    --exclude_background \
    --stride_size 4


python3 ROSIECODE/evaluate.py \
    --input_dir  images/OG_split_images/part_bottom_right.tif \
    --output_name OG_part_bottom_right \
    --output_dir images/result_images \
    --model_path ROSIECODE/best_model_single.pth \
    --log_output log \
    --exclude_background \
    --stride_size 4


python3 ROSIECODE/evaluate.py \
    --input_dir  images/OG_split_images/part_top_left.tif \
    --output_name OG_part_top_left \
    --output_dir images/result_images \
    --model_path ROSIECODE/best_model_single.pth \
    --log_output log \
    --exclude_background \
    --stride_size 4


python3 ROSIECODE/evaluate.py \
    --input_dir  images/split_images/part_top_right.tif \
    --output_name OG_part_top_right \
    --output_dir images/result_images \
    --model_path ROSIECODE/best_model_single.pth \
    --log_output log \
    --exclude_background \
    --stride_size 4