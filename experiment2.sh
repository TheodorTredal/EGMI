#!/bin/bash

OUTPUT_DIR="images/result_images/OG_split_image_into_8_40x"
MODEL_PATH="ROSIECODE/best_model_single.pth"
LOG_DIR="log"

# Stopp skriptet hvis en feil oppstår
set -e

# --- Bilde 0: Hentet direkte fra CZI (0.3775 µm/px) ---
IMG0="$OUTPUT_DIR/he_crop_3000x3000_from_czi_direct.tiff"

if [ ! -f "$IMG0" ]; then
    echo "Feil: Finner ikke filen $IMG0"
    exit 1
fi

echo "=== Prosesserer bilde 1/3: Direkte fra CZI (0.3775 µm/px) ==="
python3 ROSIECODE/evaluate.py \
    --input_dir "$IMG0" \
    --output_name "he_crop_3000x3000_from_czi_direct" \
    --output_dir "$OUTPUT_DIR" \
    --model_path "$MODEL_PATH" \
    --log_output "$LOG_DIR" \
    --stride_size 1 \
    --smooth_sigma 0.0




# --- Bilde 0: Hentet direkte fra CZI (0.3775 µm/px) ---
IMG0="$OUTPUT_DIR/he_crop_3000x3000_from_czi_direct.tiff"

if [ ! -f "$IMG0" ]; then
    echo "Feil: Finner ikke filen $IMG0"
    exit 1
fi

echo "=== Prosesserer bilde 1/3: Direkte fra CZI (0.3775 µm/px) ==="
python3 ROSIECODE/evaluate.py \
    --input_dir "$IMG0" \
    --output_name "he_crop_3000x3000_from_czi_direct_ex_background_smooth_sigma" \
    --output_dir "$OUTPUT_DIR" \
    --model_path "$MODEL_PATH" \
    --log_output "$LOG_DIR" \
    --exclude_background \
    --postprocess_image \
    --stride_size 1 \
    --smooth_sigma 0.5






# --- Bilde 1: Downsampled fra TIFF (0.3775 µm/px) ---
IMG1="$OUTPUT_DIR/he_crop_3000x3000_downsampled_03775_um_px_scale.tif"

if [ ! -f "$IMG1" ]; then
    echo "Feil: Finner ikke filen $IMG1"
    exit 1
fi

echo "=== Prosesserer bilde 2/3: Nedskalert fra TIFF (0.3775 µm/px) ==="
python3 ROSIECODE/evaluate.py \
    --input_dir "$IMG1" \
    --output_name "he_crop_3000x3000_downsampled_03775_um_px_scale" \
    --output_dir "$OUTPUT_DIR" \
    --model_path "$MODEL_PATH" \
    --log_output "$LOG_DIR" \
    --stride_size 1 \
    --smooth_sigma 0.0


# --- Bilde 2: Native oppløsning (0.2200 µm/px) ---
IMG2="$OUTPUT_DIR/he_crop_3000x3000_native_02200um_px.tif"

if [ ! -f "$IMG2" ]; then
    echo "Feil: Finner ikke filen $IMG2"
    exit 1
fi

echo "=== Prosesserer bilde 3/3: Native oppløsning (0.2200 µm/px) ==="
python3 ROSIECODE/evaluate.py \
    --input_dir "$IMG2" \
    --output_name "he_crop_3000x3000_native_02200um_px" \
    --output_dir "$OUTPUT_DIR" \
    --model_path "$MODEL_PATH" \
    --log_output "$LOG_DIR" \
    --stride_size 1 \
    --smooth_sigma 0.0

echo "Alle tre bildene er ferdig prosessert!"