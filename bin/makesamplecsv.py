#!/usr/bin/env python3

# Author: lanadelrea, 08MAY2025

# Import modules
import pandas as pd
import sys
import os
import glob
import re

# Get absolute path to input directory containing the paired end sequences
sampledir = sys.argv[1]
if not os.path.isabs(sampledir):
    sampledir = os.path.abspath(sampledir)

# Get the list of files in the input directory
def get_filepaths(directory):
    """
    This function will get the absolute path
    of the samples in the input directory
    and store them in a list
    """

    file_paths = [] # List where to store the file paths

    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".fastq.gz"): # Only the fastq files
                filepath = os.path.join(root, filename) # Get the absolute path
                file_paths.append(filepath) # Write the absolute paths in the list

    return file_paths

file_paths = get_filepaths(sampledir)

print(file_paths)

def get_samplename(directory):
    """
    This function will list the sample names from the filename
    """

    sample_name = [] # List where to store the sample names

    for files in glob.glob(directory):
                filename = os.path.split(files)[-1]
                pattern = re.compile(r"([A-Za-z0-9]+(-[A-Za-z0-9]+)+)", re.IGNORECASE) # Get the name pattern
                sample = pattern.match(filename) # Match the pattern to the filename
                sample_name.append(sample)

    return sample_name

samples = get_samplename(sampledir)

print(samples)

# Create dataframe of the list of filepaths
#df = pd.DataFrame({'paths':full_file_paths})