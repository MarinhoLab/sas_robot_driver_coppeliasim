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

#include <atomic>
#include <memory>

#include <sas_core/sas_robot_driver.hpp>

#include <dqrobotics/interfaces/coppeliasim/DQ_CoppeliaSimInterfaceZMQ.h>

using namespace Eigen;

namespace sas
{

struct RobotDriverCoppeliaSimConfiguration
{
    int port;
    std::string ip;
    int timeout = 1000;
    std::vector<std::string> robot_joint_names;
};


class RobotDriverCoppeliaSim: public RobotDriver
{
private:
    RobotDriverCoppeliaSimConfiguration configuration_;

    VectorXd joint_positions_;
    std::shared_ptr<DQ_CoppeliaSimInterfaceZMQ> csi_;
public:

    // Prevent copies as usually drivers have threads
    RobotDriverCoppeliaSim(const RobotDriverCoppeliaSim&)=delete;
    RobotDriverCoppeliaSim()=delete;
    ~RobotDriverCoppeliaSim();

    // This boilderplate constructor usually does the job well and prevent big changes when
    // parameters change
    RobotDriverCoppeliaSim(const RobotDriverCoppeliaSimConfiguration &configuration, std::atomic_bool* break_loops);

    /// Everything below this line is an override
    /// the concrete implementations are needed
    VectorXd get_joint_positions() override;
    void set_target_joint_positions(const VectorXd& desired_joint_positions_rad) override;
    std::tuple<VectorXd, VectorXd> get_joint_limits() override;

    void connect() override;
    void disconnect() override;

    void initialize() override;
    void deinitialize() override;

};
}
