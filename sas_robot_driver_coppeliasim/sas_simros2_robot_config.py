class SASSimROS2RobotManager:
    def __init__(self,
                 name: str,
                 joint_names: list[str],
                 topic_prefix: str):
        self.name = name
        self.joint_names = joint_names
        self.topic_prefix = topic_prefix


