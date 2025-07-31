"""
method.py
---------
Contains core physics functions for the N-body simulation

Includes:
    • Gravitational acceleration computation
    • Verlet integration for motion updates
    • Collision detection and merging
"""

import numpy as np

class Object:


    def __init__(self, position=np.array([0, 0, 0], dtype=float), 
                 velocity=np.array([0, 0, 0], dtype=float),
                 acceleration=np.array([0, 0, 0], dtype=float),
                 name="Object",
                 mass=1.0):
        """
        Initializes a new Planet instance and takes in arguments: 
        Position, Velocity, Acceleration, name and mass
        """
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array(acceleration, dtype=float)
        self.name = name
        self.mass = mass
        self.G = 6.67408e-20  # Gravitational constant in N·km²/kg²

    def __str__(self):
        """
        Returns a string representation of the Planet object 
        """
        return (f"Object: {self.name}, Mass: {self.mass:.3e}, "
                f"Position: {self.position}, Velocity: {self.velocity}, "
                f"Acceleration: {self.acceleration}")



def compute_gravitational_accelerations(bodies):
    """
    Computes gravitational accelerations on all bodies using Newton's Law of Gravitation.

    Formula:
        a = G * (m / r^2) * (unit vector of r)

    Args:
        bodies (list[CelestialBody]): List of celestial objects.

    Returns:
        None: Updates the `acceleration` property of each body in-place.
    """

    G = 6.67430e-20  # N·km²/kg²

    for i, obj_i in enumerate(bodies):
        total_acc = np.zeros(3)

        for j, obj_j in enumerate(bodies):
            if i == j:
                continue

            r_vec = obj_j.position - obj_i.position
            r_mag = np.linalg.norm(r_vec)

            if r_mag == 0:
                continue  # prevent division by zero

            total_acc += G * obj_j.mass * r_vec / r_mag**3

        obj_i.acceleration = total_acc

def verlet_integration(bodies, dt):
    """
    Updates positions and velocities of bodies using Velocity-Verlet integration.

    Steps:
        1. Update positions based on current velocity and acceleration.
        2. Recompute accelerations due to gravity.
        3. Update velocities using average of old and new accelerations.

    Args:
        bodies (list[CelestialBody]): List of celestial objects.
        dt (float): Time step in seconds.

    Returns:
        None: Updates positions and velocities in-place.
    """
    # Step 1: Save current accelerations
    old_accelerations = [np.copy(obj.acceleration) for obj in bodies]

    # Step 2: Update positions
    for i, obj in enumerate(bodies):
        obj.position += obj.velocity * dt + 0.5 * old_accelerations[i] * dt**2

    # Step 3: Recalculate accelerations based on new positions
    compute_gravitational_accelerations(bodies)

    # Step 4: Update velocities using average acceleration
    for i, obj in enumerate(bodies):
        obj.velocity += 0.5 * (old_accelerations[i] + obj.acceleration) * dt


def check_and_merge_collisions(bodies, collision_distance=1e7):
    """
    Detects collisions between bodies and merges them if they are closer than `collision_distance`.

    Merging is based on:
        - Conservation of momentum for velocity
        - Center of mass for position
        - Summing masses

    Args:
        bodies (list[CelestialBody]): List of celestial objects.
        collision_distance (float): Distance threshold (in meters or km depending on units).

    Returns:
        None: Modifies the list `bodies` in-place by merging colliding pairs.
        """ 
    i = 0
    while i < len(bodies):
        j = i + 1
        while j < len(bodies):
            dist = np.linalg.norm(bodies[i].position - bodies[j].position)
            if dist < collision_distance:
                # Merge
                m1 = bodies[i].mass 
                m2 = bodies[j].mass
                M = m1 + m2

                new_position = (m1 * bodies[i].position + m2 * bodies[j].position) / M
                new_velocity = (m1 * bodies[i].velocity + m2 * bodies[j].velocity) / M
                new_name = f"{bodies[i].name}+{bodies[j].name}"

                # Update body i
                bodies[i].position = new_position
                bodies[i].velocity = new_velocity
                bodies[i].mass = M
                bodies[i].name = new_name

                print(f"✅ MERGED: {bodies[i].name} at distance {dist:.2e} km")
                print(f"New Mass:{bodies[i].mass} and new vel{bodies[i].velocity}")

                # Remove body j
                bodies.pop(j)

                # ⚠️ DO NOT increment j here, as the list has shifted
            else:
                j += 1
        i += 1