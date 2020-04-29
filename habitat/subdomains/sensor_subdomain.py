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

def overwrite_config(config_from: Config, config_to: Any) -> None:
    r"""Takes Habitat-API config and Habitat-Sim config structures. Overwrites
     Habitat-Sim config with Habitat-API values, where a field name is present
     in lowercase. Mostly used to avoid `sim_cfg.field = hapi_cfg.FIELD` code.

    Args:
        config_from: Habitat-API config node.
        config_to: Habitat-Sim config structure.
    """

    def if_config_to_lower(config):
        if isinstance(config, Config):
            return {key.lower(): val for key, val in config.items()}
        else:
            return config

    for attr, value in config_from.items():
        if hasattr(config_to, attr.lower()):
            setattr(config_to, attr.lower(), if_config_to_lower(value))


@registry.register_subdomain(name = "sensor_subdomain")
class SensorSubdomain(Subdomain):
	def __init__(self, subdomain_config = None, default_subdomain_config = None, sim = None):
		super(SensorSubdomain, self).__init__(subdomain_config, default_subdomain_config)
		self.sim = sim
		self.default_agent_id = self.sim._sim.config.sim_cfg.default_agent_id
		self.num_sensors = len(self.sim._sim.config.agents[self.default_agent_id].sensor_specifications)
		
		self.original_near = [self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].parameters["near"] for i in range(self.num_sensors)]
		self.original_far = [self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].parameters["far"] for i in range(self.num_sensors)]
		self.original_hfov = [self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].parameters["hfov"] for i in range(self.num_sensors)]
		self.original_positionx = [s.config.POSITION[0] for s in self.sim.sensor_suite.sensors.values()]
		self.original_positiony = [s.config.POSITION[1] for s in self.sim.sensor_suite.sensors.values()]
		self.original_positionz = [s.config.POSITION[2] for s in self.sim.sensor_suite.sensors.values()]
		self.original_orientationx = [s.config.ORIENTATION[0] for s in self.sim.sensor_suite.sensors.values()]
		self.original_orientationy = [s.config.ORIENTATION[1] for s in self.sim.sensor_suite.sensors.values()]
		self.original_orientationz = [s.config.ORIENTATION[2] for s in self.sim.sensor_suite.sensors.values()]
		self.original_noise_model = ["None" for _ in range(self.num_sensors)]

		self.sensor_to_noise_model_mapping = {
		habitat_sim.SensorType.COLOR : ["None", "GaussianNoiseModel", "PoissonNoiseModel", "PoissonNoiseModel", "SaltAndPepperNoiseModel", "SpeckleNoiseModel"],
		habitat_sim.SensorType.DEPTH : ["None", "RedwoodDepthNoiseModel"],
		habitat_sim.SensorType.SEMANTIC : []
		}


	def check_noise_validity(self, sensor_type, model):
		if model in self.sensor_to_noise_model_mapping[sensor_type]:
			return True
		else:
			return False


	def set_sensor_configs(self, near, far, hfov, positionx, positiony, positionz, orientationx, orientationy, orientationz, noise_model):
		sensor_specifications = []
		for sensor in self.sim.sensor_suite.sensors.values():
			sensor.config.POSITION[0] = positionx
			sensor.config.POSITION[1] = positiony
			sensor.config.POSITION[2] = positionz
			sensor.config.ORIENTATION[0] = orientationx
			sensor.config.ORIENTATION[1] = orientationy
			sensor.config.ORIENTATION[2] = orientationz
			sim_sensor_cfg = habitat_sim.SensorSpec()
			overwrite_config(
			    config_from=sensor.config, config_to=sim_sensor_cfg
			)
			sim_sensor_cfg.uuid = sensor.uuid
			sim_sensor_cfg.resolution = list(
			    sensor.observation_space.shape[:2]
			)

			sim_sensor_cfg.sensor_type = sensor.sim_sensor_type  # type: ignore
			sim_sensor_cfg.gpu2gpu_transfer = (
			    self.sim.config.HABITAT_SIM_V0.GPU_GPU
			)
			sensor_specifications.append(sim_sensor_cfg)
		self.sim._sim.config.agents[self.default_agent_id].sensor_specifications = sensor_specifications

		for i in range(self.num_sensors):			
			self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].parameters["near"] = str(near[i])
			self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].parameters["far"] = str(far[i])
			self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].parameters["hfov"] = str(hfov[i])
			if self.check_noise_validity(self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].sensor_type, noise_model[i]):
				self.sim._sim.config.agents[self.default_agent_id].sensor_specifications[i].noise_model = noise_model[i]



	def sample(self):		
		original_probability = self.get_property("original_probability")
		if original_probability is None:
			original_probability = 0.0
		if random.uniform(0, 1) < original_probability:
			self.set_sensor_configs(self.original_near, self.original_far, self.original_hfov, self.original_positionx, self.original_positiony, self.original_positionz, self.original_orientationx, self.original_orientationy, self.original_orientationz, self.original_noise_model)
		else:
			near_range = self.get_property("near_range")
			far_range = self.get_property("far_range")
			hfov_range = self.get_property("hfov_range")
			positionx_range = self.get_property("positionx_range")
			positiony_range = self.get_property("positiony_range")
			positionz_range = self.get_property("positionz_range")
			orientationx_range = self.get_property("orientationx_range")
			orientationy_range = self.get_property("orientationy_range")
			orientationz_range = self.get_property("orientationz_range")
			noise_model_options = self.get_property("noise_model")

			near = [random.uniform(near_range[0], near_range[1]) for _ in range(self.num_sensors)] if near_range is not None else self.original_near
			far = [random.uniform(far_range[0], far_range[1]) for _ in range(self.num_sensors)] if far_range is not None else self.original_far
			hfov = [random.uniform(hfov_range[0], hfov_range[1]) for _ in range(self.num_sensors)] if hfov_range is not None else self.original_hfov
			positionx = [random.uniform(positionx_range[0], positionx_range[1]) for _ in range(self.num_sensors)] if positionx_range is not None else self.original_positionx
			positiony = [random.uniform(positiony_range[0], positiony_range[1]) for _ in range(self.num_sensors)] if positiony_range is not None else self.original_positiony
			positionz = [random.uniform(positionz_range[0], positionz_range[1]) for _ in range(self.num_sensors)] if positionz_range is not None else self.original_positionz
			orientationx = [random.uniform(orientationx_range[0], orientationx_range[1]) for _ in range(self.num_sensors)] if orientationx_range is not None else self.original_orientationx
			orientationy = [random.uniform(orientationy_range[0], orientationy_range[1]) for _ in range(self.num_sensors)] if orientationy_range is not None else self.original_orientationy
			orientationz = [random.uniform(orientationz_range[0], orientationz_range[1]) for _ in range(self.num_sensors)] if orientationz_range is not None else self.original_orientationz
			noise_model = [noise_model_options[random.randint(0, len(noise_model_options) - 1)] for _ in range(self.num_sensors)] if noise_model_options is not None else self.original_noise_model


			self.set_sensor_configs(near, far, hfov, positionx, positiony, positionz, orientationx, orientationy, orientationz, noise_model)
		
		self.sim._sim.__attrs_post_init__()



