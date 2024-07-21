#!/bin/bash

threads=4  # default value

while test $# -gt 0; do
  case "$1" in
    --input)
        shift
        input=$1
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

export output
export move_done

# Store sorted file names into an array
files=($(ls -Sr $input/*.fa))

# Use the array for parallel processing
parallel -j $threads '
  iqtree2 -s {} -m MFP --quiet; \
  mv "$input/{}" "$move_done/" \
' ::: "${files[@]}"
