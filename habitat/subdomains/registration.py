#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from habitat.core.logging import logger
from habitat.core.registry import registry
from habitat.subdomains import light_subdomain


def make_subdomain(id_subomain, *args, **kwargs):
	logger.info("intializing subdomain {}".format(id_subomain))
	_subdomain = registry.get_subdomain(id_subomain)
	print(_subdomain)
	assert _subdomain is not None, "Could not find subdomain with name {}".format(id_subomain)
	return _subdomain(**kwargs)
