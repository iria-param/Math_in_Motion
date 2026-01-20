from rtde_receive import RTDEReceiveInterface

# Replace with the actual IP address shown on your UR10 Teach Pendant
robot_ip = "192.168.1.20" 

try:
    rtde_r = RTDEReceiveInterface(robot_ip)
    # Get the current joint positions
    actual_q = rtde_r.getActualQ()
    print(f"Connection Successful!")
    print(f"Current Joint Positions (Radians): {actual_q}")
except Exception as e:
    print(f"Could not connect to the robot: {e}")
    print("Check if your laptop is on the same network/subnet as the UR10.")