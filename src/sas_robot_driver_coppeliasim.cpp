/*
# Copyright (c) 2016-2025 Murilo Marques Marinho
#
#    This file is part of sas_robot_driver_myrobot.
#
#    sas_robot_driver_myrobot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sas_robot_driver_myrobot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sas_robot_driver_myrobot.  If not, see <https://www.gnu.org/licenses/>.
#
# ################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#   Based on sas_robot_driver_ur.cpp
#
# ################################################################*/


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
 * @brief RobotDriverMyrobot::get_joint_positions
 * This method should always throw an exception if the user
 * tries to obtain the joint positions in an invalid state.
 *
 * One useful way of defining that is with a VectorXd(), which
 * has by default size zero until it is initialized.
 *
 * @return a VectorXd representing the configuration space in radians.
 */
VectorXd RobotDriverCoppeliaSim::get_joint_positions()
{
    return csi_->get_joint_positions(configuration_.robot_joint_names);
}

/**
 * @brief RobotDriverCoppeliaSim::set_target_joint_positions
 * Sets the joint positions and the target joint positions of the joints given in the configuration file.
 *
 * @param desired_joint_positions_rad
 */
void RobotDriverCoppeliaSim::set_target_joint_positions(const VectorXd &desired_joint_positions_rad)
{
    csi_->set_joint_positions(configuration_.robot_joint_names, desired_joint_positions_rad);
    csi_->set_joint_target_positions(configuration_.robot_joint_names, desired_joint_positions_rad);
}

/**
 * @brief RobotDriverCoppeliaSim::connect
 *
 * Connect to CoppeliaSim with the necessary information given in the configuration file.
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
 * @brief RobotDriverCoppeliaSim::initialize
 *
 * Gets the initial joint positions state. This will guarantee that future requests make sense as long
 * as connection is still alive.
 */
void RobotDriverCoppeliaSim::initialize()
{
    csi_->get_joint_positions(configuration_.robot_joint_names);
}

/**
 * @brief RobotDriverCoppeliaSim::deinitialize.
 * Nothing to do.
 */
void RobotDriverCoppeliaSim::deinitialize()
{
    //Nothing to do.
}

/**
 * @brief RobotDriverCoppeliaSim::disconnect
 * Disconnects from CoppeliaSim.
 */
void RobotDriverCoppeliaSim::disconnect()
{
    //Nothing to do
}

std::tuple<VectorXd, VectorXd> RobotDriverCoppeliaSim::get_joint_limits()
{
    //TODO: Obtain the joint limits from the simulator. This does not seem to be trivial as of now.
    int dof = get_joint_positions().size();
    auto joint_positions_max = VectorXd::Ones(dof)*2*pi;
    auto joint_positions_min = -joint_positions_max;
    return {joint_positions_min, joint_positions_max};
}

}
