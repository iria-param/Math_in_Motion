import pybullet as p
import os

# Load robot
physicsClient = p.connect(p.DIRECT)  # Use DIRECT mode for no GUI
ur10_urdf_path = os.path.join(os.path.dirname(__file__), "ur_description", "urdf", "ur10.urdf")
robot_id = p.loadURDF(ur10_urdf_path, [0, 0, 0], useFixedBase=True)
num_joints = p.getNumJoints(robot_id)

print(f'Total joints: {num_joints}\n')
print('Joint Info:')
for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    joint_name = info[1].decode()
    joint_type = info[2]
    link_name = info[12].decode()
    print(f'  Joint {i}: {joint_name} (Type: {joint_type}, Link: {link_name})')

print(f'\nEnd effector link should be at index: {num_joints - 1}')
p.disconnect()
