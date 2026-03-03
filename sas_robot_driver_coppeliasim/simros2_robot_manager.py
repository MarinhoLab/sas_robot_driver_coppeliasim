from sas_common import rclcpp_Node
from sas_robot_driver import RobotDriverServer
import sys
import numpy as np

class SimROS2RobotManager:

    def __init__(self,
                 topic_prefix: str,
                 rclcpp_node: rclcpp_Node,
                 sim,
                 robot_base_handle: int = None,
                 joint_names: list[str] = None):

        if robot_base_handle is None and joint_names is None:
            raise Exception('You must specify a robot_base_handle or joint_names')
        if robot_base_handle is not None and joint_names is not None:
            raise Exception('You cannot specify a robot_base_handle or joint_names at the same time.')

        self.robot_base_handle = robot_base_handle
        self.topic_prefix = topic_prefix
        self.rclcpp_node = rclcpp_node
        self.coppeliasim_sim = sim

        if joint_names is None:
            self.joint_handles = sim.getObjectsInTree(self.robot_base_handle, sim.sceneobject_joint)
        else:
            raise Exception("Not implemented yet.")

        self.DOF = len(self.joint_handles)

        self.rds = RobotDriverServer(rclcpp_node, self.topic_prefix)
        self.q: np.array = np.zeros(self.DOF)
        self.q_min: np.array = np.zeros(self.DOF)
        self.q_max: np.array = np.zeros(self.DOF)
        self.q_dot: np.array = np.zeros(self.DOF)
        self.q_force: np.array = np.zeros(self.DOF)
        self.q_target: np.array = None

    def sensing_update(self):
        for i in range(self.DOF):
            self.q[i] = self.sim.getJointPosition(self.joint_handles[i])
            self.q_dot[i] = self.sim.getJointVelocity(self.joint_handles[i])
            self.q_force[i] = self.sim.getJointForce(self.joint_handles[i])

            cyclic, interval = self.sim.getJointInterval(self.joint_handles[i])
            if cyclic:
                self.q_min[i] = -sys.float_info.max
                self.q_max[i] = sys.float_info.max
            else:
                self.q_min[i] = interval[0]
                self.q_max[i] = interval[1]

        self.rds.send_joint_states(
            self.q,
            self.q_dot,
            self.q_force,
        )
        self.rds.send_joint_limits((self.q_min, self.q_max))

    def actuation_update(self):
        if self.rds.is_enaled():
            self.q_target = self.rds.get_target_joint_positions()
            if self.q_target is not None:
                for i in range(self.DOF):
                    self.sim.setJointTargetPosition(self.joint_handles[i], self.q_target[i])
