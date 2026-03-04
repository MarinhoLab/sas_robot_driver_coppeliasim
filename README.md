# sas_robot_driver_coppeliasim

> [!TIP]
> Repository for this module: https://github.com/MarinhoLab/sas_robot_driver_coppeliasim \
> More information about SmartArmStack is available in https://smartarmstack.github.io/.

> [!NOTE]
> `sas_robot_driver_coppeliasim_node` is being replaced by the ROS2 Python scripts described below.
> `zmq` interface for `CoppeliaSim` currently cannot handle multiple operations at a high frequency.

## ROS2 Python Scripts In CoppeliaSim

> [!IMPORTANT]
> This image only works in `amd64` environments owing to CoppeliaSim limitations. 
> It does not work in `arm64` even with `qemu`.

```console
mkdir -p ~/sas_tutorial_workspace/docker/sas_robot_driver_coppeliasim
cd ~/sas_tutorial_workspace/docker/sas_robot_driver_coppeliasim/
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_robot_driver_coppeliasim/refs/heads/jazzy/docker/run_docker_sample.sh
chmod +x run_docker_sample.sh
./run_docker_sample.sh
```

Notes
- Remember to edit `COPPELIA_SIM_SCENE_FILE` in the compose file to be the correct scene file in the same directory.
- Each robot is being controlled with the script `scripts/joint_interface_example.py`.

### Adding capabilities to your own scenes

Use the following convenience scripts for the most common functionalities.

|                                      |                                                                                     |
|--------------------------------------|-------------------------------------------------------------------------------------|
| `.devcontainer/sas_object_script.py` | Add to the root of an object in the scene, for instance, to get and send poses.     |
| `.devcontainer/sas_robot_script.py`  | Add to the root of a serial-link robot to create a `sas::RobotDriverServer` for it. |

Unusual use cases can be covered by the classes in the Python module `sas_robot_driver_coppeliasim`.
