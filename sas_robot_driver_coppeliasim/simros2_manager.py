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
from rclpy.executors import ExternalShutdownException
from rclpy.utilities import ok

from sas_common import rclcpp_init, rclcpp_Node, rclcpp_shutdown, rclcpp_spin_some
from sas_robot_driver_coppeliasim.simros2_node import SimROS2Node


class SimROS2Manager:
    """Manages ROS 2 lifecycle within a CoppeliaSim simulation."""

    def __init__(self, sim=None):
        """
        :param sim: CoppeliaSim simulation object provided by the simulator.
        """
        self.node: SimROS2Node | None = None
        self.rclcpp_node: rclcpp_Node = None
        self.coppeliasim_sim = sim

    def sys_call_init(self):
        """Initializes rclpy, the C++ node, and the SimROS2Node."""
        try:
            if self.node is None:
                if not ok():
                    rclpy.init(args=None)
                rclcpp_init()
                timestamp_for_anonymous_name = str(time.time()).replace('.', '_')
                self.rclcpp_node = rclcpp_Node(f"sas_simros2_{timestamp_for_anonymous_name}_cpp_node")
                self.node = SimROS2Node(self.rclcpp_node, self.coppeliasim_sim)
                print("ROS 2 nodes initialized successfully")

        except Exception as e:
            print(f"Error initializing ROS 2: {e}")

    def sys_call_actuation(self):
        """Runs the actuation update step."""
        if self.node is not None:
            self.node.actuation_update()

    def sys_call_sensing(self):
        """Runs the sensing update step and spins both nodes once."""
        if self.node is not None:
            self.node.sensing_update()
            try:
                rclpy.spin_once(self.node, timeout_sec=0.0)
                rclcpp_spin_some(self.rclcpp_node)
            except (KeyboardInterrupt, ExternalShutdownException):
                pass
            except Exception as e:
                print(e)

    def sys_call_cleanup(self):
        """Releases the nodes and shuts down the C++ ROS 2 side."""
        if self.node is not None:
            # No destroy_node()/rclpy.shutdown(): rclpy shuts the context
            # down itself, and shutdown() would raise when Ctrl-C already
            # brought the context down. Dropping the references lets the GC
            # release the nodes, and clearing them lets sys_call_init
            # re-create them on the next simulation.
            self.node = None
            self.rclcpp_node = None
            rclcpp_shutdown()
            print("ROS 2 shutdown requested")
