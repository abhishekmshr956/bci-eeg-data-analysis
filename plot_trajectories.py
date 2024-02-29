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
    print(readme_file_path)

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

    return target_pos, target_dia[0]


def plot_trajectories(session):
    datadir = pathlib.Path('/data/raspy/')
    data_path = datadir / session

    # read the target position and diameter from the readme.txt
    target_pos, target_dia = get_target_pos_dia(data_path)
    

   
    


    

  



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('session_name', help='session name to plot the trajectories')

    args = parser.parse_args()
    session = args.session_name
    plot_trajectories(session)