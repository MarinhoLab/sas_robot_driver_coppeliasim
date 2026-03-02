from sas_robot_driver_coppeliasim import SimROS2Manager

def sysCall_init():
    self.sas_manager = SimROS2Manager()
    self.sas_manager.sys_call_init()

def sysCall_actuation():
    self.sas_manager.sys_call_actuation()

def sysCall_sensing():
    self.sas_manager.sys_call_sensing()

def sysCall_cleanup():
    self.sas_manager.sys_call_cleanup()


