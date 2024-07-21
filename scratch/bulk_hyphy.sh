#!/bin/bash

# Define the directories
trees_dir="/home/powertower/work_in_progress/targeted_list_busted/iqtree_targeted_gene_trees"
fas_dir="/home/powertower/work_in_progress/targeted_list_busted/targeted_families"

# Iterate over the tree files
for tree_file in "$trees_dir"/*.treefile; do
    # Extract the basename by removing the path and extension
    base_name=$(basename "$tree_file" .treefile)

    # Remove any additional extensions from the basename
    base_name=${base_name%%.*}

    # Construct the paths to the tree and fasta files
    tree_path="$trees_dir/$base_name.no_duplicates.fa.treefile"
    fasta_path="$fas_dir/$base_name.no_duplicates.fa"

    # Run the hyphy command
    hyphy BUSTED-PH.bf --alignment "$fasta_path" --tree "$tree_path" --srv No --branches test --comparison reference
done
