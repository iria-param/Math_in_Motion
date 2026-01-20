"""
HOME POSITION DEFINITION FOR UR10 COBOT

The "home" or center position is defined in pattern_generator.py for each pattern.
All patterns oscillate around this center position.
"""

import math

print("=" * 70)
print("UR10 HOME POSITION DEFINITION")
print("=" * 70)

print("""
CURRENT HOME POSITION (in pattern_generator.py):
-------------------------------------------------
j1_center = 0.0      # Shoulder Pan (Base rotation)
j2_center = -1.57    # Shoulder Lift (Up/Down) 
j3_center = 1.57     # Elbow (Extend/Retract)
j4_center = 0.0      # Wrist 1
j5_center = 1.57     # Wrist 2
j6_center = 0.0      # Wrist 3

WHAT THESE VALUES MEAN:
-----------------------
""")

# Convert radians to degrees for clarity
j1_deg = math.degrees(0.0)
j2_deg = math.degrees(-1.57)
j3_deg = math.degrees(1.57)
j4_deg = math.degrees(0.0)
j5_deg = math.degrees(1.57)
j6_deg = math.degrees(0.0)

print(f"j1 = 0.0 rad = {j1_deg:.1f}° | Shoulder Pan: Facing FORWARD")
print(f"j2 = -1.57 rad = {j2_deg:.1f}° | Shoulder Lift: ARM RAISED (90° up)")
print(f"j3 = 1.57 rad = {j3_deg:.1f}° | Elbow: EXTENDED (90° bend)")
print(f"j4 = 0.0 rad = {j4_deg:.1f}° | Wrist 1: NEUTRAL")
print(f"j5 = 1.57 rad = {j5_deg:.1f}° | Wrist 2: UPRIGHT")
print(f"j6 = 0.0 rad = {j6_deg:.1f}° | Wrist 3: NEUTRAL")
  
print("""

WHAT IS HOME POSITION:
----------------------
The home position is the CENTER point around which the pattern oscillates.
For example, in the infinity pattern:

  Pattern point = home + (variation * scale)
  
  j1_actual = j1_center + x * 0.5
  j2_actual = j2_center + y * 0.3
  j3_actual = j3_center + (x + y) * 0.2
  
The robot will move AROUND this home position, not FROM it.

COMMON UR10 HOME POSITIONS:
---------------------------
""")

home_positions = {
    "Current (Raised Arm)": [0.0, -1.57, 1.57, 0.0, 1.57, 0.0],
    "Zero Position": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "Safe Home (Folded)": [0.0, -1.57, -1.57, 0.0, 1.57, 0.0],
    "Ready Position": [0.0, -1.57, 0.0, 0.0, 1.57, 0.0],
    "Upright Arm": [0.0, -3.14, 1.57, 0.0, 1.57, 0.0],
}

for name, angles in home_positions.items():
    degrees = [f"{math.degrees(a):.1f}°" for a in angles]
    print(f"\n{name}:")
    print(f"  Radians: {[round(a, 2) for a in angles]}")
    print(f"  Degrees: {degrees}")

print("""

HOW TO CHANGE HOME POSITION:
----------------------------
1. Open pattern_generator.py
2. Find the pattern method (e.g., infinity_3d)
3. Change the j1_center, j2_center, etc. values
4. Save and re-run

Example: To move the home position lower:
  Change: j2_center = -1.57    # Currently raised
  To:     j2_center = -2.0     # Lower position
  
The pattern will now execute from a lower starting height.

PRACTICAL TIPS:
---------------
✓ Home position should be SAFE and accessible
✓ Avoid home positions near joint limits (±2π radians)
✓ Use the robot's actual home position as reference:
  - Check the "Move" tab on UR10 pendant
  - Note the current joint angles
  - Use those as j*_center values

CHECKING YOUR ROBOT'S HOME:
--------------------------
1. On UR10 Teaching Pendant:
   - Go to "Move" tab
   - Press "Jog" mode
   - Read the current joint angles (j0-j5)
   - These are your current home position

2. Example output from pendant:
   j0: 0.04    (base)
   j1: -1.55   (shoulder)
   j2: 1.58    (elbow)
   j3: -0.03   (wrist 1)
   j4: 1.57    (wrist 2)
   j5: -0.01   (wrist 3)

3. Copy these values to pattern_generator.py:
   j1_center = 0.04
   j2_center = -1.55
   j3_center = 1.58
   j4_center = -0.03
   j5_center = 1.57
   j6_center = -0.01

WHY IT MATTERS:
---------------
- Home position determines WHERE in workspace the pattern executes
- Wrong home = pattern may hit obstacles or exceed joint limits
- Good home = smooth, safe pattern execution
""")

print("\n" + "=" * 70)
print("CURRENT HOME POSITION IN YOUR PATTERNS")
print("=" * 70)

from pattern_generator import PatternGenerator

generator = PatternGenerator(num_points=10)

# Get first waypoint of each pattern (shows home + initial offset)
patterns = {
    'Infinity': generator.infinity_3d(),
    'Circle': generator.circle_pattern(),
    'Spiral': generator.spiral_pattern(),
    'Wave': generator.wave_pattern(),
}

for name, trajectory in patterns.items():
    first = trajectory[0]
    home = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]
    offset = [round(first[i] - home[i], 4) for i in range(6)]
    
    print(f"\n{name}:")
    print(f"  First waypoint: {[round(a, 4) for a in first]}")
    print(f"  Home position: {home}")
    print(f"  Offset (variation from home): {offset}")
