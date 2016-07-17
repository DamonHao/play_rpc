#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'damonhao'

from tornado.platform import select

from net.io_loop import EnhancedPollIoLoop


class SelectIOLoop(EnhancedPollIoLoop):
	def initialize(self, **kwargs):
			super(SelectIOLoop, self).initialize(impl=select._Select(), **kwargs)