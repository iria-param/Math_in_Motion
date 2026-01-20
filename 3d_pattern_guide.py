"""
CONVERTING 2D PATTERNS TO 3D PATTERNS
=====================================

There are two approaches:

1. JOINT SPACE 3D (Current - simpler, safer)
   - Vary all 6 joint angles to create 3D motion
   - What: Directly control joint angles
   - How: Combine variations in j1, j2, j3 to create 3D paths
   - Pro: Safe, predictable, no IK needed
   - Con: Less precise end-effector positioning

2. CARTESIAN SPACE 3D (Advanced - more accurate)
   - Define exact 3D positions (X, Y, Z)
   - What: Define TCP (tool center point) positions
   - How: Use forward kinematics to convert to joint angles
   - Pro: Precise paths in workspace
   - Con: More complex, needs IK

We'll implement both!
"""

import math
import numpy as np
from pattern_generator import PatternGenerator

print("=" * 70)
print("3D PATTERN CONVERSION GUIDE")
print("=" * 70)

print(__doc__)

print("\n" + "=" * 70)
print("APPROACH 1: ENHANCED JOINT SPACE 3D (Recommended)")
print("=" * 70)

print("""
CURRENT LIMITATION:
- Most patterns only vary j1 (base) and j2 (shoulder)
- j3-j6 have minimal variation
- Result: Mostly 2D motion

SOLUTION:
- Add more variation to j3 (elbow) for vertical/depth motion
- Vary j4, j5, j6 (wrist) for orientation changes
- Combine them for true 3D patterns

Example: 3D Box Pattern
j1 varies left/right (X)
j2 varies up/down (Y)
j3 varies forward/back (Z)
j4, j5, j6 add wrist rotation

""")

print("\n" + "=" * 70)
print("APPROACH 2: CARTESIAN SPACE 3D (For precise positioning)")
print("=" * 70)

print("""
Define patterns in 3D coordinates (X, Y, Z):

Instead of:
  j1 = 0.2, j2 = -1.5, j3 = 1.6, ...

Define:
  X = 0.5m (right)
  Y = 0.3m (forward)
  Z = 0.8m (height)

Then convert to joint angles using forward/inverse kinematics.

UR10 Kinematics Parameters (DH):
  Link 0: Base offset = 0.08916 m (height)
  Link 1: Length = 0.13585 m
  Link 2: Length = 0.425 m (upper arm)
  Link 3: Length = 0.39225 m (forearm)
  Link 4-5: Wrist offsets

""")

# Create enhanced 3D pattern examples
class Enhanced3DPatterns:
    """Enhanced patterns with true 3D variation"""
    
    def __init__(self, num_points=150):
        self.num_points = num_points
    
    def box_3d(self, size=0.3):
        """3D box/cube pattern - traces edges of a cube"""
        trajectory = []
        
        # Home position
        home = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
        
        # Generate cube pattern (8 corners + back to start)
        cube_steps = 8
        
        for step in range(self.num_points):
            # Determine which corner of the cube
            corner = int((step / self.num_points) * cube_steps)
            progress = (step / self.num_points) * cube_steps - corner
            
            # Define cube corners (scale in joint space)
            corners = [
                [0, 0, 0],           # corner 0
                [size, 0, 0],        # corner 1
                [size, size, 0],     # corner 2
                [0, size, 0],        # corner 3
                [0, 0, size],        # corner 4
                [size, 0, size],     # corner 5
                [size, size, size],  # corner 6
                [0, size, size],     # corner 7
            ]
            
            current_corner = corners[corner % 8]
            next_corner = corners[(corner + 1) % 8]
            
            # Interpolate between corners
            x = current_corner[0] + (next_corner[0] - current_corner[0]) * progress
            y = current_corner[1] + (next_corner[1] - current_corner[1]) * progress
            z = current_corner[2] + (next_corner[2] - current_corner[2]) * progress
            
            # Map to joint angles
            j1 = home[0] + x * 0.5
            j2 = home[1] + y * 0.3
            j3 = home[2] + z * 0.3  # Vertical variation
            j4 = home[3] + math.sin(step / self.num_points * 4 * math.pi) * 0.1
            j5 = home[4] + math.cos(step / self.num_points * 4 * math.pi) * 0.1
            j6 = home[5] + (step / self.num_points) * 0.3
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def lissajous_3d(self, freq_ratio=2, amplitude=0.3):
        """3D Lissajous curve - complex 3D pattern"""
        trajectory = []
        home = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
        
        for i in range(self.num_points):
            t = (i / self.num_points) * 2 * math.pi
            
            # Lissajous curve: different frequencies for X, Y, Z
            x = amplitude * math.sin(t)
            y = amplitude * math.sin(freq_ratio * t)
            z = amplitude * math.sin(3 * t) * 0.5
            
            j1 = home[0] + x * 0.5
            j2 = home[1] + y * 0.3
            j3 = home[2] + z * 0.3
            j4 = home[3] + math.sin(t * 2) * 0.1
            j5 = home[4] + math.cos(t * 3) * 0.1
            j6 = home[5] + t * 0.05
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def torus_3d(self, major_radius=0.3, minor_radius=0.1):
        """3D Torus (donut) pattern"""
        trajectory = []
        home = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
        
        for i in range(self.num_points):
            u = (i / self.num_points) * 2 * math.pi
            v = ((i % int(self.num_points / 3)) / int(self.num_points / 3)) * 2 * math.pi
            
            # Torus parametric equations
            x = (major_radius + minor_radius * math.cos(v)) * math.cos(u)
            y = (major_radius + minor_radius * math.cos(v)) * math.sin(u)
            z = minor_radius * math.sin(v)
            
            j1 = home[0] + x * 0.5
            j2 = home[1] + y * 0.3
            j3 = home[2] + z * 0.3
            j4 = home[3] + math.sin(u) * 0.1
            j5 = home[4] + math.cos(v) * 0.1
            j6 = home[5] + u * 0.1
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def helix_3d(self, radius=0.25, pitch=0.4, turns=3):
        """3D Helix spiral (improved spiral with more variation)"""
        trajectory = []
        home = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
        
        for i in range(self.num_points):
            t = (i / self.num_points) * turns * 2 * math.pi
            
            # Helix: circular motion + vertical progression
            x = radius * math.cos(t)
            y = radius * math.sin(t)
            z = (i / self.num_points) * pitch
            
            j1 = home[0] + x * 0.5
            j2 = home[1] + y * 0.3
            j3 = home[2] + z * 0.5  # More vertical range
            j4 = home[3] + math.sin(t) * 0.15
            j5 = home[4] + math.cos(t) * 0.15
            j6 = home[5] + t * 0.05
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def rose_curve_3d(self, petals=5, amplitude=0.3):
        """3D Rose curve (k-petaled flower pattern)"""
        trajectory = []
        home = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
        
        for i in range(self.num_points):
            t = (i / self.num_points) * 2 * math.pi
            
            # Rose curve: r = a * cos(k*t)
            r = amplitude * math.cos(petals * t)
            
            x = r * math.cos(t)
            y = r * math.sin(t)
            z = amplitude * math.sin(t) * 0.5
            
            j1 = home[0] + x * 0.5
            j2 = home[1] + y * 0.3
            j3 = home[2] + z * 0.3
            j4 = home[3] + math.sin(t * 2) * 0.1
            j5 = home[4] + math.cos(petals * t) * 0.1
            j6 = home[5] + t * 0.05
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory

