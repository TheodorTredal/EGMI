#!/bin/bash

# Kjør python-skriptet med argumentene dine
python python_scripts/stitch_image.py \
  --channel 0 \
  --input-dir "images/result_images" \
  --output-dir "images/result_images" \
  --overlap 256 \
  --normalize \
  --format png