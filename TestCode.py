"""
Math Motion Module for UR10 Robot
Author: Rajath Singh
Date: Jan 2026
Purpose: Generate and control mathematical motion patterns for UR10 robot arm
"""

import socket
import time
import numpy as np
from pattern_generator import PatternGenerator


# ==========================
# ROBOT CONFIG
# ==========================

ROBOT_IP = "192.168.1.20"   # <-- CHANGE IF NEEDED
PORT = 30002


# ==========================
# BATMAN PATTERN (NEW)
# ==========================

def batman_pattern(num_points=600):
    """
    Batman parametric equation mapped to joint space
    Returns list of [j1..j6]
    """

    t = np.linspace(-7, 7, num_points)
    trajectory = []

    # UR10 neutral posture
    j1_c = 0.0
    j2_c = -1.57
    j3_c = 1.57

    for ti in t:
        x = 0.5 * (
            np.exp(np.abs(ti)) * np.cos(ti)
            - 2 * np.cos(4 * ti)
            - np.sin(ti / 12)**5
        )

        y = 0.5 * (
            np.exp(np.abs(ti)) * np.sin(ti)
            - 2 * np.sin(4 * ti)
        )

        j1 = j1_c + x * 0.08
        j2 = j2_c + y * 0.06
        j3 = j3_c + 0.04 * np.sin(0.5 * ti)

        trajectory.append([
            round(j1, 4),
            round(j2, 4),
            round(j3, 4),
            0.0, 0.0, 0.0
        ])

    return trajectory


# ==========================
# URSCRIPT GENERATOR
# ==========================

def generate_pattern_script(
    pattern_name,
    num_points=200,
    acceleration=1.2,
    velocity=0.6,
    complexity=1.0
):
    """
    Generate URScript from selected pattern
    """

    generator = PatternGenerator(num_points=num_points)

    # Lazy pattern registry (important)
    pattern_registry = {
        "infinity": lambda: generator.infinity_3d(scale=0.3, speed=1.0),
        "circle": lambda: generator.circle_pattern(radius=0.3, plane="horizontal", speed=1.0),
        "spiral": lambda: generator.spiral_pattern(radius=0.3, height=0.4, speed=1.0),
        "wave": lambda: generator.wave_pattern(amplitude=0.3, wavelength=4, speed=1.0),
        "lorenz": lambda: generator.lorenz_attractor(scale=0.3, complexity=complexity),
        "rossler": lambda: generator.rossler_attractor(scale=0.3, complexity=complexity),
        "henon": lambda: generator.henon_attractor(scale=0.3, complexity=complexity),
        "batman": lambda: batman_pattern(num_points),
    }

    pattern_name = pattern_name.lower()

    if pattern_name not in pattern_registry:
        raise ValueError(f"Unknown pattern: {pattern_name}")

    trajectory = pattern_registry[pattern_name]()

    # Build URScript
    script = f"""
# Auto-generated URScript
# Pattern: {pattern_name.upper()}
def execute_{pattern_name}_pattern():
  a = {acceleration}
  v = {velocity}
  r = 0.05

"""

    for angles in trajectory:
        script += f"  movej({angles}, a=a, v=v, r=r)\n"

    script += f"""
end

execute_{pattern_name}_pattern()
"""

    return script


# ==========================
# SEND SCRIPT TO ROBOT
# ==========================

def send_urscript(script, pattern_name="pattern"):
    """
    Send URScript to UR10 via port 30002
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ROBOT_IP, PORT))
        print(f"[+] Connected to UR10 at {ROBOT_IP}:{PORT}")

        sock.sendall(script.encode("utf-8"))
        print(f"[>] Executing {pattern_name.upper()} pattern")

        time.sleep(15)
        sock.close()
        print("[✓] Execution complete, connection closed")

    except Exception as e:
        print(f"[✗] ERROR: {e}")


# ==========================
# MAIN CLI
# ==========================

if __name__ == "__main__":

    print("=" * 60)
    print("UR10 MATHEMATICAL MOTION EXECUTOR")
    print("=" * 60)

    print("\nAvailable Patterns:")
    print("  1. Infinity")
    print("  2. Circle")
    print("  3. Spiral")
    print("  4. Wave")
    print("  5. Lorenz Attractor")
    print("  6. Rossler Attractor")
    print("  7. Henon Attractor")
    print("  8. Batman (NEW)")
    print()

    pattern_map = {
        "1": "infinity",
        "2": "circle",
        "3": "spiral",
        "4": "wave",
        "5": "lorenz",
        "6": "rossler",
        "7": "henon",
        "8": "batman",
    }

    choice = input("Select pattern (1–8 or name): ").strip().lower()
    pattern = pattern_map.get(choice, choice)

    try:
        num_points = int(input("Waypoints (default 200): ") or "200")
        acceleration = float(input("Acceleration (default 1.2): ") or "1.2")
        velocity = float(input("Velocity (default 0.6): ") or "0.6")
    except ValueError:
        num_points = 200
        acceleration = 1.2
        velocity = 0.6

    complexity = 1.0
    if pattern in ["lorenz", "rossler", "henon"]:
        complexity = float(input("Complexity (0.5–2.0, default 1.0): ") or "1.0")

    print(f"\n[*] Generating {pattern.upper()} pattern...")
    urscript = generate_pattern_script(
        pattern,
        num_points=num_points,
        acceleration=acceleration,
        velocity=velocity,
        complexity=complexity
    )

    confirm = input("Send to robot? (yes/no): ").strip().lower()
    if confirm == 'yes':
            send_urscript(urscript, pattern)
    else:
        print("Cancelled.")
        print("\nHere's the generated script:")
        print("=" * 60)
        print(urscript[:500] + "..." if len(urscript) > 500 else urscript)
