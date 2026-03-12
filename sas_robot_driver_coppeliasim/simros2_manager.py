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
import time
import rclpy
from rclpy.node import Node
from sas_common import rclcpp_init, rclcpp_Node, rclcpp_spin_some, rclcpp_shutdown
from .simros2_node import SimROS2Node

class SimROS2Manager:
    def __init__(self, sim):
        self.node: Node = None
        self.rclcpp_node: rclcpp_Node = None
        self.coppeliasim_sim = sim

    def sys_call_init(self):
        try:
            if self.node is None:
                rclpy.init(args=None)
                rclcpp_init()
                timestamp_for_anonymous_name = str(time.time()).replace('.', '_')
                self.rclcpp_node = rclcpp_Node(f"sas_simros2_{timestamp_for_anonymous_name}_cpp_node")
                self.node = SimROS2Node(self.rclcpp_node, self.coppeliasim_sim)
                print("ROS 2 nodes initialized successfully")

        except Exception as e:
            print(f"Error initializing ROS 2: {e}")

    def sys_call_actuation(self):
        if self.node is not None:
            self.node.actuation_update()

    def sys_call_sensing(self):
        if self.node is not None:
            self.node.sensing_update()
            rclpy.spin_once(self.node, timeout_sec=0.0)
            rclcpp_spin_some(self.rclcpp_node)

    def sys_call_cleanup(self):
        if self.node is not None:
            self.node.destroy_node()
            rclpy.shutdown()
            rclcpp_shutdown()
            print("ROS 2 shutdown requested")