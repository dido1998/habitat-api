#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import json
import os

from habitat.core.logging import logger
from habitat.config import Config
from habitat.core.simulator import Simulator
from habitat.subdomains import make_subdomain


class DomainRandomization:
	def __init__(self, sim_cfg: Config, sim: Simulator):
		data_file = sim_cfg.DOMAIN_RANDOMIZATION.DATA_PATH
		default_data_file = sim_cfg.DOMAIN_RANDOMIZATION.DEFAULT_DATA_PATH

		subdomain_config = {}
		default_subdomain_config = {}
		default_exists = True
		if not os.path.exists(default_data_file):
			logger.warning("default domain randomization configuration {} not found".format(default_data_file))
			default_exists = False 
		self.enabled = True 
		if not os.path.exists(data_file):
			logger.warning("specified domain randomization configuration {} not found, falling back to default configuration".format(data_file))
			if default_exists:
				data_file = default_data_file
			else:
				logger.warning('default {} an specifiedd {} configurations do not exist, will not use domain randomization'.format(data_file, default_data_file))
				self.enabled = False

		if self.enabled:
			config = json.load(open(data_file))
			subdomain_dir = os.path.join(os.path.dirname(data_file), 'subdomain_properties')
			default_subdomain_dir = os.path.join(os.path.dirname(default_data_file), 'subdomain_properties')
			for s in config['subdomains']:
				subdomain_path = os.path.join(subdomain_dir, s + '.json')
				default_subdomain_path = os.path.join(default_subdomain_dir, s + '.json')
				if os.path.exists(default_subdomain_path):
					default_subdomain_config[s] = json.load(open(default_subdomain_path))
				else:
					default_subdomain_config[s] = None
				if not os.path.exists(subdomain_path):
					subdomain_config[s] = json.load(open(subdomain_path))
				else:
					subdomain_config[s] = None
					if subdomain_config[s] is None and default_subdomain_config[s] is not None:
						subdomain_config[s] = default_subdomain_config[s]
						logger.warning('specified domain randomization configuration for {} not found, falling back to default configuration'.format(s))
					if subdomain_config[s] is None and default_subdomain_config[s] is None:
						logger.warning('could not find any configuration for {}'.format(s))

		self.subdomains = []

		for s_user, s_default in zip(subdomain_config, default_subdomain_config):
			if subdomain_config[s_user] is not None:
				self.subdomains.append(make_subdomain(s_user, subdomain_config = subdomain_config[s_user], default_subdomain_config = default_subdomain_config[s_default], sim = sim, sim_cfg = sim_cfg))
				logger.info('loaded {} subdomain'.format(s_user))

	def sample(self):
		if not self.enabled:
			return
		for s in self.subdomains:
			s.sample()
