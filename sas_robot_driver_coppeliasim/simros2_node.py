import rclpy
from rclpy.node import Node

from sas_common import rclcpp_Node
from .simros2_robot_manager import SimROS2RobotManager


class SimROS2Node(Node):
    def __init__(self,
                 rclcpp_node: rclcpp_Node,
                 sim
                 ):
        super().__init__("sas_simros2_python_node")
        self.rclcpp_node: rclcpp_Node = rclcpp_node
        self.robot_managers : list[SimROS2RobotManager] = []
        self.coppeliasim_sim = sim

    def add_robot_manager(self, robot_manager: SimROS2RobotManager):
        self.robot_managers.append(robot_manager)

    def update(self):
        for robot_manager in self.robot_managers:
            robot_manager.update()
