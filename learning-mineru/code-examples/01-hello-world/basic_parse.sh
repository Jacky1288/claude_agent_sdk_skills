#!/bin/bash
# Basic MinerU parsing example
#
# Usage: ./basic_parse.sh <input.pdf>
#
# This script demonstrates the simplest way to use MinerU

if [ $# -eq 0 ]; then
    echo "Usage: $0 <input.pdf>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_DIR="output"

echo "Parsing: $INPUT_FILE"
echo "Output will be saved to: $OUTPUT_DIR"

# Run MinerU with default settings (hybrid backend)
mineru -p "$INPUT_FILE" -o "$OUTPUT_DIR"

echo "Done! Check output at: $OUTPUT_DIR"
