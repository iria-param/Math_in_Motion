import pybullet as p
import pybullet_data
import time
import os
from pattern_generator import PatternGenerator

# Initialize PyBullet
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load UR10 Model
ur10_urdf_path = os.path.join(os.path.dirname(__file__), "ur_description", "urdf", "ur10.urdf")
robot_id = p.loadURDF(ur10_urdf_path, [0, 0, 0], useFixedBase=True)

print("=" * 60)
print("UR10 PATTERN SIMULATOR")
print("=" * 60)
print("\nSelect a pattern to run:")
print("  1. Infinity (3D Figure-8)")
print("  2. Circle (Horizontal)")
print("  3. Spiral (3D Helix)")
print("  4. Wave (Sine Wave)")
print("  5. Exit")
print()

choice = input("Enter choice (1-5): ").strip()

# Generate pattern based on choice
generator = PatternGenerator(num_points=100)

patterns = {
    '1': ("Infinity Pattern", generator.infinity_3d(scale=0.4, speed=1.0)),
    '2': ("Circle Pattern", generator.circle_pattern(radius=0.4, plane='horizontal', speed=1.0)),
    '3': ("Spiral Pattern", generator.spiral_pattern(radius=0.3, height=0.5, speed=1.0)),
    '4': ("Wave Pattern", generator.wave_pattern(amplitude=0.4, wavelength=4, speed=1.0)),
}

if choice not in patterns:
    print("Invalid choice. Exiting.")
    p.disconnect()
    exit()

pattern_name, trajectory = patterns[choice]

print(f"\n--- Executing: {pattern_name} ---")
print(f"Total waypoints: {len(trajectory)}")
print("Running simulation... (Close window to stop)\n")

try:
    # Add sliders for speed control
    speed_slider = p.addUserDebugParameter("Speed", 0.1, 3.0, 1.0)
    pause_slider = p.addUserDebugParameter("Pause", 0, 1, 0)
    
    waypoint_idx = 0
    paused = False
    
    while True:
        # Read slider values
        speed = p.readUserDebugParameter(speed_slider)
        pause_state = p.readUserDebugParameter(pause_slider)
        
        # Check if paused
        if pause_state > 0.5 and not paused:
            paused = True
            print(f"[PAUSED] at waypoint {waypoint_idx}")
        elif pause_state < 0.5 and paused:
            paused = False
            print(f"[RESUMED] from waypoint {waypoint_idx}")
        
        # If not paused, move to next waypoint
        if not paused:
            angles = trajectory[waypoint_idx % len(trajectory)]
            
            # Apply joint angles to robot
            for i in range(6):
                p.setJointMotorControl2(robot_id, i, p.POSITION_CONTROL, angles[i])
            
            # Print current waypoint every 10 points
            if waypoint_idx % 10 == 0:
                angles_rounded = [round(a, 4) for a in angles]
                print(f"Waypoint {waypoint_idx}: {angles_rounded}")
            
            waypoint_idx += 1
        
        p.stepSimulation()
        
        # Control speed via slider
        sleep_time = 0.01 / speed
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\n[STOPPED] by user")
    p.disconnect()
