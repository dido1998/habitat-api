#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import random

import habitat_sim
from habitat_sim.gfx import (
    DEFAULT_LIGHTING_KEY,
    NO_LIGHT_KEY,
    LightInfo,
    LightPositionModel,
)
from habitat.core.logging import logger
from habitat.core.subdomain import Subdomain		
from habitat.core.registry import registry


@registry.register_subdomain(name = "light_subdomain")
class LightSubdomain(Subdomain):
	def __init__(self, subdomain_config = None, default_subdomain_config = None, sim = None):
		super(LightSubdomain, self).__init__(subdomain_config, default_subdomain_config)
		self.sim = sim._sim

	def sample(self):
		original_probability = self.get_property("original_probability")
		if original_probability is None:
			original_probability = 0.0
		if random.uniform(0, 1) < original_probability:
			lighting = [LightInfo(position=[1.0, 1.0, 1.0], color = [1.0, 1.0, 1.0, 1.0], model=LightPositionModel.CAMERA)]
			self.sim.set_light_setup(lighting)
		else:
			x_range = self.get_property('x_range')
			y_range = self.get_property('y_range')
			z_range = self.get_property('z_range')

			r_range = self.get_property('r_range')
			g_range = self.get_property('g_range')
			b_range = self.get_property('b_range')
			a_range = self.get_property('a_range')

			x = random.uniform(x_range[0], x_range[1]) if x_range is not None else 1.0
			y = random.uniform(y_range[0], y_range[1]) if y_range is not None else 1.0
			z = random.uniform(z_range[0], z_range[1]) if z_range is not None else 1.0
			r = random.uniform(r_range[0], r_range[1]) if r_range is not None else 1.0
			g = random.uniform(g_range[0], g_range[1]) if g_range is not None else 1.0
			b = random.uniform(b_range[0], b_range[1]) if b_range is not None else 1.0
			a = random.uniform(a_range[0], a_range[1]) if a_range is not None else 1.0

			lighting = [LightInfo(position = [x, y, z], color = [r, g, b, a], model=LightPositionModel.CAMERA)]
			self.sim.set_light_setup(lighting)
