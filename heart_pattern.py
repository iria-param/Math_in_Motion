import numpy as np
import matplotlib.pyplot as plt
import math

class HeartPatternGenerator:
    """Generate a heart pattern for the UR10 robot"""
    
    def __init__(self, num_points=200):
        """
        Initialize heart pattern generator
        num_points: number of trajectory points
        """
        self.num_points = num_points
        self.trajectory = []
    
    def generate_heart_trajectory(self, scale=0.1, z_base=0.5):
        """
        Generate heart pattern waypoints for the robot
        
        Parameters:
        - scale: size of the heart (0.05 to 0.2 recommended)
        - z_base: base height for the end effector
        
        Returns:
        List of [x, y, z] waypoints
        """
        waypoints = []
        
        # Heart parametric equations
        for i in range(self.num_points):
            t = (i / self.num_points) * 2 * math.pi
            
            # Parametric heart equations (scaled down for robot workspace)
            x = scale * 16 * math.sin(t)**3
            y = scale * (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t))
            z = z_base  # Keep constant Z height (draw on a plane)
            
            waypoints.append([x, y, z])
        
        self.trajectory = waypoints
        return waypoints
    
    def get_trajectory(self):
        """Return the generated trajectory"""
        return self.trajectory
    
    def print_waypoints(self):
        """Print waypoints in a readable format"""
        print("Heart Pattern Waypoints for UR10:")
        print("=" * 50)
        for i, wp in enumerate(self.trajectory):
            print(f"Point {i}: X={wp[0]:.4f}, Y={wp[1]:.4f}, Z={wp[2]:.4f}")
    
    def save_to_file(self, filename="heart_waypoints.txt"):
        """Save waypoints to a file for robot programming"""
        with open(filename, 'w') as f:
            f.write("# Heart Pattern Waypoints for UR10\n")
            f.write("# Format: X, Y, Z (in meters)\n")
            f.write("# " + "="*50 + "\n")
            for i, wp in enumerate(self.trajectory):
                f.write(f"{wp[0]:.6f}, {wp[1]:.6f}, {wp[2]:.6f}\n")
        print(f"Waypoints saved to {filename}")

def plot_heart_pattern(waypoints):
    """Visualize the heart pattern"""
    waypoints = np.array(waypoints)
    
    plt.figure(figsize=(10, 8))
    plt.plot(waypoints[:, 0], waypoints[:, 1], 'r-', linewidth=2.5, label='Heart Path')
    plt.scatter(waypoints[0, 0], waypoints[0, 1], color='green', s=100, label='Start', zorder=5)
    plt.scatter(waypoints[-1, 0], waypoints[-1, 1], color='blue', s=100, label='End', zorder=5)
    
    plt.title('UR10 Robot - Heart Pattern Trajectory', fontsize=16, fontweight='bold')
    plt.xlabel('X (meters)', fontsize=12)
    plt.ylabel('Y (meters)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig('heart_pattern_trajectory.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"X range: [{waypoints[:, 0].min():.4f}, {waypoints[:, 0].max():.4f}]")
    print(f"Y range: [{waypoints[:, 1].min():.4f}, {waypoints[:, 1].max():.4f}]")
    print(f"Z height: {waypoints[0, 2]:.4f}")

if __name__ == "__main__":
    # Generate heart pattern
    heart_gen = HeartPatternGenerator(num_points=300)
    waypoints = heart_gen.generate_heart_trajectory(scale=0.12, z_base=0.5)
    
    # Print and save waypoints
    print(f"Generated {len(waypoints)} waypoints for heart pattern\n")
    heart_gen.print_waypoints()
    
    # Save to file for robot
    heart_gen.save_to_file("heart_waypoints.txt")
    
    # Visualize
    plot_heart_pattern(waypoints)
