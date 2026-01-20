import math
import numpy as np

class PatternGenerator:
    """Generate joint angle trajectories for UR10 robot patterns"""
    
    def __init__(self, num_points=100):
        """
        Initialize pattern generator
        num_points: number of trajectory points to generate
        """
        self.num_points = num_points
        self.trajectory = []
    
    def infinity_3d(self, scale=0.3, speed=1.0):
        """
        Generate a 3D infinity (Lemniscate) pattern in joint space
        
        Parameters:
        - scale: size of the pattern (0.1 to 0.5 recommended)
        - speed: how fast to traverse the pattern (1.0 = normal)
        
        Returns:
        List of joint angle arrays [j1, j2, j3, j4, j5, j6]
        """
        trajectory = []
        
        # Home position (starting point)
        j1_center = 0.0      # Shoulder pan (rotating base)
        j2_center = -1.57    # Shoulder lift (raised)
        j3_center = 1.57     # Elbow (extended)
        j4_center = 0.0      # Wrist 1
        j5_center = 1.57     # Wrist 2
        j6_center = 0.0      # Wrist 3
        
        # Trace the infinity symbol in the horizontal plane with 3D variation
        # Using Lemniscate parametric equations
        for i in range(self.num_points):
            t = (i / self.num_points) * 2 * math.pi * speed
            
            # Lemniscate: parametric form
            # x(t) = a * cos(t) / (1 + sin²(t))
            # y(t) = a * cos(t) * sin(t) / (1 + sin²(t))
            a = scale
            denom = 1 + math.sin(t) ** 2
            x = a * math.cos(t) / denom if denom != 0 else 0
            y = a * math.cos(t) * math.sin(t) / denom if denom != 0 else 0
            z = a * math.sin(t * 2) * 0.4  # Enhanced 3D depth variation
            
            # Map the 2D pattern to joint angles
            # j1: rotate base (shoulder pan) with the pattern
            j1 = j1_center + x * 0.8  # More rotation for larger pattern
            
            # j2: move up/down based on Y (shoulder lift)
            j2 = j2_center + y * 0.5  # More variation
            
            # j3: extend/retract based on pattern (elbow) - more for 3D
            j3 = j3_center + z * 0.5 + (x + y) * 0.2  # Increased 3D variation
            
            # j4, j5, j6: add more wrist variation for true 3D orientation
            j4 = j4_center + math.sin(t * 2) * 0.15
            j5 = j5_center + math.cos(t * 2) * 0.15
            j6 = j6_center + t * 0.08  # More twist
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def circle_pattern(self, radius=0.3, plane='horizontal', speed=1.0):
        """
        Generate a circular pattern with enhanced 3D variation
        
        Parameters:
        - radius: size of circle (0.1 to 0.5)
        - plane: 'horizontal', 'vertical_xz', or 'vertical_yz'
        - speed: traverse speed
        """
        trajectory = []
        
        j1_center = 0.0
        j2_center = -1.57
        j3_center = 1.57
        j4_center = 0.0
        j5_center = 1.57
        j6_center = 0.0
        
        for i in range(self.num_points):
            t = (i / self.num_points) * 2 * math.pi * speed
            
            if plane == 'horizontal':
                # Circle in XY plane with vertical bobbing
                x = radius * math.cos(t)
                y = radius * math.sin(t)
                z = radius * 0.3 * math.sin(t * 2)  # Bobbing motion
            elif plane == 'vertical_xz':
                # Circle in XZ plane
                x = radius * math.cos(t)
                y = 0
                z = radius * math.sin(t)
            else:  # vertical_yz
                # Circle in YZ plane
                x = 0
                y = radius * math.cos(t)
                z = radius * math.sin(t)
            
            j1 = j1_center + x * 0.8  # More variation
            j2 = j2_center + y * 0.5 + z * 0.5  # More variation
            j3 = j3_center + (x + z) * 0.4  # Enhanced elbow variation
            j4 = j4_center + math.sin(t * 2) * 0.15
            j5 = j5_center + math.cos(t * 2) * 0.15
            j6 = j6_center + t * 0.08
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def wave_pattern(self, amplitude=0.3, wavelength=2, speed=1.0):
        """
        Generate a wave/sinusoidal pattern with enhanced 3D variation
        
        Parameters:
        - amplitude: height of wave
        - wavelength: number of complete waves
        - speed: traverse speed
        """
        trajectory = []
        
        j1_center = 0.0
        j2_center = -1.57
        j3_center = 1.57
        j4_center = 0.0
        j5_center = 1.57
        j6_center = 0.0
        
        for i in range(self.num_points):
            t = (i / self.num_points) * wavelength * 2 * math.pi * speed
            
            # X increases linearly, Y follows sine wave, Z adds vertical variation
            x = (i / self.num_points) * 0.8 - 0.4  # Larger traverse range
            y = amplitude * math.sin(t)
            z = amplitude * math.cos(t * 0.5) * 0.7  # More vertical variation
            
            j1 = j1_center + x * 0.5  # Side-to-side
            j2 = j2_center + y * 0.5  # Up-down oscillation
            j3 = j3_center + y * 0.4 + z * 0.4  # Enhanced vertical
            j4 = j4_center + math.sin(t) * 0.15
            j5 = j5_center + math.cos(t) * 0.15
            j6 = j6_center + t * 0.04
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def spiral_pattern(self, radius=0.3, height=0.4, speed=1.0):
        """
        Generate a spiral pattern (3D helix) with enhanced variation
        
        Parameters:
        - radius: radius of spiral
        - height: vertical distance traveled
        - speed: traverse speed
        """
        trajectory = []
        
        j1_center = 0.0
        j2_center = -1.57
        j3_center = 1.57
        j4_center = 0.0
        j5_center = 1.57
        j6_center = 0.0
        
        for i in range(self.num_points):
            t = (i / self.num_points) * 4 * math.pi * speed  # 2 full rotations
            
            # Helix parametric equations with enhanced variation
            x = radius * math.cos(t)
            y = radius * math.sin(t)
            z = (i / self.num_points) * height
            
            j1 = j1_center + x * 0.8  # More base rotation
            j2 = j2_center + y * 0.5  # More shoulder lift
            j3 = j3_center + z * 0.8 + (x * y * 0.3)  # Much more elbow variation
            j4 = j4_center + math.sin(t) * 0.15
            j5 = j5_center + math.cos(t) * 0.15
            j6 = j6_center + t * 0.08
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def print_trajectory(self, trajectory, label="Trajectory"):
        """Pretty print the trajectory"""
        print(f"\n{label}:")
        print(f"Total points: {len(trajectory)}")
        print("\nFirst 5 waypoints (angles in radians):")
        for i in range(min(5, len(trajectory))):
            angles = [round(a, 4) for a in trajectory[i]]
            print(f"  Point {i}: {angles}")
        print(f"\nLast waypoint:")
        angles = [round(a, 4) for a in trajectory[-1]]
        print(f"  Point {len(trajectory)-1}: {angles}")
    
    def export_to_urscript(self, trajectory, filename, acceleration=1.2, velocity=0.6):
        """
        Export trajectory as UR Script commands
        
        Parameters:
        - trajectory: list of joint angle arrays
        - filename: output file path
        - acceleration: acceleration parameter
        - velocity: velocity parameter
        """
        with open(filename, 'w') as f:
            f.write("# Auto-generated UR Script from pattern generator\n\n")
            f.write("def execute_pattern():\n")
            
            for i, angles in enumerate(trajectory):
                angles_str = str([round(a, 4) for a in angles])
                f.write(f"  movej({angles_str}, a={acceleration}, v={velocity})\n")
            
            f.write("end\n\n")
            f.write("execute_pattern()\n")
        
        print(f"Trajectory exported to {filename}")


    def lorenz_attractor(self, scale=0.3, complexity=1.0):
        """
        Lorenz Attractor - Butterfly pattern from chaos theory
        Creates a beautiful, complex curve with all joints moving
        
        Parameters:
        - scale: size of the pattern (0.1 to 0.5)
        - complexity: sensitivity parameter (higher = more intricate motion)
        
        Returns:
        List of joint angle arrays [j1, j2, j3, j4, j5, j6]
        """
        trajectory = []
        
        # Home position
        j1_center = 0.0
        j2_center = -1.57
        j3_center = 1.57
        j4_center = 0.0
        j5_center = 1.57
        j6_center = 0.0
        
        # Lorenz attractor parameters (classic butterfly)
        sigma = 10.0
        rho = 28.0 * complexity  # Adjust for complexity
        beta = 8.0 / 3.0
        
        # Integrate Lorenz equations using Euler method
        x, y, z = 1.0, 1.0, 1.0
        dt = 0.01
        
        for i in range(self.num_points):
            # Lorenz differential equations
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            
            # Update position
            x += dx * dt
            y += dy * dt
            z += dz * dt
            
            # Normalize to prevent explosion
            magnitude = math.sqrt(x**2 + y**2 + z**2)
            if magnitude > 0:
                x = (x / magnitude) * scale * 10
                y = (y / magnitude) * scale * 10
                z = (z / magnitude) * scale * 10
            
            # Map to joint angles - all joints move based on attractor
            j1 = j1_center + x * 0.5      # Primary oscillation
            j2 = j2_center + y * 0.4      # Secondary oscillation
            j3 = j3_center + z * 0.3      # Tertiary oscillation
            j4 = j4_center + x * 0.2      # Wrist coupling
            j5 = j5_center + y * 0.2      # Wrist coupling
            j6 = j6_center + z * 0.2      # Wrist coupling
            
            # Safety clamps
            j1 = max(-3.14, min(3.14, j1))
            j2 = max(-3.14, min(3.14, j2))
            j3 = max(0.5, min(2.5, j3))
            j4 = max(-3.14, min(3.14, j4))
            j5 = max(-3.14, min(3.14, j5))
            j6 = max(-3.14, min(3.14, j6))
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def rossler_attractor(self, scale=0.3, complexity=1.0):
        """
        Rössler Attractor - Spiral chaos pattern
        Creates smooth, spiral-like complex motion
        
        Parameters:
        - scale: size of pattern (0.2 to 0.5)
        - complexity: sensitivity parameter (0.5 to 2.0)
        
        Returns:
        List of joint angle arrays [j1, j2, j3, j4, j5, j6]
        """
        trajectory = []
        
        j1_center = 0.0
        j2_center = -1.57
        j3_center = 1.57
        j4_center = 0.0
        j5_center = 1.57
        j6_center = 0.0
        
        # Rössler parameters
        a = 0.1
        b = 0.1
        c = 14.0 * complexity
        
        x, y, z = 1.0, 0.0, 0.0
        dt = 0.01
        
        for i in range(self.num_points):
            # Rössler differential equations
            dx = -y - z
            dy = x + a * y
            dz = b + z * (x - c)
            
            x += dx * dt
            y += dy * dt
            z += dz * dt
            
            # Normalize
            magnitude = math.sqrt(x**2 + y**2 + z**2)
            if magnitude > 0:
                x = (x / magnitude) * scale * 8
                y = (y / magnitude) * scale * 8
                z = (z / magnitude) * scale * 8
            
            # Map to joints - smooth spiraling motion
            j1 = j1_center + x * 0.6
            j2 = j2_center + y * 0.5
            j3 = j3_center + z * 0.35
            j4 = j4_center + math.sin(i / 10) * 0.3
            j5 = j5_center + math.cos(i / 10) * 0.3
            j6 = j6_center + z * 0.2
            
            j1 = max(-3.14, min(3.14, j1))
            j2 = max(-3.14, min(3.14, j2))
            j3 = max(0.5, min(2.5, j3))
            j4 = max(-3.14, min(3.14, j4))
            j5 = max(-3.14, min(3.14, j5))
            j6 = max(-3.14, min(3.14, j6))
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory
    
    def henon_attractor(self, scale=0.3, complexity=1.2):
        """
        Hénon Attractor - 2D chaotic map extended to 3D
        Creates intricate, folded patterns
        
        Parameters:
        - scale: size (0.2 to 0.4)
        - complexity: fold intensity (1.0 to 2.0)
        
        Returns:
        List of joint angle arrays
        """
        trajectory = []
        
        j1_center = 0.0
        j2_center = -1.57
        j3_center = 1.57
        j4_center = 0.0
        j5_center = 1.57
        j6_center = 0.0
        
        # Hénon parameters
        a = 1.4 * complexity
        b = 0.3
        
        x, y, z = 0.0, 0.0, 0.0
        
        for i in range(self.num_points):
            # Hénon map (extended to 3D)
            x_new = 1 - a * x**2 + y
            y_new = b * x
            z_new = (x_new + y_new) * 0.5
            
            x, y, z = x_new, y_new, z_new
            
            # Normalize
            x = max(-1, min(1, x)) * scale
            y = max(-1, min(1, y)) * scale
            z = max(-1, min(1, z)) * scale
            
            # Map to all joints for complex, synchronized motion
            j1 = j1_center + x * 0.7
            j2 = j2_center + y * 0.5
            j3 = j3_center + z * 0.4
            j4 = j4_center + (x * y) * 0.3
            j5 = j5_center + (y * z) * 0.3
            j6 = j6_center + (z * x) * 0.3
            
            j1 = max(-3.14, min(3.14, j1))
            j2 = max(-3.14, min(3.14, j2))
            j3 = max(0.5, min(2.5, j3))
            j4 = max(-3.14, min(3.14, j4))
            j5 = max(-3.14, min(3.14, j5))
            j6 = max(-3.14, min(3.14, j6))
            
            trajectory.append([j1, j2, j3, j4, j5, j6])
        
        return trajectory


if __name__ == "__main__":
    # Example usage
    generator = PatternGenerator(num_points=150)
    
    # Generate 3D infinity pattern
    infinity = generator.infinity_3d(scale=0.3, speed=1.0)
    generator.print_trajectory(infinity, "3D Infinity Pattern")
    generator.export_to_urscript(infinity, "infinity_pattern.script")
    
    # Generate circular pattern
    circle = generator.circle_pattern(radius=0.3, plane='horizontal', speed=1.0)
    generator.print_trajectory(circle, "Circular Pattern (Horizontal)")
    generator.export_to_urscript(circle, "circle_pattern.script")
    
    # Generate spiral pattern
    spiral = generator.spiral_pattern(radius=0.3, height=0.4, speed=1.0)
    generator.print_trajectory(spiral, "Spiral Pattern")
    generator.export_to_urscript(spiral, "spiral_pattern.script")
    
    # Generate wave pattern
    wave = generator.wave_pattern(amplitude=0.3, wavelength=3, speed=1.0)
    generator.print_trajectory(wave, "Wave Pattern")
    generator.export_to_urscript(wave, "wave_pattern.script")
