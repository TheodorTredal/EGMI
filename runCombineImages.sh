#!/bin/bash

# Kjør python-skriptet med argumentene dine
python stitch_image.py \
  --channel 35 \
  --input-dir "split_images_results" \
  --output-dir "split_images_results" \
  --overlap 256 \
  --normalize \
  --format png