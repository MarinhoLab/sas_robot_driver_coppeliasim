#!/bin/bash

EXAMPLE_FOLDER=~/sas_tutorial_workspace/docker/sas_robot_driver_coppeliasim/
BASE_REPO_URL=https://raw.githubusercontent.com/MarinhoLab/sas_robot_driver_coppeliasim/refs/heads/jazzy

mkdir -p "$EXAMPLE_FOLDER"
cd "$EXAMPLE_FOLDER"

curl -OL "$BASE_REPO_URL"/docker/compose.yml
curl -OL "$BASE_REPO_URL"/docker/compose_joint_interface_example.yml
curl -OL "$BASE_REPO_URL"/docker/SampleCommunicationScene.ttt

docker compose -f compose_joint_interface_example.yml build --pull
xhost +local:root
docker compose -f compose_joint_interface_example.yml up