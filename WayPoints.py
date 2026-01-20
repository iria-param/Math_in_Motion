import pybullet as p
import pybullet_data
import time
import math
import os

# 1. Initialize Simulator
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# 2. Load UR10 Model
ur10_urdf_path = os.path.join(os.path.dirname(__file__), "ur_description", "urdf", "ur10.urdf")
robot_id = p.loadURDF(ur10_urdf_path, [0, 0, 0], useFixedBase=True)
num_joints = p.getNumJoints(robot_id)

# Print joint info for debugging
print(f"Total links: {num_joints}")
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    print(f"Link {i}: {info[12].decode()}")

# End effector is the last movable joint
end_effector_idx = 5  # wrist_3_link (6th joint/link)

# 3. Create Sliders for X, Y, Z (Target TCP)
target_x = p.addUserDebugParameter("TCP X", -1, 1, 0.5)
target_y = p.addUserDebugParameter("TCP Y", -1, 1, 0.0)
target_z = p.addUserDebugParameter("TCP Z", 0, 1.5, 0.5)

print("\n--- SIMULATOR READY ---")
print("Move the sliders in the GUI. Copy the angles below:")

try:
    while True:
        # Get Slider Values
        x = p.readUserDebugParameter(target_x)
        y = p.readUserDebugParameter(target_y)
        z = p.readUserDebugParameter(target_z)

        # Calculate Inverse Kinematics (The Math)
        # Use wrist_3_link (index 5) as end effector
        joint_angles = p.calculateInverseKinematics(robot_id, end_effector_idx, [x, y, z])

        # Apply angles to the virtual robot (only the 6 movable joints)
        for i in range(6):
            p.setJointMotorControl2(robot_id, i, p.POSITION_CONTROL, joint_angles[i])

        # Format for your VS Code script
        clean_angles = [round(a, 4) for a in joint_angles[:6]]
        print(f"COPY THIS: movej({clean_angles}, a=1.2, v=0.6)", end="\r")

        p.stepSimulation()
        time.sleep(0.01)

except KeyboardInterrupt:
    p.disconnect()