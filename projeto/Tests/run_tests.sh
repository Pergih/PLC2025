#!/bin/bash

INPUT_DIR="in"
OUTPUT_DIR="out"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*; do
    filename=$(basename "$file")
    output_file="$OUTPUT_DIR/${filename%.*}.vm" 

    echo "Compilando $filename -> $output_file"

   
    python3 ../program.py < "$file" > "$output_file" 2>&1

    if [ $? -ne 0 ]; then
        echo "Erro ao compilar $filename - saída parcial em $output_file"
    else
        echo "$filename compilado com sucesso!"
    fi
done

