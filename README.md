# sas_robot_driver_coppeliasim

## ROS2 Python Scripts In CoppeliaSim

Use the following sample environment. 

```console
cd docker
docker compose build --pull
docker compose up
```

Use the following scripts convenience scripts for the most common functionalities.

|                                      |                                                                                     |
|--------------------------------------|-------------------------------------------------------------------------------------|
| `.devcontainer/sas_object_script.py` | Add to the root of an object in the scene to get and send poses.                    |
| `.devcontainer/sas_robot_script.py`  | Add to the root of a serial-link robot to create a `sas::RobotDriverServer` for it. |

Unusual use cases can be covered by the classes inside `sas_robot_driver_coppeliasim`.

Notes
- Remember to edit `COPPELIA_SIM_SCENE_PATH` in the compose file to be the scene file in a reachable volume.

## Controlling robots with `sas`

A sample joint controller can be used with the following environment. This will run the sample simulation and the sample
script `scripts/joint_interface_example.py`.

```console
cd docker
docker compose -f compose_joint_interface_example.yml build --pull
docker compose -f compose_joint_interface_example.yml up
```