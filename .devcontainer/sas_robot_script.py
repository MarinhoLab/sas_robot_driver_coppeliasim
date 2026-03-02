from sas_robot_driver_coppeliasim import SimROS2Manager, SimROS2RobotManager

def sysCall_init():
    self.sim = require('sim')
    self.sas_manager = SimROS2Manager(self.sim)
    robot_base_handle = self.sim.getObject("..")
    robot_manager_1 = SimROS2RobotManager(topic_prefix="ur_1",
                                          rclcpp_node=self.sas_manager.rclcpp_node,
                                          sim=self.sim,
                                          robot_base_handle=robot_base_handle)
    self.sas_manager.add_robot_manager(robot_manager_1)
    self.sas_manager.sys_call_init()

def sysCall_actuation():
    self.sas_manager.sys_call_actuation()

def sysCall_sensing():
    self.sas_manager.sys_call_sensing()

def sysCall_cleanup():
    self.sas_manager.sys_call_cleanup()


