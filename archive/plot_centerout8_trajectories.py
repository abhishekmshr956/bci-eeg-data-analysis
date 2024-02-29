import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.collections
import data_util

sessions = ['2024-02-02_H2_CL_5'] # all the sessions for which to plot the trajectories
# sessions = ['2024-01-15_H1_CL_2'] # all the sessions for which to plot the trajectories

def get_trials_indices(session):
    """ given a sesssion name, return task_data, the start and end of center-out trials"""
    task_data = data_util.load_data(f'/data/raspy/{session}/task.bin')
    # print(np.unique(task_data['state_task'], return_counts=True)) # 99 is for center target, 0: left, 1: right, 2: up, 3: down, 5: leftup, 6: leftdown, 7: rightup, 8:rightdown)
    trial_start_inds = np.nonzero((task_data['state_task'][0:-1] == 99)*(task_data['state_task'][1:None] != 99))[0] + 1
    trial_end_inds = np.nonzero((task_data['state_task'][0:-1] != 99)*(task_data['state_task'][1:None] == 99))[0] + 1 # last index containing the same state_task
    if trial_start_inds[0] < trial_end_inds[0]:
        trial_start_inds = trial_start_inds[0:len(trial_end_inds)] # only use trials that end.
    else:
        # For when there's an end before a start. Not sure why this happens.
        trial_end_inds = trial_end_inds[1:None]
        trial_start_inds = trial_start_inds[0:len(trial_end_inds)] # only use trials that end.
    return task_data, trial_start_inds, trial_end_inds

# Define colors for 8 targets
colors = ['r', 'g', 'b', 'm', 'c', 'y', 'k', 'orange']

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

# Create 8 subplots
fig, axes = plt.subplots(2, 4, figsize=(15, 10))
# Flatten the axes array to iterate over it easily
axes = axes.flatten()

for session in sessions:
    task_data, trial_start_inds, trial_end_inds = get_trials_indices(session)
    print(len(trial_start_inds), len(trial_end_inds))
    for trial_no, (start, end) in enumerate(zip(trial_start_inds, trial_end_inds)):
        xy = task_data['decoded_pos'][start:end]
        target_no = int(task_data['state_task'][start].item())
        if target_no > 3:
            target_no -= 1
        ax = axes[target_no]
        ax.plot(xy[:, 0], xy[:, 1], color = colors[target_no])
        # print('Hello')
        # circle = plt.Circle(positions[target_no], 0.39/2, color=colors[target_no], alpha=0.1)
        # ax.add_patch(circle)

        # Set axis limits
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.tight_layout()
        # print(f"Session: {session}, Trial: {trial_no}, Target: {target_no}, Data Shape: {xy.shape}")
# target_nos = task_data['state_task'][trial_start_inds]
# for target_no, ax in enumerate(axes):
#     if target_no > 3:
#         target_no += 1
#     ax.set_title( str(int(np.sum(target_nos == target_no))))

# Fill areas with circles for 8 targets
for i in range(8):
    circle = plt.Circle(positions[i], 0.4/2, color=colors[i], alpha=0.4, zorder=-4)
    cursor = plt.Circle((0.0, 0.0), 0.1/2, color='gray', alpha=0.4, zorder=-4)
    ax = axes[i]
    # Draw a bounding box
    ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'gray', alpha=0.3, zorder=-3)
    ax.add_patch(circle)
    ax.add_patch(cursor)

# # Fill areas with rectangles for 8 targets
# for i in range(8):
#     rect_width = 0.4
#     rect_height = 0.4
#     rect = plt.Rectangle((positions[i][0] - rect_width / 2, positions[i][1] - rect_height / 2),
#                          rect_width, rect_height, color=colors[i], alpha=0.4, zorder=-4)
    
#     cursor = plt.Circle((0.0, 0.0), 0.1/2, color='gray', alpha=0.4, zorder=-4)
#     ax = axes[i]
#     # Draw a bounding box
#     ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'gray', alpha=0.3, zorder=-3)
#     ax.add_patch(rect)
#     ax.add_patch(cursor)

fig.savefig('figures/2024-02-02_H2/CL_5_separate_targets.pdf')
fig.savefig('figures/2024-02-02_H2/CL_5_separate_targets.png')

