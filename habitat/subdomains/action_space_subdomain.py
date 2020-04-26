#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import random

import habitat_sim
from habitat.core.logging import logger
from habitat.core.subdomain import Subdomain		
from habitat.core.registry import registry


@registry.register_subdomain(name = "action_space_subdomain")
class ActionSpaceSubdomain(Subdomain):
	def __init__(self, subdomain_config = None, default_subdomain_config = None, sim = None):
		super(ActionSpaceSubdomain, self).__init__(subdomain_config, default_subdomain_config)
		self.sim = sim._sim
		self.default_agent_id = self.sim.config.sim_cfg.default_agent_id
		self.original = {}
		self.mapping = {}
		action_space = self.sim.config.agents[self.default_agent_id].action_space
		for action in action_space:
			self.original[action_space[action].name] = action_space[action].actuation
			self.mapping[action_space[action].name] = action


	def sample(self):
		original_probability = self.get_property("original_probability")
		if random.uniform(0, 1) < original_probability:
			for action in self.mapping:
				if self.original[action] is None:
					continue
				self.sim.config.agents[self.default_agent_id].action_space[self.mapping[action]].actuation.amount = self.original[action].amount
		else:
			forward_range = self.get_property("forward_range")
			turn_range = self.get_property("turn_range")

			forward = random.uniform(forward_range[0], forward_range[1]) if forward_range is not None else None
			turn = random.uniform(turn_range[0], turn_range[1]) if turn_range is not None else None

			for action in self.mapping:
				if self.original[action] is None:
					continue
				if 'forward' in action:
					self.sim.config.agents[self.default_agent_id].action_space[self.mapping[action]].actuation.amount = forward if forward is not None else self.original[action].amount
				elif 'turn' in action:
					self.sim.config.agents[self.default_agent_id].action_space[self.mapping[action]].actuation.amount = turn if turn is not None else self.original[action].amount

		self.sim.__attrs_post_init__()
