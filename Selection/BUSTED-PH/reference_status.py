"""
Context: We need Hyphy-Busted-PH (https://github.com/veg/hyphy-analyses/tree/master/BUSTED-PH) to test 
the presence/absense of selection pressures on branches in context of other branches.
To do this, we need to label which branches are references and which are background.
This script wraps functions from ETE3, polars and python-newick that enable it to take a regular newick file and convert it to 
a labelled newick file that is suitable for BUSTED-PH processing.
"""

# Dependencies!

from ete3 import Tree
import os
import newick
import polars as pl
#import ete3
import argparse
import re
import glob
import pickle

# Set up the CLI
parser = argparse.ArgumentParser(description = """
                                Context: We need Hyphy-Busted-PH (https://github.com/veg/hyphy-analyses/tree/master/BUSTED-PH) to test 
                                the presence/absense of selection pressures on branches in context of other branches.
                                To do this, we need to label which branches are references and which are background.
                                This script wraps functions from ETE3, polars and python-newick that enable it to take a regular newick file and convert it to 
                                a labelled newick file that is suitable for BUSTED-PH processing.
                                     
                                 """)

parser.add_argument('-d','--dict',help= "The dict that indicates which species codes are reference and which are test.")
parser.add_argument('-t','--tree',help = "The tree that you want wrangled")
parser.add_argument('-o','--output', help= "The path to the ouput, defaults to current directory.")

args = parser.parse_args()

# Functions

def lines_to_dict(read_lines:list, sep:str = "\t"):
    
    dict_one = {}
    
    '''
    Does: 
        Takes a list made of `readlines()` and for each line returns a dictionary type object
    
    Arguments:
        A list where each item is a line and the first item is a species code and second item is species names in the fashion of first_second
        separator that defaults to "\t"
    
    Returns:
        A dict where the keys are species codes and values are species names
    '''
    for i in read_lines:
        
        i = i.rstrip()
        
        i = i.rsplit(sep)
        
        dict_one[i[0]] = i[1]
    
    return dict_one

def append_reference_status(tree,my_dict):
    
    """
    Written for: Convienience
    
    Context:
        I have gene treefiles in newick format and I need to wrangle the strings in the names of the genes at the species level.
        For example:
            If I have a two genes in the newick file from one species each:
                a. Gene-ABCD-1234
                b. Gene-EFGH-5678
            Now, the sub-string "ABCD" identifies the first species and the sub-string "EFGH" identifies the second. 
            I need to add the code "{reference}" to the gene's name because `Hyphy BUSTED-PH` expects that in its input.
        
        My solution here is to have a dictionary that pairs the species code (sub-)string as keys with the status of the species as the value i.e. "{"ABCD": "reference", "EFGH":"background"}".
        
        I iterate through the nodes of the tree, iterate through the keys of the dict i.e. the species code (sub-)sting (double nested for-loops, what blasphemy!) and if the node's name has the species key (sub-)string, I append "reference" to the node's name.
        
    Does:
        Takes a ete3 Treefile object and a dictionary.
        The dictionary should have keys that are the species code (sub-)strings and the values indicate whether the species is of type reference or not. And use this relationship to wrangle the newick file.
    """
    
    for node in tree:
        for code in my_dict:
            if ((code in node.name) and (my_dict.get(code) == "test")):
                node.name += "{test}"
            elif ((code in node.name) and (my_dict.get(code) != "test")):
                node.name += "{reference}"
            else:
                continue
    
    return tree


def replace_dots(text):
    """
    Replace all '.' with '_' and then replace all '_{' with '{'
    This is necessary becasue '.' confuse BUSTED-PH
    """
    text = re.sub(r'\.', '_', text)
    text = re.sub(r'_\{', '{', text)
    return text
# Wranlging and interactions with inputs

## placeholder for the tree that will be read in

## Read the species code file in and convert it to a dict and keep it around for futher use.

species_keys_path = args.dict

with open(species_keys_path,"r") as current_file:
    lines = current_file.readlines()

species_dict = lines_to_dict(lines)

## now bring in the tree

path_to_tree = args.tree

my_tree = Tree(path_to_tree)

fixed_tree = append_reference_status(my_tree,species_dict)

# Account for the fact that BUSTED-PH needs to avoid '.'s in gene names
for node in fixed_tree:
    
    node.name = replace_dots(node.name)

# write to file!
if args.output is not None:

    fixed_tree.write(format=1,outfile=args.output)

else:

    base_name = '.'.join(os.path.basename(path_to_tree).rsplit(".")[0:-1])

    fixed_tree.write(format=1,outfile=f"{base_name}.new.nwk")   
