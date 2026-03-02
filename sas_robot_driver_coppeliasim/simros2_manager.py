import rclpy
from rclpy.node import Node
from sas_common import rclcpp_init, rclcpp_Node, rclcpp_spin_some, rclcpp_shutdown
from .simros2_node import SimROS2Node

class SimROS2Manager:
    def __init__(self):
        self.node: Node = None
        self.rclcpp_node: rclcpp_Node = None

    def sys_call_init(self):
        """
        Based on Juan's tutorial
        :return:
        """
        try:
            if self.node is None:
                rclpy.init(args=None)
                rclcpp_init()
                self.rclcpp_node = rclcpp_Node("sas_simros2_cpp_node")
                self.node = SimROS2Node(self.rclcpp_node)
                print("ROS 2 node initialized successfully")

        except Exception as e:
            print(f"Error initializing ROS 2: {e}")

    def sys_call_actuation(self):
        pass


    def sys_call_sensing(self):
        if self.node is not None:
            rclpy.spin_once(self.node, timeout_sec=0.0)
            rclcpp_spin_some(self.rclcpp_node)

    def sys_call_cleanup(self):
        if self.node is not None:
            rclpy.shutdown()
            rclcpp_shutdown()