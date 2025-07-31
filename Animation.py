"""
Animation.py
------------
Visualizes saved N-body simulation data as a 3D animation using Matplotlib.

Features:
    • Loads simulation snapshot data from a .npy file.
    • Dynamically detects and tracks object positions.
    • Creates animated 3D scatter plots with trails for each object.
    • Uses a dark-space theme for realistic visualization.

Usage:
    python Animation.py

Requirements:
    - Ensure 'simulation.npy' (or desired .npy file) is present in the directory.
    - Generated from running `main.py`.

Modules:
    - numpy: For numerical operations and array handling.
    - matplotlib.pyplot: For plotting and rendering.
    - matplotlib.animation.FuncAnimation: For creating animations.
    - mpl_toolkits.mplot3d: For 3D visualization.
    """

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# ========================
# Load simulation data
# ========================
data = np.load("simulation.npy", allow_pickle=True)

# Collect all object names dynamically from every frame
object_names = set()
for snapshot in data:
    object_names.update(snapshot.keys())
object_names = sorted(object_names)

# ========================
# Figure setup
# ========================
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("N Body Simulation",color='white', fontsize=16, fontweight='bold')
ax.set_xlabel("X (km)")
ax.set_ylabel("Y (km)")
ax.set_zlabel("Z (km)")


# Automatic Axes limit
all_positions = np.array([
    pos for snapshot in data for pos in snapshot.values()
])
x_min, x_max = np.min(all_positions[:, 0]), np.max(all_positions[:, 0])
y_min, y_max = np.min(all_positions[:, 1]), np.max(all_positions[:, 1])
z_min, z_max = np.min(all_positions[:, 2]), np.max(all_positions[:, 2])
padding = 0.1
x_pad = (x_max - x_min) * padding
y_pad = (y_max - y_min) * padding
z_pad = (z_max - z_min) * padding

# Apply limits
ax.set_xlim(x_min - x_pad, x_max + x_pad)
ax.set_ylim(y_min - y_pad, y_max + y_pad)
ax.set_zlim(z_min - z_pad, z_max + z_pad)


# Dark theme
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')
ax.tick_params(colors='white')
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.line.set_color("white")
    axis.set_pane_color((0, 0, 0, 1))

# ========================
# Initialize scatters & trails
# ========================
scatters = {}
trails = {}
TRAIL_LENGTH = 20000

for name in object_names:
    scatters[name] = ax.scatter([], [], [], s=10, label=name)  # Fixed size
    trails[name], = ax.plot([], [], [], lw=1)

#ax.legend(loc='upper left',fontsize=8)

# ========================
# Animation update function
# ========================
def update(frame):
    """Updates scatter positions and trails for each frame in the animation.

    Args:
        frame (int): Frame index representing current simulation step.

    Returns:
        list: Updated scatter plot artists for blitting.
    """
    current_snapshot = data[frame]

    for name in object_names:
        if name in current_snapshot:
            obj_data = current_snapshot[name]
            pos = obj_data[:3]

            # Update scatter position (fixed size)
            scatters[name]._offsets3d = ([pos[0]], [pos[1]], [pos[2]])

            # Update trails
            trail_data = [
                snap[name][:3] for snap in data[max(0, frame - TRAIL_LENGTH):frame + 1]
                if name in snap
            ]
            trail_data = np.array(trail_data)
            trails[name].set_data(trail_data[:, 0], trail_data[:, 1])
            trails[name].set_3d_properties(trail_data[:, 2])

            # Show active objects
            scatters[name].set_alpha(1.0)
            trails[name].set_alpha(1.0)
        else:
            # Hide merged/inactive objects
            scatters[name].set_alpha(0.0)
            trails[name].set_alpha(0.0)

    return list(scatters.values()) + list(trails.values())

# ========================
# Run animation
# ========================
ani = FuncAnimation(fig, update, frames=len(data), interval=3, blit=False)
plt.tight_layout()
plt.show()

