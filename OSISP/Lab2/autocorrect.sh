#!/bin/bash

input_file="input.txt"
output_file="output.txt"

if [ ! -f "$input_file" ]; then
    echo "Error: File '$input_file' not found." >&2
    exit 1
fi

sed -E ':a;N;$!ba;
  s/^[[:space:]]*([[:lower:]])/\U\1/;
s/([.!?])([[:space:]\n]+)([[:lower:]])/\1\2\u\3/g' "$input_file" > "$output_file"
