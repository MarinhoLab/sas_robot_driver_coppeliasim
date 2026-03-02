from sas_robot_driver_coppeliasim import SimROS2Manager
from geometry_msgs.msg import Point
#python

import rclpy
from rclpy.node import Node

def sysCall_init():
    sim = require('sim')
    rclpy.init(args=None)
    print("Hi")
    self.node = Node("hello")
    self.amazing_quote_publisher = self.node.create_publisher(
        msg_type=Point,
        topic='/point',
        qos_profile=1)

    # do some initialization here
    #
    # Instead of using globals, you can do e.g.:
    # self.myVariable = 21000000

def sysCall_actuation():
    # self.node.get_logger().info(f'Printed.')
    self.amazing_quote_publisher.publish(Point())

def sysCall_sensing():
    rclpy.spin_once(self.node, timeout_sec=0.0)
    #print("hello")
    #pass
    #global sas_manager
    #sas_manager.sys_call_sensing()

def sysCall_cleanup():
    rclpy.shutdown()

# See the user manual or the available code snippets for additional callback functions and details
