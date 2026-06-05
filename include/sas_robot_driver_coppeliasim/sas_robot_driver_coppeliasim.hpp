#pragma once
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
#   Based on `sas` ros composer.
#
# ################################################################*/

/**
 * @file sas_robot_driver_coppeliasim.hpp
 * @brief RobotDriver for CoppeliaSim via ZMQ.
 */

#include <atomic>
#include <memory>

#include <sas_core/sas_robot_driver.hpp>

#include <dqrobotics/interfaces/coppeliasim/DQ_CoppeliaSimInterfaceZMQ.h>

using namespace Eigen;

namespace sas
{

/**
 * @brief Configuration for RobotDriverCoppeliaSim.
 */
struct RobotDriverCoppeliaSimConfiguration
{
    int port;                                   ///< ZMQ port number.
    std::string ip;                             ///< CoppeliaSim IP address.
    int timeout = 1000;                         ///< Connection timeout in milliseconds.
    std::vector<std::string> robot_joint_names; ///< Names of the joints to control.
};

/**
 * @brief RobotDriver for CoppeliaSim via ZMQ.
 */
class RobotDriverCoppeliaSim: public RobotDriver
{
private:
    RobotDriverCoppeliaSimConfiguration configuration_; ///< Driver configuration.
    VectorXd joint_positions_;                          ///< Cached joint positions.
    std::shared_ptr<DQ_CoppeliaSimInterfaceZMQ> csi_;   ///< CoppeliaSim ZMQ interface.

public:

    // Prevent copies as usually drivers have threads
    RobotDriverCoppeliaSim(const RobotDriverCoppeliaSim&)=delete;
    RobotDriverCoppeliaSim()=delete;
    ~RobotDriverCoppeliaSim();

    /**
     * @brief Constructs the driver.
     * @param configuration Driver configuration parameters.
     * @param break_loops Pointer to the loop-breaking flag.
     */
    RobotDriverCoppeliaSim(const RobotDriverCoppeliaSimConfiguration &configuration, std::atomic_bool* break_loops);

    /**
     * @brief Returns current joint positions in radians.
     * @return Joint positions as a VectorXd.
     */
    VectorXd get_joint_positions() override;

    /**
     * @brief Sets joint positions and target joint positions.
     * @param desired_joint_positions_rad Desired joint positions in radians.
     */
    void set_target_joint_positions(const VectorXd& desired_joint_positions_rad) override;

    /**
     * @brief Returns joint position limits.
     * @return Tuple of (min, max) joint position vectors.
     */
    std::tuple<VectorXd, VectorXd> get_joint_limits() override;

    /**
     * @brief Connects to the CoppeliaSim instance.
     */
    void connect() override;

    /**
     * @brief Disconnects from the CoppeliaSim instance.
     */
    void disconnect() override;

    /**
     * @brief Initializes the driver state.
     */
    void initialize() override;

    /**
     * @brief Deinitializes the driver state.
     */
    void deinitialize() override;

};
}
