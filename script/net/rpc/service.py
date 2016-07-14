#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


class RpcService(object):
	"""support common service function"""

	def __init__(self, io_loop):
		self.io_loop = io_loop