#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

import google.protobuf.service as service


class RpcController(service.RpcController):
	"""An RpcController mediates a single method call."""
	pass


class ServiceSideController(RpcController):

	def __init__(self, channel):
		super(ServiceSideController, self).__init__()
		self.channel = channel