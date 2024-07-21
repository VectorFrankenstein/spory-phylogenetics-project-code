import argparse

parser = argparse.ArgumentParser(description='Convert a list of BUSCO JSONs into a table.')

parser.add_argument('-i', '--input', required=True, help='The directory that has the BUSCO JSONs.')
parser.add_argument('-o', '--output', default = "json_scores", help='What should be the name of the table file.')

args = parser.parse_args()

# %%
import json

# %%
import glob

# %%
import polars as pl

# %%
import os

# %%
list_of_files_path = args.input

# %%
def busco_json_convienience_function(my_data:dict):
    """

    This is a convienience function meant to pull the following key values out of the the json dict.

    1. "Complete percentage"
    2. "Single copy percentage"
    3. "Multi copy percentage"
    4. "Fragmented percentage"
    5. "Missing percentage"

    Inputs:
        1. Supply a busco json as a dict

        2. Name of the JSON/dict
    """

    subset_dict = dict()

    # The field "results" is the one that has all the percentage values
    results_field = my_data.get("results",{})

    keys_to_include = [
        "Complete percentage",
        "Single copy percentage",
        "Multi copy percentage",
        "Fragmented percentage",
        "Missing percentage"
    ]

    subset_dict = {k: results_field.get(k,"N/A") for k in keys_to_include}

    return(subset_dict)

# %%
list_of_files = glob.glob(list_of_files_path + "*.json") # This makes it so that the only json are read in.

# %%
json_names = [os.path.basename(i).split(".")[0] for i in list_of_files]

# %%
all_jsons = []

for current_json in list_of_files:

    # Get just the basename without extension
    base_name = os.path.basename(current_json).split(".")[0]

    # Open the JSON file
    with open(current_json, 'r') as f:
        # Parse the JSON data into a Python dictionary
        data = json.load(f)

    base_name = busco_json_convienience_function(data)

    all_jsons.append(base_name)

# %%
percentages = pl.DataFrame(all_jsons)

# %%
# Add names to the percentages

perecentages_with_names = pl.DataFrame({
    "source": json_names
}).with_columns(percentages)


final_output_name = f"{args.output}.tsv"

# %%
perecentages_with_names.write_csv(final_output_name,separator="\t")
