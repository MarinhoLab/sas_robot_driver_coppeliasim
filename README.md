# sas_robot_driver_coppeliasim

## ROS2 Python Scripts In CoppeliaSim

Use the following sample environment. 

```console
cd .devcontainer
docker compose build --pull
docker compose up
```

Use the following scripts convenience scripts for the most common functionalities.

|                                      |                                                                                     |
|--------------------------------------|-------------------------------------------------------------------------------------|
| `.devcontainer/sas_object_script.py` | Add to the root of an object in the scene to get and send poses.                    |
| `.devcontainer/sas_robot_script.py`  | Add to the root of a serial-link robot to create a `sas::RobotDriverServer` for it. |

Unusual use cases can be covered by the classes inside `sas_robot_driver_coppeliasim`.
