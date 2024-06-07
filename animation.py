from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Step 1: Read CSV File
data = pd.read_csv('coordinates.csv', names=['latitude', 'longitude'])

# Step 2: Create Map
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(data['longitude'].min(), data['longitude'].max())
ax.set_ylim(data['latitude'].min(), data['latitude'].max())

# Initialize an empty scatter plot
scatter = ax.scatter([], [], s=0.5, color='white')

# Set figure background color and remove axes
ax.set_facecolor('#202020')
fig.patch.set_facecolor('#202020')

ax.set_xticks([])
ax.set_yticks([])

sides = ['top', 'right', 'bottom', 'left']

for side in sides:
    ax.spines[side].set_visible(False)

# Step 3: Animate

# Number of points to display at a time. By default display all points
buffer_size = len(data)


def update(frame):
    start_idx = max(0, frame - buffer_size)
    end_idx = frame
    scatter.set_offsets(
        data[['longitude', 'latitude']].values[start_idx:end_idx])

    # Debug Only
    print(f'Frame: {frame}/{len(data)}', end='\r')

    return scatter,


ani = FuncAnimation(fig, update, frames=np.arange(
    0, len(data), 100), interval=200, blit=True)

# Step 4: Save Animation
ani.save('animation.mp4', writer='ffmpeg')
plt.show()
