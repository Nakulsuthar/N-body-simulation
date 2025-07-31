from database import get_star_cluster,get_objects_from_user,get_solar_system
from method import compute_gravitational_accelerations,verlet_integration,check_and_merge_collisions
import numpy as np
from tqdm import tqdm

"""
main.py
--------
Main driver script for the N-body simulation.

Features:
    - Option 1: Generate random star cluster
    - Option 2: Load predefined solar system
    - Option 3: Input objects manually
    - Runs simulation using Verlet integration
    - Handles collisions and saves snapshots

Usage:
    python main.py
"""
# -------------------------------------------------------------
# Simulation setup: Choose initialization method
# -------------------------------------------------------------
print("\nChoose initial setup:")
print("1 - Generate objects manually")
print("2 - Generate predefined solar system")
print("3 - Generate star cluster")
choice = input("Enter 1, 2, or 3: ")

if choice == "1":
    num_objects = int(input("How many objects do you want to simulate "))
    bodies = get_objects_from_user(num_objects)     # Option 1: Manual object input
    print("✅ Loaded objects from user input.")
elif choice == "2":
    bodies = get_solar_system()         # Option 2: Predefined solar system
    print("✅ Loaded predefined solar system.")
elif choice == "3":
    num_objects = int(input("How many stars do you want in this cluster "))
    bodies = get_star_cluster(num_objects)  # Option 3: Random star cluster
    print("✅ Generated a star cluster ")
else:
    print("❌ Invalid choice! Defaulting to predefined solar system.")
    bodies = get_solar_system()

num_years = int(input("How many years do you want to run it for "))
# -------------------------------------------------------------
# Initial acceleration computation
# -------------------------------------------------------------
compute_gravitational_accelerations(bodies)

# -------------------------------------------------------------
# Simulation parameters
# -------------------------------------------------------------
dt = 36000          # Time step (10 hour)
steps = 876 *num_years     # Number of steps (~1 year if dt=10 hour)
Data = []           # Stores snapshots for visualization

# -------------------------------------------------------------
# Main simulation loop
# -------------------------------------------------------------
for step in tqdm(range(steps), desc="Simulating", unit="step"):
    # 1️⃣ Update positions and velocities
    verlet_integration(bodies, dt)

    # 2️⃣ Check for collisions AFTER movement
    check_and_merge_collisions(bodies, collision_distance=1e7)

    # 3️⃣ Save snapshots every 10 steps
    if step % 10 == 0:
        snapshot = {}
        for obj in bodies:
            snapshot[obj.name] = [obj.position[0], obj.position[1], obj.position[2]]
        Data.append(snapshot)

    # 4️⃣ Continuously save progress
    np.save("simulation.npy", Data, allow_pickle=True)

print("✅ Simulation complete. Results saved to simulation.npy")
print("▶ To view results in 3D, run: python animation.py")
