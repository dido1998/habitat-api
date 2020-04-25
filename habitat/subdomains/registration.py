#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from habitat.core.logging import logger
from habitat.core.registry import registry
from habitat.subdomains.light_subdomain import LightSubdomain
from habitat.subdomains.agent_subdomain import AgentSubdomain
from habitat.subdomains.action_space_subdomain import ActionSpaceSubdomain
from habitat.subdomains.sensor_subdomain import SensorSubdomain
from habitat.subdomains.object_subdomain import ObjectSubdomain


def make_subdomain(id_subomain, *args, **kwargs):
	logger.info("intializing subdomain {}".format(id_subomain))
	_subdomain = registry.get_subdomain(id_subomain)
	print(_subdomain)
	assert _subdomain is not None, "Could not find subdomain with name {}".format(id_subomain)
	return _subdomain(**kwargs)
