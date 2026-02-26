import rclpy
from rclpy.node import Node

from sas_common import rclcpp_init, rclcpp_Node, rclcpp_spin_some, rclcpp_shutdown
from sas_robot_driver import RobotDriverServer

from sas_robot_driver_coppeliasim import SASSimROS2RobotManager

class SASSimROS2(Node):
    def __init__(self):
        super().__init__("sas_simros2")

        self.rclcpp_node = rclcpp_Node("sas_simros2_cpp")
        self.robot_managers : list[SASSimROS2RobotManager] = []

    def add_robot_manager(self, robot_manager: SASSimROS2RobotManager):

    def sysCall_init(self):
        pass

    def sysCall_actuation(self):
        pass

    def sysCall_sensing(self):
        pass

    def sysCall_cleanup(self):