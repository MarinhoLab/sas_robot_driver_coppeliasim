# Testing colcon build

This will test if colcon builds properly and the basic sample script can be executed.

```console
cd .devcontainer
docker compose -f compose_colcon.yml build --pull
docker compose -f compose_colcon.yml up
```

# Testing network

I could not make the ROS2 communication work over `qemu`. Given that it didn't work, I can only guess why it isn't
working. Then using both computers as `x64` architecture (or compatible with the host) it worked fine.

Use the following to test the communication between containers. If this doesn't work, then the coppeliasim
script won't work either.

```console
cd .devcontainer
docker compose -f compose_comm_test.yml build --pull
docker compose -f compose_comm_test.yml up
```

# Testing with CoppeliaSim

```console
xhost +
cd .devcontainer
docker compose -f compose_view.yml build --pull
docker compose -f compose_view.yml up
```

