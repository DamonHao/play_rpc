#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

import weakref

from stub import stub_factory


class RpcService(object):
	"""support common service function"""

	def __init__(self):
		self._service_mgr = None

	@property
	def service_mgr(self):
		return self._service_mgr

	def init_on_register(self, service_mgr):
		self._service_mgr = weakref.proxy(service_mgr)

	def create_stub(self, service_stub_class, channel):
		return stub_factory(service_stub_class, channel)