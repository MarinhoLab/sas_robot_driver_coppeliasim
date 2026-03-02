from dqrobotics import *
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from sas_conversions import geometry_msgs_pose_stamped_to_dq

class SimROS2ObjectManager:

    def __init__(self,
                 object_handle: int,
                 node: Node,
                 sim):

        self.object_handle = object_handle
        self.object_alias = sim.getObjectAlias(object_handle, 1).replace("[", "_").replace("]", "_")

        self.publishers = node.create_publisher(
            msg_type=PoseStamped,
            topic=f'/sas_robot_driver_coppeliasim/object{self.object_alias}/get/pose',
            qos_profile=1)

        self.subscriber = node.create_subscription(
            msg_type=PoseStamped,
            topic=f'/sas_robot_driver_coppeliasim/object{self.object_alias}/set/pose',
            callback=self.subscriber_callback,
            qos_profile=1)

        self.x = None

    def update(self):
        if self.x is not None:
            t = vec3(translation(self.x))
            r = vec4(rotation(self.x))
            x_cs = [t[0], t[1], t[2],
                    r[1], r[2], r[3], r[0]]
            self.sim.setObjectPose(self.object_handle, x_cs)

    def subscriber_callback(self, msg: PoseStamped):
        self.x = geometry_msgs_pose_stamped_to_dq(msg)


