"""
# Copyright (c) 2026 Murilo Marques Marinho
#
#    This file is part of sas_robot_driver_coppeliasim.
#
#    sas_robot_driver_coppeliasim is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sas_robot_driver_coppeliasim is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sas_robot_driver_coppeliasim.  If not, see <https://www.gnu.org/licenses/>.
#
# #######################################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#
# #######################################################################################
"""
import sys

import numpy as np

from sas_common import rclcpp_Node
from sas_robot_driver import Functionality, RobotDriverServer


class SimROS2RobotManager:
    """Publishes joint states and applies joint commands for a CoppeliaSim robot."""

    def __init__(self,
                 topic_prefix: str,
                 rclcpp_node: rclcpp_Node,
                 sim,
                 robot_base_handle: int | None = None,
                 joint_names: list[str] | None = None):
        """
        Either ``robot_base_handle`` or ``joint_names`` must be provided, but not both.

        :param topic_prefix: ROS 2 topic prefix for this robot's driver server.
        :param rclcpp_node: C++ rclcpp node used by the RobotDriverServer.
        :param sim: CoppeliaSim simulation object provided by the simulator.
        :param robot_base_handle: CoppeliaSim handle of the robot base object.
                                  All joints in the subtree are used automatically.
        :param joint_names: Explicit list of joint names (not yet implemented).
        """
        if robot_base_handle is None and joint_names is None:
            raise Exception('You must specify a robot_base_handle or joint_names')
        if robot_base_handle is not None and joint_names is not None:
            raise Exception('You cannot specify a robot_base_handle or joint_names at the same time.')

        self.robot_base_handle = robot_base_handle
        self.topic_prefix = topic_prefix
        self.rclcpp_node = rclcpp_node
        self.sim = sim

        if joint_names is None:
            # sim.sceneobject_joint is not available in CoppeliaSim 4.7, which uses sim.object_joint_type.
            joint_type = getattr(sim, 'sceneobject_joint', None)
            if joint_type is None:
                joint_type = sim.object_joint_type
            self.joint_handles = sim.getObjectsInTree(self.robot_base_handle, joint_type)
        else:
            raise Exception("Not implemented yet.")

        self.DOF = len(self.joint_handles)

        self.rds = RobotDriverServer(rclcpp_node, f"/sas_robot_driver_coppeliasim{self.topic_prefix}")
        self.q: np.ndarray = np.zeros(self.DOF)        # Current joint positions (rad).
        self.q_min: np.ndarray = np.zeros(self.DOF)    # Joint position lower limits (rad).
        self.q_max: np.ndarray = np.zeros(self.DOF)    # Joint position upper limits (rad).
        self.q_dot: np.ndarray = np.zeros(self.DOF)    # Current joint velocities (rad/s).
        self.q_force: np.ndarray = np.zeros(self.DOF)  # Current joint forces/torques (N·m).
        self.q_target: np.ndarray | None = None               # Target joint positions received from the driver server.
        self.q_dot_target: np.ndarray | None = None           # Target joint velocities received from the driver server.
        self._dynamic_control_mode = None            # Current sim.jointdynctrl_* mode of the dynamic joints.

    def sensing_update(self):
        """Reads joint states from the simulator and publishes them via the driver server."""
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
        """Applies the latest joint targets from the driver server to the simulator.

        The last type of target received selects the control mode: target joint positions use
        position control and target joint velocities use velocity control. Velocity targets
        persist until a new target is received, so send zeros or a position target to stop.
        """
        active = self.rds.get_currently_active_functionality()
        if active == Functionality.PositionControl:
            self.q_target = self.rds.get_target_joint_positions()
            if self.q_target is not None and len(self.q_target) == self.DOF:
                self._set_dynamic_control_mode(self.sim.jointdynctrl_position)
                for i in range(self.DOF):
                    self.sim.setJointTargetPosition(self.joint_handles[i], self.q_target[i])
        elif active == Functionality.VelocityControl:
            self.q_dot_target = self.rds.get_target_joint_velocities()
            if self.q_dot_target is None or len(self.q_dot_target) != self.DOF:
                self.q_dot_target = np.zeros(self.DOF)  # Malformed command: stop the robot.
            self._set_dynamic_control_mode(self.sim.jointdynctrl_velocity)
            for i in range(self.DOF):
                self.sim.setJointTargetVelocity(self.joint_handles[i], self.q_dot_target[i])

    def _set_dynamic_control_mode(self, mode):
        """Switches the dynamically enabled joints between position and velocity control."""
        if mode == self._dynamic_control_mode:
            return
        for handle in self.joint_handles:
            if self.sim.getJointMode(handle)[0] != self.sim.jointmode_dynamic:
                continue
            self.sim.setObjectInt32Param(handle, self.sim.jointintparam_dynctrlmode, mode)
            if mode == self.sim.jointdynctrl_velocity:
                # Lock joints with zero target velocity so that they do not drift under gravity.
                self.sim.setObjectInt32Param(handle, self.sim.jointintparam_velocity_lock, 1)
        self._dynamic_control_mode = mode
