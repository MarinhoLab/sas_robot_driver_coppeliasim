from sas_common import rclcpp_Node
from sas_robot_driver import RobotDriverServer

class SimROS2RobotManager:
    def __init__(self,
                 name: str,
                 joint_names: list[str],
                 topic_prefix: str,
                 rclcpp_node: rclcpp_Node):
        self.name = name
        self.joint_names = joint_names
        self.topic_prefix = topic_prefix
        self.rclcpp_node = rclcpp_node

        self.rds = RobotDriverServer(node, self.topic_prefix)
        self.q = None




