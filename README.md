# sas_robot_driver_coppeliasim

> [!TIP]
> Repository for this module: https://github.com/MarinhoLab/sas_robot_driver_coppeliasim \
> More information about SmartArmStack is available in https://smartarmstack.github.io/.

> [!NOTE]
> `sas_robot_driver_coppeliasim_node` is being replaced by the ROS2 Python scripts described below.
> `zmq` interface for `CoppeliaSim` currently cannot handle multiple operations at a high frequency.

## ROS 2 Nodes & Parameters

### Node: `sas_robot_driver_coppeliasim_node`

| Property | Value |
|---|---|
| **Executable** | `sas_robot_driver_coppeliasim_node` |
| **ROS node name** | `myrobot_1` (set by the `name` launch argument of `robot_launch.py`) |
| **Description** | Robot driver node for CoppeliaSim. Reads all parameters, instantiates `RobotDriverCoppeliaSim` (ZMQ interface to the simulated robot) and `RobotDriverROS` (runs the control loop). |

#### Parameters

| Parameter | Type | Mandatory / Optional | Default | Purpose |
|---|---|---|---|---|
| `joint_limits_min` | array of doubles (degrees) | **Mandatory** | none — must be provided | Minimum joint limits; converted from deg → rad internally |
| `joint_limits_max` | array of doubles (degrees) | **Mandatory** | none — must be provided | Maximum joint limits; converted from deg → rad internally |
| `robot_joint_names` | array of strings | **Mandatory** | none — must be provided | Names of the robot joints to control |
| `thread_sampling_time_sec` | double | **Mandatory** | none — must be provided | Sampling period of the robot control-loop thread (e.g. `0.002` s = 500 Hz) |
| `ip` | string | Optional | `127.0.0.1` | CoppeliaSim (ZMQ) IP address |
| `port` | int | Optional | `23000` | CoppeliaSim (ZMQ) port number |
| `timeout` | int | Optional | `1000` | ZMQ connection timeout, in milliseconds |

**How mandatory/optional is determined in code:**
- **Mandatory** params are read with `sas::get_ros_parameter(...)` — if missing, the node throws and fails to start.
- **Optional** params are read with `sas::get_ros_optional_parameter(..., <default>)` — they carry in-code defaults.

#### Sample launch

`launch/robot_launch.py` starts the node with the parameters from `config/config.yaml`:

```console
ros2 launch sas_robot_driver_coppeliasim robot_launch.py
```

To use a different node name or configuration file:

```console
ros2 launch sas_robot_driver_coppeliasim robot_launch.py name:=myrobot_2 config_file:=/path/to/config.yaml
```

## ROS2 Python Scripts In CoppeliaSim

> [!CAUTION]
> This image only works in `amd64` environments owing to CoppeliaSim limitations. 
> It does not work in `arm64` even with `qemu`.

https://github.com/user-attachments/assets/3d6222b8-e683-4039-ab72-d6a7ad08ba51

![](./sas_rdcs_sample.mp4)

Run the following.

```console
mkdir -p ~/sas_tutorial_workspace/docker/sas_robot_driver_coppeliasim
cd ~/sas_tutorial_workspace/docker/sas_robot_driver_coppeliasim/
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_robot_driver_coppeliasim/refs/heads/jazzy/docker_sample/run_docker_sample.sh
chmod +x run_docker_sample.sh
./run_docker_sample.sh
```

Notes
- Remember to edit `COPPELIA_SIM_SCENE_FILE` in the compose file to be the correct scene file in the same directory.
- Each robot is being controlled with the script `scripts/joint_interface_example.py`.

### Adding capabilities to your own scenes

Use the following convenience scripts for the most common functionalities.

> [!IMPORTANT]
> Add the scripts via the top menu with `Add` ▶️ `Script` ▶️ `simulation script` ▶️ `Non threaded` ▶️ `Python`.

|                                      |                                                                                                        |
|--------------------------------------|--------------------------------------------------------------------------------------------------------|
| `.devcontainer/sas_object_script.py` | Add as immediate child to the root of an object in the scene, for instance, to get and send poses.     |
| `.devcontainer/sas_robot_script.py`  | Add as immediate child to the root of a serial-link robot to create a `sas::RobotDriverServer` for it. |

Unusual use cases can be covered by the classes in the Python module `sas_robot_driver_coppeliasim`.
