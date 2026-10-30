# Copyright (c) 2012-2026 Murilo Marques Marinho
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

"""sas_robot_driver_coppeliasim Python package.

Exports the classes required to bridge CoppeliaSim with ROS 2 via the SAS
robot driver and object interfaces.
"""
from sas_robot_driver_coppeliasim.simros2_manager import SimROS2Manager
from sas_robot_driver_coppeliasim.simros2_node import SimROS2Node
from sas_robot_driver_coppeliasim.simros2_object_manager import SimROS2ObjectManager
from sas_robot_driver_coppeliasim.simros2_robot_manager import SimROS2RobotManager
