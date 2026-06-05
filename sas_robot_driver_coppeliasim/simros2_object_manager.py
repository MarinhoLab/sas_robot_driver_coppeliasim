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
from dqrobotics import *
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from sas_conversions import geometry_msgs_pose_stamped_to_dq, dq_to_geometry_msgs_pose_stamped

class SimROS2ObjectManager:
    """Publishes and receives poses for a CoppeliaSim scene object."""

    def __init__(self,
                 object_handle: int,
                 node: Node,
                 sim):
        """
        :param object_handle: CoppeliaSim handle of the scene object.
        :param node: rclpy Node used to create publishers and subscriptions.
        :param sim: CoppeliaSim simulation object provided by the simulator.
        """
        self.object_handle = object_handle
        self.object_alias = sim.getObjectAlias(object_handle, 1).replace("[", "_").replace("]", "_")
        self.sim = sim

        self.publisher = node.create_publisher(
            msg_type=PoseStamped,
            topic=f'/sas_robot_driver_coppeliasim/object{self.object_alias}/get/pose',
            qos_profile=1)

        self.subscriber = node.create_subscription(
            msg_type=PoseStamped,
            topic=f'/sas_robot_driver_coppeliasim/object{self.object_alias}/set/pose',
            callback=self.subscriber_callback,
            qos_profile=1)

        self.x = None  # Pending pose command as a unit dual quaternion, or None.

    def sensing_update(self):
        """Reads the object pose from the simulator and publishes it."""
        x_cs = self.sim.getObjectPose(self.object_handle)
        t = x_cs[0]*i_ + x_cs[1]*j_ + x_cs[2]*k_
        r = (x_cs[6] + x_cs[3]*i_ + x_cs[4]*j_ + x_cs[5]*k_).normalize()
        msg = dq_to_geometry_msgs_pose_stamped(r + 0.5*E_*t*r)
        self.publisher.publish(msg)

    def actuation_update(self):
        """Applies a pending pose command to the simulator, then clears it."""
        if self.x is not None:
            t = vec3(translation(self.x))
            r = vec4(rotation(self.x))
            x_cs = [t[0], t[1], t[2],
                    r[1], r[2], r[3], r[0]]
            self.sim.setObjectPose(self.object_handle, x_cs)
            self.x = None # 26.03.12 - Objects won't be manipulable in the interface otherwise, even those we want to update only once.

    def subscriber_callback(self, msg: PoseStamped):
        """Stores an incoming pose command for the next actuation step."""
        self.x = geometry_msgs_pose_stamped_to_dq(msg)


