from sas_robot_driver_coppeliasim import SimROS2Manager

def sysCall_init():
    self.sim = require('sim')
    self.sim_ros2_manager = SimROS2Manager()
    self.sim_ros2_manager.sys_call_init()

def sysCall_actuation():
    self.sim_ros2_manager.sys_call_actuation()

def sysCall_sensing():
    self.sim_ros2_manager.sys_call_sensing()

def sysCall_cleanup():
    self.sim_ros2_manager.sys_call_cleanup()

