"""
Real-time Pattern Visualization with PyBullet
==============================================

Visualizes UR10 robot performing attractor and geometric patterns
Shows all joints moving smoothly in 3D space
"""

import pybullet as p
import pybullet_data
import time
import math
from pattern_generator import PatternGenerator


class PatternVisualizer:
    """Visualize patterns in PyBullet"""
    
    def __init__(self, headless=False):
        """Initialize PyBullet connection"""
        if headless:
            self.client = p.connect(p.GUI, options="--width=1200 --height=800")
        else:
            self.client = p.connect(p.GUI)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        # Load plane
        p.loadURDF("plane.urdf")
        
        # Load UR10
        self.robot = p.loadURDF("ur_description/urdf/ur10.urdf", 
                                basePosition=[0, 0, 0],
                                baseOrientation=[0, 0, 0, 1],
                                useFixedBase=True)
        
        # Set camera for better view
        p.resetDebugVisualizerCamera(
            cameraDistance=2.0,
            cameraYaw=45,
            cameraPitch=-30,
            cameraTargetPosition=[0.3, 0, 0.5]
        )
        
        # Get joint info
        self.num_joints = p.getNumJoints(self.robot)
        self.joint_indices = list(range(self.num_joints))
        
        print(f"[+] UR10 loaded with {self.num_joints} joints")
    
    def set_joint_angles(self, angles):
        """Set robot joint angles"""
        for i, angle in enumerate(angles[:6]):  # First 6 joints only
            p.resetJointState(self.robot, i, angle)
    
    def visualize_pattern(self, trajectory, pattern_name, speed=0.02):
        """
        Visualize a trajectory in real-time
        
        Parameters:
        - trajectory: list of joint angle arrays
        - pattern_name: name of pattern for display
        - speed: visualization speed (seconds per waypoint)
        """
        print(f"\n[*] Visualizing {pattern_name.upper()} ({len(trajectory)} waypoints)")
        print("[>] Close PyBullet window to stop\n")
        
        # Add text overlay
        text_id = p.addUserDebugText(
            f"Pattern: {pattern_name}", 
            [0, 0, 1.5],
            textColorRGB=[1, 1, 1],
            textSize=2
        )
        
        waypoint_id = p.addUserDebugText(
            "", 
            [0, 0, 1.3],
            textColorRGB=[0.5, 1, 0.5],
            textSize=1.5
        )
        
        try:
            for i, angles in enumerate(trajectory):
                # Check if user closed window
                if not p.isConnected(self.client):
                    print("[!] Visualization stopped")
                    return
                
                # Update joint angles
                self.set_joint_angles(angles)
                
                # Update text overlay
                progress = int((i / len(trajectory)) * 100)
                p.removeUserDebugItem(waypoint_id)
                waypoint_id = p.addUserDebugText(
                    f"Waypoint: {i+1}/{len(trajectory)} ({progress}%)",
                    [0, 0, 1.3],
                    textColorRGB=[0.5, 1, 0.5],
                    textSize=1.5
                )
                
                # Step simulation
                p.stepSimulation()
                time.sleep(speed)
            
            print(f"[✓] Visualization complete!")
            print("[>] Window still open - you can inspect the final position")
            
            # Keep window open for inspection
            while p.isConnected(self.client):
                p.stepSimulation()
                time.sleep(0.01)
        
        except KeyboardInterrupt:
            print("\n[!] Visualization interrupted")
    
    def close(self):
        """Close PyBullet connection"""
        p.disconnect()


def main():
    print("=" * 70)
    print("UR10 PATTERN VISUALIZER - Real-time 3D Display")
    print("=" * 70)
    print("\nAvailable patterns:")
    print("  1. Infinity (3D Figure-8)")
    print("  2. Circle (Horizontal)")
    print("  3. Spiral (3D Helix)")
    print("  4. Wave (Sine Wave)")
    print("\nAttractor Patterns (all joints moving):")
    print("  5. Lorenz (Butterfly chaos)")
    print("  6. Rössler (Spiral chaos)")
    print("  7. Hénon (Folded chaos)")
    print()
    
    choice = input("Enter pattern (1-7) or name: ").strip().lower()
    
    pattern_map = {
        '1': ('infinity', 0.3),
        '2': ('circle', 0.3),
        '3': ('spiral', 0.3),
        '4': ('wave', 0.3),
        '5': ('lorenz', 0.3),
        '6': ('rossler', 0.3),
        '7': ('henon', 0.3),
    }
    
    if choice in pattern_map:
        pattern_name, _ = pattern_map[choice]
    else:
        pattern_name = choice
    
    # Get parameters
    try:
        num_points = int(input("Number of waypoints (default 300): ") or "300")
        speed = float(input("Speed (seconds per waypoint, default 0.02): ") or "0.02")
    except ValueError:
        num_points = 300
        speed = 0.02
    
    complexity = 1.0
    if pattern_name in ['lorenz', 'rossler', 'henon']:
        try:
            complexity = float(input("Complexity (default 1.0, 0.5-2.0): ") or "1.0")
        except ValueError:
            complexity = 1.0
    
    # Generate pattern
    print(f"\n[*] Generating {pattern_name.upper()} pattern...")
    generator = PatternGenerator(num_points=num_points)
    
    patterns = {
        'infinity': lambda: generator.infinity_3d(scale=0.3, speed=1.0),
        'circle': lambda: generator.circle_pattern(radius=0.3, plane='horizontal', speed=1.0),
        'spiral': lambda: generator.spiral_pattern(radius=0.3, height=0.4, speed=1.0),
        'wave': lambda: generator.wave_pattern(amplitude=0.3, wavelength=4, speed=1.0),
        'lorenz': lambda: generator.lorenz_attractor(scale=0.3, complexity=complexity),
        'rossler': lambda: generator.rossler_attractor(scale=0.3, complexity=complexity),
        'henon': lambda: generator.henon_attractor(scale=0.3, complexity=complexity),
    }
    
    if pattern_name not in patterns:
        print(f"[✗] Pattern '{pattern_name}' not found!")
        return
    
    trajectory = patterns[pattern_name]()
    print(f"[✓] Generated {len(trajectory)} waypoints")
    
    # Visualize
    print("\n[*] Starting visualization (close window to exit)...")
    visualizer = PatternVisualizer(headless=False)
    
    try:
        visualizer.visualize_pattern(trajectory, pattern_name, speed=speed)
    except Exception as e:
        print(f"[✗] Error during visualization: {e}")
    finally:
        visualizer.close()
        print("[+] Done!")


if __name__ == "__main__":
    main()
