import numpy as np
import data_util
import matplotlib.pyplot as plt
import pathlib
import math
import argparse

from scipy.stats import ttest_ind
from plot_util import get_target_pos_dia

def get_task_data(session):
    """ returns task_data, state_task, start and end indices for a session """
    datadir = pathlib.Path('/data/raspy/')
    task_data = data_util.load_data(datadir / session / 'task.bin')
    state_task = task_data['state_task'].flatten().copy()
    state_task[task_data['numCompletedBlocks'].flatten() < 0] = 99

    start_inds = np.nonzero(state_task[1:None] != state_task[0:-1])[0][1:None] + 1
    end_inds = np.hstack([start_inds[1:None], [len(state_task)+1]])

    return task_data, state_task, start_inds, end_inds

def calculate_distance(x1, y1, x2, y2):
    """ calculates euclidean distance between two points """
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def total_distance_traveled(positions):
    """ calculates the total distance along a path given by positions """
    total_distance = 0.0

    for i in range(1, len(positions)):
        x1, y1 = positions[i-1]
        x2, y2 = positions[i]
        total_distance += calculate_distance(x1, y1, x2, y2)

    return total_distance

def path_efficiency(cursor_positions, target_position):
    """ calculate path efficiency """
    straight_distance = target_position # assume that the cursor starts from the center. This is not always the case however
    total_distance = total_distance_traveled(cursor_positions)

    efficiency = (straight_distance / total_distance) * 100.0

    return efficiency

def calculate_efficiency_array(session):
    task_data, state_task, start_inds, end_inds = get_task_data(session)

    # read the target position and diameter from the readme.txt
    datadir = pathlib.Path('/data/raspy/')
    data_path = datadir / session
    positions, _ = get_target_pos_dia(data_path)

    efficiency_array = []

    for start, end in zip(start_inds, end_inds):
        xy = task_data['decoded_pos'][start:end]
        target = state_task[start]
        if target != 99:
            efficiency = path_efficiency(xy, np.abs(positions[0][0]))
            efficiency_array.append(efficiency)

    mean_efficiency = np.mean(efficiency_array)
    std_dev_efficiency = np.std(efficiency_array)

    return efficiency_array, mean_efficiency, std_dev_efficiency

def plot_path_efficiency(sessions):
    """ plot path efficieny. currently optimised for comparing two sessions only. """
    session1, session2 = sessions
    efficiency_array_session1, mean_efficiency_session1, std_dev_efficiency_session1 = calculate_efficiency_array(session1)
    efficiency_array_session2, mean_efficiency_session2, std_dev_efficiency_session2 = calculate_efficiency_array(session2)

    t_stat, p_value = ttest_ind(efficiency_array_session1, efficiency_array_session2)
    significant_difference_stars = '*' * (int(-np.log10(p_value)) - 1) if p_value < 0.05 else ''

    fig, ax = plt.subplots(figsize= (6, 6))

    # Bar plots for mean efficiency
    ax.bar(0.5, mean_efficiency_session1, color = 'blue', width = 0.2, label = 'Mean without copilot')
    ax.bar(0.8, mean_efficiency_session2, color = 'red', width = 0.2, label = 'Mean with copilot')

    ax.scatter(np.ones(len(efficiency_array_session1)) * 0.5, efficiency_array_session1, color = 'black', marker = 'o', alpha = 0.5)
    ax.scatter(np.ones(len(efficiency_array_session2)) * 0.8, efficiency_array_session2, color = 'black', marker='o', alpha = 0.5)

    ax.errorbar(0.5, mean_efficiency_session1, yerr = std_dev_efficiency_session1, color = 'blue', capsize = 5, capthick = 2, alpha = 0.6)
    ax.errorbar(0.8, mean_efficiency_session2, yerr = std_dev_efficiency_session2, color = 'red', capsize = 5, capthick = 2, alpha = 0.6)

    ax.annotate(significant_difference_stars, xy=(0.75, mean_efficiency_session2 + 3.0), fontsize=12, ha = 'center', va = 'center', color = 'black')

    ax.set_xticks([0.5, 0.8])
    ax.set_xticklabels(['Without copilot', 'With copilot'])
    ax.set_ylabel('Path Efficiency (%)')
    ax.set_ylim(0, 100)
    ax.legend(loc='upper left')

    plt.title(f'Path Efficiency Comparison')
    plt.tight_layout()
    plt.savefig(f'figures/path_efficiency_plots/{session1}_2_Pathefficiency.pdf', bbox_inches='tight')

    print(f'\nMean Path Efficiency: {mean_efficiency_session1:.2f}%')
    print(f'Standard Deviation of Path Efficiency: {std_dev_efficiency_session1:.2f}')

    print(f'\nMean Path Efficiency: {mean_efficiency_session2:.2f}%')
    print(f'Standard Deviation of Path Efficiency: {std_dev_efficiency_session2:.2f}')

    print(f'\np value: {p_value}')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('session_names', nargs=2, help='session names to compare the path efficiencies')

    args = parser.parse_args()
    sessions = args.session_names
    plot_path_efficiency(sessions)