# Generate and display 3D patterns
patterns_3d = Enhanced3DPatterns(num_points=150)

print("\nGENERATED 3D PATTERNS:")
print("-" * 70)

patterns = {
    '3D Box': patterns_3d.box_3d(size=0.2),
    '3D Lissajous': patterns_3d.lissajous_3d(freq_ratio=2),
    '3D Torus': patterns_3d.torus_3d(major_radius=0.25),
    '3D Helix': patterns_3d.helix_3d(radius=0.25, pitch=0.4),
    '3D Rose': patterns_3d.rose_curve_3d(petals=5),
}

for name, traj in patterns.items():
    j1_range = (min([a[0] for a in traj]), max([a[0] for a in traj]))
    j2_range = (min([a[1] for a in traj]), max([a[1] for a in traj]))
    j3_range = (min([a[2] for a in traj]), max([a[2] for a in traj]))
    
    print(f"\n{name}:")
    print(f"  Waypoints: {len(traj)}")
    print(f"  j1 (base) range: {j1_range[0]:.3f} to {j1_range[1]:.3f}")
    print(f"  j2 (shoulder) range: {j2_range[0]:.3f} to {j2_range[1]:.3f}")
    print(f"  j3 (elbow) range: {j3_range[0]:.3f} to {j3_range[1]:.3f}")
    print(f"  First waypoint: {[round(a, 4) for a in traj[0]]}")

print("\n" + "=" * 70)
print("HOW TO USE 3D PATTERNS")
print("=" * 70)

print("""
1. QUICK START - Use enhanced patterns in math_motion.py:

   Add this import to math_motion.py:
   from enhanced_3d_patterns import Enhanced3DPatterns

   Then add pattern generation:
   patterns_3d = Enhanced3DPatterns(num_points=200)
   trajectory = patterns_3d.box_3d(size=0.3)

2. CREATE CUSTOM 3D PATTERN:

   # Add to pattern_generator.py or create new class
   def my_custom_3d_pattern(self):
       trajectory = []
       home = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
       
       for i in range(self.num_points):
           t = (i / self.num_points) * 2 * math.pi
           
           # Define your 3D motion
           x = 0.3 * math.cos(t)
           y = 0.3 * math.sin(t)
           z = 0.2 * math.sin(2*t)  # Add vertical variation
           
           # Map to joint angles
           j1 = home[0] + x * 0.5
           j2 = home[1] + y * 0.3
           j3 = home[2] + z * 0.5  # Key: vary j3 for vertical
           j4 = home[3] + math.sin(t) * 0.1
           j5 = home[4] + math.cos(t) * 0.1
           j6 = home[5] + t * 0.05
           
           trajectory.append([j1, j2, j3, j4, j5, j6])
       
       return trajectory

3. KEY DIFFERENCES FROM 2D:

   2D Pattern:
   - j1, j2 vary (horizontal motion)
   - j3, j4, j5, j6 mostly constant
   - Motion in horizontal plane

   3D Pattern:
   - j1, j2, j3 all vary significantly
   - j4, j5, j6 add wrist orientation
   - Motion in all 3 dimensions (X, Y, Z)

4. WHEN TO USE EACH APPROACH:

   Use 2D patterns for:
   ✓ Painting/coating surfaces
   ✓ Grinding/polishing
   ✓ Linear assembly tasks
   ✓ Simple orbital motions

   Use 3D patterns for:
   ✓ Complex sculptural paths
   ✓ 3D inspection paths
   ✓ Multi-layer welding
   ✓ Creative demonstrations
""")
