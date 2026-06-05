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
from rclpy.node import Node

from sas_common import rclcpp_Node
from .simros2_robot_manager import SimROS2RobotManager
from .simros2_object_manager import SimROS2ObjectManager


class SimROS2Node(Node):
    """ROS 2 node coordinating robot and object managers."""

    def __init__(self,
                 rclcpp_node: rclcpp_Node,
                 sim
                 ):
        """
        :param rclcpp_node: Companion C++ rclcpp node.
        :param sim: CoppeliaSim simulation object provided by the simulator.
        """
        timestamp_for_anonymous_name = str(time.time()).replace('.', '_')
        super().__init__(f"sas_simros2_{timestamp_for_anonymous_name}_python_node")
        self.rclcpp_node: rclcpp_Node = rclcpp_node
        self.robot_managers : list[SimROS2RobotManager] = []
        self.object_managers : list[SimROS2ObjectManager] = []
        self.coppeliasim_sim = sim

    def add_robot_manager(self, robot_manager: SimROS2RobotManager):
        """Registers a SimROS2RobotManager with this node."""
        self.robot_managers.append(robot_manager)

    def add_object_manager(self, robot_manager: SimROS2ObjectManager):
        """Registers a SimROS2ObjectManager with this node."""
        self.object_managers.append(robot_manager)

    def sensing_update(self):
        """Calls sensing_update on all registered managers."""
        for robot_manager in self.robot_managers:
            robot_manager.sensing_update()
        for object_manager in self.object_managers:
            object_manager.sensing_update()

    def actuation_update(self):
        """Calls actuation_update on all registered managers."""
        for robot_manager in self.robot_managers:
            robot_manager.actuation_update()
        for object_manager in self.object_managers:
            object_manager.actuation_update()
