#!/usr/bin/env python3

# Author: lanadelrea, 08MAY2025

# Import modules
import pandas as pd
import sys
import os

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
    Input: Directory containing the samples
    Output: List of the filepaths for each fastq.gz file
    """
    file_paths = [] # List where to store the file paths
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".fastq.gz"): # Only the fastq.gz files
                filepath = os.path.join(root, filename) # Get the absolute path
                file_paths.append(filepath) # Write the absolute paths in the list
    return file_paths

file_paths = get_filepaths(sampledir)

def sort_R1(paths):
    """
    This function sorts the forward and reverse file paths
    Input: All the paths
    Output: Sorted forward and reverse file paths
    """
    R1_paths = []
    R2_paths = []
    for files in paths:
        direction = (os.path.basename(files)).split("_")[3]
        if direction == 'R1':
            R1_paths.append(files)
        elif direction == 'R2':
            R2_paths.append(files)
    return R1_paths, R2_paths

R1_paths, R2_paths = sort_R1(file_paths) 

def get_samplename(paths):
    """
    This function will list the sample names
    Input: File paths
    Output: Sample names
    """
    sample_name = [] # List where to store sample names
    for files in paths:
        filename = (os.path.basename(files)).split("_")[0] # First get the filename with extension then spilt the filename using '_' and get the first string
        sample_name.append(filename) # Populate the list
    return sample_name

R1_samples = get_samplename(R1_paths)
R2_samples = get_samplename(R2_paths)

# Create dataframe of the list of sample name with their corresponding file paths then print to samplesheet.csv
df_R1 = pd.DataFrame({'sample':R1_samples, 'fastq_1':R1_paths})
df_R2 = pd.DataFrame({'sample':R2_samples, 'fastq_2':R2_paths})
df = pd.merge(df_R1, df_R2, on='sample', how='inner')
df.set_index('sample', inplace=True)
df.to_csv("samplesheet.csv", sep=",") 