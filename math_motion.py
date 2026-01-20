"""
Math Motion Module for UR10 Robot
Author: Rajath Singh
Date: Jan 2026
Purpose: Generate and control mathematical motion patterns for UR10 robot arm
"""

import socket
import time
from pattern_generator import PatternGenerator


ROBOT_IP = "192.168.1.20"  # Replace with your UR10 IP
PORT = 30002


def generate_pattern_script(pattern_name, num_points=100, acceleration=1.2, velocity=0.6, complexity=1.0):
    """Generate UR Script from pattern"""
    generator = PatternGenerator(num_points=num_points)
    
    # Generate pattern based on choice
    patterns = {
        'infinity': generator.infinity_3d(scale=0.3, speed=1.0),
        'circle': generator.circle_pattern(radius=0.3, plane='horizontal', speed=1.0),
        'spiral': generator.spiral_pattern(radius=0.3, height=0.4, speed=1.0),
        'wave': generator.wave_pattern(amplitude=0.3, wavelength=4, speed=1.0),
        'heart': generator.heart_pattern(scale=0.25, speed=1.0),
        'lorenz': generator.lorenz_attractor(scale=0.3, complexity=complexity),
        'rossler': generator.rossler_attractor(scale=0.3, complexity=complexity),
        'henon': generator.henon_attractor(scale=0.3, complexity=complexity),
    }
    
    if pattern_name.lower() not in patterns:
        print(f"Pattern '{pattern_name}' not found. Available: infinity, circle, spiral, wave, lorenz, rossler, henon")
        return None
    
    trajectory = patterns[pattern_name.lower()]
    
    # Build URScript with path blending (r parameter prevents stops between moves)
    script = f"""
# Auto-generated UR Script - {pattern_name.upper()} Pattern
def execute_{pattern_name.lower()}_pattern():
  a = {acceleration}
  v = {velocity}
  r = 0.05
  
"""
    
    for i, angles in enumerate(trajectory):
        angles_str = str([round(a, 4) for a in angles])
        # Use r parameter for path blending - prevents stop at each waypoint
        script += f"  movej({angles_str}, a={acceleration}, v={velocity}, r={0.05})\n"
    
    script += """end

execute_""" + pattern_name.lower() + """_pattern()
"""
    
    return script


def send_urscript(script, pattern_name="Pattern"):
    """Send URScript to robot via port 30002"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ROBOT_IP, PORT))
        print(f"[+] Connected to UR10 at {ROBOT_IP}:{PORT}")
        
        s.send(script.encode("utf-8"))
        print(f"[>] Sent: {pattern_name} pattern to robot")
        
        # Wait for execution (adjust based on pattern length)
        time.sleep(15)
        s.close()
        print("[✓] Disconnected")
        
    except ConnectionRefusedError:
        print(f"[✗] ERROR: Could not connect to UR10 at {ROBOT_IP}:{PORT}")
        print("    Make sure the robot is running and the IP is correct")
    except Exception as e:
        print(f"[✗] ERROR: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("UR10 PATTERN EXECUTOR - WITH ATTRACTOR PATTERNS")
    print("=" * 60)
    print("\nAvailable patterns:")
    print("  1. Infinity (3D Figure-8)")
    print("  2. Circle (Horizontal)")
    print("  3. Spiral (3D Helix)")
    print("  4. Wave (Sine Wave)")
    print("  5. Heart (Love Shape)")
    print("\nAttractor Patterns (complex, all joints moving):")
    print("  6. Lorenz (Butterfly chaos - classic)")
    print("  7. Rössler (Spiral chaos)")
    print("  8. Hénon (Folded chaos)")
    print()
    
    choice = input("Enter pattern (1-8) or name: ").strip().lower()
    
    # Map numbers to pattern names
    pattern_map = {
        '1': 'infinity',
        '2': 'circle',
        '3': 'spiral',
        '4': 'wave',
        '5': 'heart',
        '6': 'lorenz',
        '7': 'rossler',
        '8': 'henon',
    }
    
    pattern = pattern_map.get(choice, choice)
    
    # Get parameters
    try:
        num_points = int(input("Number of waypoints (default 200 for smooth motion): ") or "200")
        acceleration = float(input("Acceleration (default 1.2): ") or "1.2")
        velocity = float(input("Velocity (default 0.8): ") or "0.8")
    except ValueError:
        num_points = 200
        acceleration = 1.2
        velocity = 0.8
    
    # For attractor patterns, ask for complexity
    complexity = 1.0
    if pattern in ['lorenz', 'rossler', 'henon']:
        try:
            complexity = float(input("Complexity (default 1.0, 0.5-2.0 recommended): ") or "1.0")
        except ValueError:
            complexity = 1.0
    
    print(f"\n[*] Generating {pattern.upper()} pattern...")
    urscript = generate_pattern_script(pattern, num_points=num_points, 
                                        acceleration=acceleration, velocity=velocity,
                                        complexity=complexity)
    
    if urscript:
        print(f"[*] Script generated ({num_points} waypoints)")
        print("\n[!] READY TO SEND TO ROBOT")
        confirm = input("Send to robot? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            send_urscript(urscript, pattern)
        else:
            print("Cancelled.")
            print("\nHere's the generated script:")
            print("=" * 60)
            print(urscript[:500] + "..." if len(urscript) > 500 else urscript)