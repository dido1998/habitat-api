#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any
import random

import habitat_sim
from habitat.core.logging import logger
from habitat.core.subdomain import Subdomain		
from habitat.core.registry import registry
from habitat.core.simulator import Config


@registry.register_subdomain(name = "object_subdomain")
class ObjectSubdomain(Subdomain):
    def __init__(self, subdomain_config = None, default_subdomain_config = None, sim = None, sim_cfg = None):
        super(ObjectSubdomain, self).__init__(subdomain_config, default_subdomain_config)
        self.sim = sim
        new_physics_file = self.get_property("physics_config_file")
        
        if new_physics_file is not None:
            self.sim._sim.config.sim_cfg.physics_config_file = new_physics_file
            self.sim._sim.config.sim_cfg.enable_physics = True
            self.sim._sim._config_backend(self.sim._sim.config)

        if self.sim._sim.config.sim_cfg.enable_physics == False:
            self.sim._sim.config.sim_cfg.enable_physics = True
            self.sim._sim._config_backend(self.sim._sim.config)

        self.num_objects = self.sim._sim.get_physics_object_library_size()
        self.added_object_ids = []


    def sample(self):
        if len(self.added_object_ids) > 0:
            for object_id in self.added_object_ids:
                self.sim._sim.remove_object(object_id)
            self.added_object_ids = []
        original_probability = self.get_property("original_probability")
        if random.uniform(0, 1) < original_probability:
            return
        else:
            num_objects_range = self.get_property("num_objects_range")
            num_objects_to_add = random.randint(num_objects_range[0], num_objects_range[1])
            for i in range(num_objects_to_add):
                object_id = random.randint(0, self.num_objects - 1)
                cur_id = self.sim._sim.add_object(object_id)
                if cur_id == -1:
                    continue
                self.added_object_ids.append(cur_id)

                navigable_point = self.sim._sim.pathfinder.get_random_navigable_point()

                self.sim._sim.set_translation(navigable_point, cur_id)
                self.sim._sim.set_object_motion_type(habitat_sim.physics.MotionType.STATIC, cur_id)

            if len(self.added_object_ids) > 0:
                navmesh_settings = habitat_sim.NavMeshSettings()
                navmesh_settings.set_defaults()
                self.sim._sim.recompute_navmesh(self.sim._sim.pathfinder, navmesh_settings, include_static_objects=True)
