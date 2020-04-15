#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from habitat.core.logging import logger

class Subdomain(object):
	def __init__(self, subdomain_config, default_subdomain_config):
		self.subdomain = subdomain_config["name"]
		self.properties = subdomain_config
		self.default_properties = default_subdomain_config

	def sample(self):
		raise NotImplementedError

	def set_property(self, name, value):
		if name in self.properties or self.default_properties is None:
			properties = self.properties
		elif name in self.default_properties:
			properties = self.default_properties
		else:
			logger.warning("subdomain {} does not contain property {}".format(self.subdomain, name))
			return 

		if '_range' in name:
			assert type(properties[name]) == type(value) and len(properties[name]) == len(value), "Incorrect format: expected {} of length {} but got {} of length {}".format(type(properties[name]), len(properties[name]), type(value), len(value))
			self.properties[name] = value
		else:
			assert type(properties[name]) == type(value) , "Incorrect type: expected {} got {}".format(type(properties[name]), type(value))
			self.properties[name] = value

	def get_property(self, name):
		if name not in self.properties:
			logger.warning("subdomain {} does not contain property {}".format(self.subdomain, name))
			return
		return self.properties[name]
