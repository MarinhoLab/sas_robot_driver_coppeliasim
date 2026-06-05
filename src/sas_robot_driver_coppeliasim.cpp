/*
# Copyright (c) 2016-2025 Murilo Marques Marinho
#
#    This file is part of sas_robot_driver_coppeliasim.
#
#    sas_robot_driver_coppeliasim is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sas_robot_driver_coppeliasim is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sas_robot_driver_coppeliasim.  If not, see <https://www.gnu.org/licenses/>.
#
# ################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#   Based on sas_robot_driver_ur.cpp
#
# ################################################################*/

/**
 * @file sas_robot_driver_coppeliasim.cpp
 * @brief RobotDriverCoppeliaSim implementation.
 */


#include "sas_robot_driver_coppeliasim/sas_robot_driver_coppeliasim.hpp"
#include <dqrobotics/utils/DQ_Constants.h>
#include <sas_core/eigen3_std_conversions.hpp>

namespace sas
{


RobotDriverCoppeliaSim::RobotDriverCoppeliaSim(const RobotDriverCoppeliaSimConfiguration &configuration, std::atomic_bool* break_loops):
    RobotDriver(break_loops),
    configuration_(configuration)
{
    csi_ = std::make_shared<DQ_CoppeliaSimInterfaceZMQ>();
}

RobotDriverCoppeliaSim::~RobotDriverCoppeliaSim()
{

}

/**
 * @brief Returns current joint positions in radians.
 *
 * Throws if the interface is in an invalid state (e.g., not connected).
 *
 * @return Joint positions as a VectorXd.
 */
VectorXd RobotDriverCoppeliaSim::get_joint_positions()
{
    return csi_->get_joint_positions(configuration_.robot_joint_names);
}

/**
 * @brief Sets joint positions and target joint positions.
 * @param desired_joint_positions_rad Desired joint positions in radians.
 */
void RobotDriverCoppeliaSim::set_target_joint_positions(const VectorXd &desired_joint_positions_rad)
{
    csi_->set_joint_positions(configuration_.robot_joint_names, desired_joint_positions_rad);
    csi_->set_joint_target_positions(configuration_.robot_joint_names, desired_joint_positions_rad);
}

/**
 * @brief Connects to the CoppeliaSim instance.
 *
 * Throws std::runtime_error if the connection attempt fails.
 */
void RobotDriverCoppeliaSim::connect()
{
    if(!csi_->connect(configuration_.ip,
                       configuration_.port,
                       configuration_.timeout))
    {
        throw std::runtime_error("::Unable to connect to CoppeliaSim.");
    }
}

/**
 * @brief Initializes the driver state.
 *
 * Reads the initial joint positions to ensure the internal state is valid
 * before the control loop begins.
 */
void RobotDriverCoppeliaSim::initialize()
{
    csi_->get_joint_positions(configuration_.robot_joint_names);
}

/**
 * @brief Deinitializes the driver state.
 */
void RobotDriverCoppeliaSim::deinitialize()
{
    //Nothing to do.
}

/**
 * @brief Disconnects from the CoppeliaSim instance.
 */
void RobotDriverCoppeliaSim::disconnect()
{
    //Nothing to do
}

/**
 * @brief Returns joint position limits.
 *
 * Joint limits are queried from the simulator when available.
 * For cyclic joints, limits are set to the representable float range.
 *
 * @return Tuple of (min, max) joint position vectors in radians.
 */
std::tuple<VectorXd, VectorXd> RobotDriverCoppeliaSim::get_joint_limits()
{
    //TODO: Obtain the joint limits from the simulator. This does not seem to be trivial as of now.
    int dof = get_joint_positions().size();
    auto joint_positions_max = VectorXd::Ones(dof)*2*pi;
    auto joint_positions_min = -joint_positions_max;
    return {joint_positions_min, joint_positions_max};
}

}
