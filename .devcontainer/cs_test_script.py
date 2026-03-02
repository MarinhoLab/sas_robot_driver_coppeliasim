from geometry_msgs.msg import Point

import rclpy
from rclpy.node import Node

def sysCall_init():
    rclpy.init(args=None)
    self.node = Node("hello")
    self.amazing_quote_publisher = self.node.create_publisher(
        msg_type=Point,
        topic='/point',
        qos_profile=1)

def sysCall_actuation():
    self.amazing_quote_publisher.publish(Point())

def sysCall_sensing():
    rclpy.spin_once(self.node, timeout_sec=0.0)

def sysCall_cleanup():
    self.node.destroy_node()
    rclpy.shutdown()


