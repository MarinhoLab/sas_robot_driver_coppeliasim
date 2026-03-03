import time
from rclpy.node import Node

from sas_common import rclcpp_Node
from .simros2_robot_manager import SimROS2RobotManager
from .simros2_object_manager import SimROS2ObjectManager


class SimROS2Node(Node):
    def __init__(self,
                 rclcpp_node: rclcpp_Node,
                 sim
                 ):
        timestamp_for_anonymous_name = str(time.time()).replace('.', '_')
        super().__init__(f"sas_simros2_{timestamp_for_anonymous_name}_python_node")
        self.rclcpp_node: rclcpp_Node = rclcpp_node
        self.robot_managers : list[SimROS2RobotManager] = []
        self.object_managers : list[SimROS2ObjectManager] = []
        self.coppeliasim_sim = sim

    def add_robot_manager(self, robot_manager: SimROS2RobotManager):
        self.robot_managers.append(robot_manager)

    def add_object_manager(self, robot_manager: SimROS2ObjectManager):
        self.object_managers.append(robot_manager)

    def sensing_update(self):
        for robot_manager in self.robot_managers:
            robot_manager.sensing_update()
        for object_manager in self.object_managers:
            object_manager.sensing_update()

    def actuation_update(self):
        for robot_manager in self.robot_managers:
            robot_manager.actuation_update()
        for object_manager in self.object_managers:
            object_manager.actuation_update()
