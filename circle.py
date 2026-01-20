import math
from rtde_control import RTDEControlInterface
from rtde_receive import RTDEReceiveInterface

robot_ip = "192.168.1.20"

try:
    rtc = RTDEControlInterface(robot_ip)
    rtr = RTDEReceiveInterface(robot_ip)

    # 1. Get Start Position
    start_pose = rtr.getActualTCPPose()
    print(f"Starting at: {start_pose}")

    # Circle Parameters
    radius = 0.05   # 5cm radius
    steps = 40      # Number of points
    center_x = start_pose[0]
    center_z = start_pose[2]
    
    # 2. Create the PATH list
    path = []
    
    # Motion Settings for the Path
    # velocity (0.1 m/s), acceleration (0.2 m/s^2), blend (0.002 m = 2mm)
    # Note: Blend radius (0.002) must be small enough to fit between points!
    vel = 0.1
    acc = 0.2
    blend = 0.002 

    print("Calculating Path...")
    for i in range(steps):
        angle = (2 * math.pi * i) / steps
        
        # Calculate coordinate
        waypoint = list(start_pose)
        waypoint[0] = center_x + (radius * math.cos(angle))
        waypoint[2] = center_z + (radius * math.sin(angle))
        
        # KEY DIFFERENCE: Add the motion parameters to EACH point
        # Format: [x, y, z, rx, ry, rz, velocity, acceleration, blend_radius]
        waypoint.append(vel)
        waypoint.append(acc)
        waypoint.append(blend)
        
        # Add to our list
        path.append(waypoint)

    # Add the final point (Start point) to close the loop
    # We set blend=0 for the last point so the robot stops gracefully at the end.
    last_point = list(start_pose)
    last_point.append(vel)
    last_point.append(acc)
    last_point.append(0) 
    path.append(last_point)

    # 3. Send the WHOLE path in one shot
    print("Uploading full path to robot...")
    rtc.moveL(path)

    print("Path sent! Robot should move smoothly now.")
    rtc.stopScript()

except Exception as e:
    print(f"Error: {e}")