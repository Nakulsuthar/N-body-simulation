"""
database.py
-----------
Provides data and initialization functions for the N-body simulation.

Includes:
    - generate_star_cluster: Randomized cluster of N stars
    - load_solar_system: Predefined solar system setup
    - get_objects_from_user: Manual object input
"""

import numpy as np

G = 6.67430e-20 # Gravitational constant (km^3 kg^-1 s^-2)

# -------------------------------------------------------------
# Object Class
# -------------------------------------------------------------
class Object:
    def __init__(self, name, mass, position, velocity):
        """
        Represents a celestial body in the simulation.

        Args:
            name (str): Name of the object.
            mass (float): Mass of the object (kg).
            position (list[float]): Initial [x, y, z] position (km).
            velocity (list[float]): Initial [vx, vy, vz] velocity (km/s).
        """
        self.name = name
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.zeros(3, dtype=float)

# -------------------------------------------------------------
# Option 1: Generate Random Star Cluster
# -------------------------------------------------------------

def get_star_cluster(n_stars=100):
    
    R = 5e9 # cluster radius in km
    v_scale = 5.0  # velocity scale in km/s

    bodies = []
    for i in range(n_stars):
        # Random position inside a sphere
        pos = np.random.normal(size=3)
        pos /= np.linalg.norm(pos)
        pos *= np.random.uniform(0, R)

        # Randomized mass (0.05 - 10 solar mass)
        mass = np.random.uniform(1e29, 2e31)

        # Randomized velocity (Gaussian distribution)
        vel = np.random.normal(0, v_scale, size=3)

        bodies.append(Object(
            name=f"Star{i+1}",
            mass=mass,
            position=pos,
            velocity=vel
        ))

    return bodies

# -------------------------------------------------------------
# Option 2: Predefined Solar System
# -------------------------------------------------------------


from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel
t = Time("2026-01-01 17:24:00.0", scale="tdb")

sun_data = get_body_barycentric_posvel("sun", t, ephemeris="jpl") 
position_sun = sun_data[0].xyz.to("km").value 
velocity_sun = sun_data[1].xyz.to("km/s").value 

mer_data = get_body_barycentric_posvel("mercury", t, ephemeris="jpl") 
position_mer = mer_data[0].xyz.to("km").value 
velocity_mer = mer_data[1].xyz.to("km/s").value 

ven_data = get_body_barycentric_posvel("venus", t, ephemeris="jpl") 
position_ven = ven_data[0].xyz.to("km").value 
velocity_ven = ven_data[1].xyz.to("km/s").value 

ear_data = get_body_barycentric_posvel("earth", t, ephemeris="jpl") 
position_ear = ear_data[0].xyz.to("km").value 
velocity_ear = ear_data[1].xyz.to("km/s").value 

mar_data = get_body_barycentric_posvel("mars", t, ephemeris="jpl") 
position_mar = mar_data[0].xyz.to("km").value 
velocity_mar = mar_data[1].xyz.to("km/s").value 

jup_data = get_body_barycentric_posvel("jupiter", t, ephemeris="jpl") 
position_jup = jup_data[0].xyz.to("km").value 
velocity_jup = jup_data[1].xyz.to("km/s").value 

sat_data = get_body_barycentric_posvel("saturn", t, ephemeris="jpl") 
position_sat = sat_data[0].xyz.to("km").value 
velocity_sat = sat_data[1].xyz.to("km/s").value 

ura_data = get_body_barycentric_posvel("uranus", t, ephemeris="jpl") 
position_ura = ura_data[0].xyz.to("km").value 
velocity_ura = ura_data[1].xyz.to("km/s").value 

nep_data = get_body_barycentric_posvel("neptune", t, ephemeris="jpl") 
position_nep = nep_data[0].xyz.to("km").value 
velocity_nep = nep_data[1].xyz.to("km/s").value 

def get_solar_system():
    """
    Loads a sourced solar system model (Sun + 8 planets).

    Returns:
        list: List of CelestialBody objects.
    """
    bodies = [
        Object(name="Sun", mass=1.989e30, position=position_sun, velocity=velocity_sun),
    Object(name="Mercury", mass=3.285e23, position=position_mer, velocity=velocity_mer),
    Object(name="Venus",   mass=4.867e24, position=position_ven, velocity=velocity_ven),
    Object(name="Earth",   mass=5.972e24, position=position_ear, velocity=velocity_ear),
    Object(name="Mars",    mass=6.39e23,  position=position_mar, velocity=velocity_mar),
    Object(name="Jupiter", mass=1.898e27, position=position_jup, velocity=velocity_jup),
    Object(name="Saturn",  mass=5.683e26, position=position_sat, velocity=velocity_sat),
    Object(name="Uranus",  mass=8.681e25, position=position_ura, velocity=velocity_ura),
    Object(name="Neptune", mass=1.024e26, position=position_nep, velocity=velocity_nep),
    ]
    return bodies

# -------------------------------------------------------------
# Option 3: Manual User Input
# -------------------------------------------------------------
def get_objects_from_user(num_bodies):
    """
    Prompts user to manually input celestial objects.

    Args:
        num_bodies (int): Number of objects to input.

    Returns:
        list: List of CelestialBody objects.
    """
    bodies = []
    for i in range(num_bodies):  # Loop starts from i=0 to num_bodies-1
        print(f"\n--- Enter data for Object {i+1} ---")  # Correct numbering
        
        name = input("Name: ")
        mass = float(input("Mass (kg): "))

        # Position input
        while True:
            try:
                pos = list(map(float, input("Position x y z (in km): ").split()))
                if len(pos) != 3:
                    raise ValueError("Please enter exactly 3 values for position.")
                break
            except ValueError as e:
                print(f"⚠️ {e} Try again.")

        # Velocity input
        while True:
            try:
                vel = list(map(float, input("Velocity vx vy vz (in km/s): ").split()))
                if len(vel) != 3:
                    raise ValueError("Please enter exactly 3 values for velocity.")
                break
            except ValueError as e:
                print(f"⚠️ {e} Try again.")

        # Convert km to meters for simulation
        bodies.append(Object(name, mass, position=pos, velocity=vel))

    print(f"✅ Loaded {len(bodies)} objects from user input.")
    return bodies

    
