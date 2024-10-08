#!/bin/bash

threads=4  # default value

while test $# -gt 0; do
  case "$1" in
    --input)
        shift
        input=$1
        shift
        ;;
    --output)
        shift
        output=$1
        shift
        ;;
    --move_done)
        shift
        move_done=$1
        shift
        ;;
    --threads)
        shift
        threads=$1
        shift
        ;;
  esac
done

parallel -j $threads '
  base_name=$(basename -- {}); \
  base_name="${base_name%.*}"; \
  final_output_name="'$output'/${base_name}.tre" \
  iqtree2 -s {} -m MFP --quiet > $final_output_name \
  mv {} "'$move_done'/" \ 
' ::: $input/*
