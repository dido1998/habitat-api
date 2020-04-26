#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import random

import habitat_sim
from habitat.core.logging import logger
from habitat.core.subdomain import Subdomain		
from habitat.core.registry import registry


@registry.register_subdomain(name = "agent_subdomain")
class AgentSubdomain(Subdomain):
	def __init__(self, subdomain_config = None, default_subdomain_config = None, sim = None):
		super(AgentSubdomain, self).__init__(subdomain_config, default_subdomain_config)
		self.sim = sim._sim
		self.num_agents = len(self.sim.config.agents)
		self.original_height = [self.sim.config.agents[i].height for i in range(self.num_agents)]
		self.original_radius = [self.sim.config.agents[i].radius for i in range(self.num_agents)]
		self.original_linear_acceleration = [self.sim.config.agents[i].linear_acceleration for i in range(self.num_agents)] 
		self.original_angular_acceleration = [self.sim.config.agents[i].angular_acceleration for i in range(self.num_agents)]
		self.original_linear_friction = [self.sim.config.agents[i].linear_friction for i in range(self.num_agents)]
		self.original_angular_friction = [self.sim.config.agents[i].angular_friction for i in range(self.num_agents)]

	def set_agent_configs(self, height, radius, linear_acceleration, angular_acceleration, linear_friction, angular_friction):
		for i in range(self.num_agents):
			self.sim.config.agents[i].height = height[i]
			self.sim.config.agents[i].radius = radius[i]
			self.sim.config.agents[i].linear_acceleration = linear_acceleration[i]
			self.sim.config.agents[i].angular_acceleration = angular_acceleration[i]
			self.sim.config.agents[i].linear_friction = linear_friction[i]
			self.sim.config.agents[i].angular_friction = angular_friction[i]

	def sample(self):
		original_probability = self.get_property("original_probability")
		if random.uniform(0, 1) < original_probability:
			self.set_agent_configs(self.original_height, self.original_radius, self.original_linear_acceleration, self.original_angular_acceleration, self.original_linear_friction, self.original_angular_friction)
		else:
			height_range = self.get_property('height_range')
			radius_range = self.get_property('radius_range')
			linear_acceleration_range = self.get_property('linear_acceleration_range')
			angular_acceleration_range = self.get_property('angular_acceleration_range')
			linear_friction_range = self.get_property('linear_friction_range')
			angular_friction_range = self.get_property('angular_friction_range')
			
			height = [random.uniform(height_range[0], height_range[1]) for _ in range(self.num_agents)] if height_range is not None else self.original_height
			radius = [random.uniform(radius_range[0], radius_range[1]) for _ in range(self.num_agents)] if radius_range is not None else self.original_radius
			linear_acceleration = [random.uniform(linear_acceleration_range[0], linear_acceleration_range[1]) for _ in range(self.num_agents)] if linear_acceleration_range is not None else self.original_linear_acceleration
			angular_acceleration = [random.uniform(angular_acceleration_range[0], angular_acceleration_range[1]) for _ in range(self.num_agents)] if angular_acceleration_range is not None else self.original_linear_acceleration_range
			linear_friction = [random.uniform(linear_friction_range[0], linear_friction_range[1]) for _ in range(self.num_agents)] if linear_friction_range is not None else self.original_linear_friction 
			angular_friction = [random.uniform(angular_acceleration_range[0], angular_acceleration_range[1]) for _ in range(self.num_agents) ] if angular_friction_range is not None else self.original_angular_friction

			self.set_agent_configs(height, radius, linear_acceleration, angular_acceleration, linear_friction, angular_friction)

		self.sim.__attrs_post_init__()
