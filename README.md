# sas_robot_driver_coppeliasim

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
- Remember to edit `COPPELIA_SIM_SCENE_PATH` in the compose file to be the scene file in a reachable volume.

### Adding capabilities to your own scenes

Use the following scripts convenience scripts for the most common functionalities.

|                                      |                                                                                     |
|--------------------------------------|-------------------------------------------------------------------------------------|
| `.devcontainer/sas_object_script.py` | Add to the root of an object in the scene to get and send poses.                    |
| `.devcontainer/sas_robot_script.py`  | Add to the root of a serial-link robot to create a `sas::RobotDriverServer` for it. |

Unusual use cases can be covered by the classes in the Python module `sas_robot_driver_coppeliasim`.

### Controlling robots with `sas`

A sample script is available in `scripts/joint_interface_example.py`.
