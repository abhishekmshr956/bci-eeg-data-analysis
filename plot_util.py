import numpy as np
import data_util
import matplotlib.pyplot as plt
import pathlib
import argparse
import ast
import re

def get_target_info(data_path):
    """ converts readme.txt into a dictionary """

    readme_file_path = data_path / 'README.txt'

    # Initialize an empty dictionary to store key-value pairs
    readme_data = {}

    with open(readme_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Split each line into key and value using the ':' as a separator
        split_result = line.split(':', 1)

        # check if the split result has at least two elements
        if len(split_result) >= 2:
            key, value = map(str.strip, split_result)
            readme_data[key] = value

    return readme_data

def get_target_pos_dia(data_path):
    """ extracts target position and diameter from the readme.txt """
    readme = get_target_info(data_path)
    target_info = readme['Target info']
    # Use regular expressions to extract numeric values inside brackets
    values = re.findall(r'[-+]?\d*\.\d+|\d+', target_info)
    # Extract target_pos and target_size
    target_pos = [float(values[0]), float(values[1])]
    target_dia = [float(values[2]), float(values[3])]

    if target_pos[0] == -0.7 or target_pos == 0.7:
        # Define positions for 8 targets
        positions = [
            (-0.7, 0),    # Left
            (0.7, 0),     # Right
            (0, 0.7),     # Up
            (0, -0.7),    # Down
            (-0.495, 0.495),  # LeftUp
            (-0.495, -0.495), # LeftDown
            (0.495, 0.495),   # RightUp
            (0.495, -0.495)   # RightDown
        ]

    return positions, target_dia[0]