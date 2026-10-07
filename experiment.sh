#!/bin/bash

# Konfigurer felles stier og parametere
INPUT_DIR="images/input_images/OG_split_image_into_8_40x"
OUTPUT_DIR="images/result_images/OG_split_image_into_8_40x"
MODEL_PATH="ROSIECODE/best_model_single.pth"
LOG_DIR="log"

# Stopp skriptet hvis en feil oppstår
set -e

# Løkk gjennom alle .tif-filer i mappen
for img in "$INPUT_DIR"/*.tif; do
    # Sjekk om filen faktisk eksisterer (i tilfelle ingen .tif-filer finnes)
    [ -e "$img" ] || continue

    # Hent ut filnavn uten sti og ending (f.eks. "part_r1_c1")
    filename=$(basename "$img")
    name_no_ext="${filename%.*}"

    echo "=== Prosesserer: $filename ==="

    python3 ROSIECODE/evaluate.py \
        --input_dir "$img" \
        --output_name "$name_no_ext" \
        --output_dir "$OUTPUT_DIR" \
        --model_path "$MODEL_PATH" \
        --log_output "$LOG_DIR" \
        --exclude_background \
        --stride_size 4 \
        --postprocess_image \
        --smooth_sigma 0.5
done

echo "Alle bilder er ferdig prosessert!"
