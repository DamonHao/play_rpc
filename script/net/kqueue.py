#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from tornado.platform import kqueue

from net.io_loop import EnhancedPollIoLoop


class KQueueIOLoop(EnhancedPollIoLoop):
	def initialize(self, **kwargs):
			super(KQueueIOLoop, self).initialize(impl=kqueue._KQueue(), **kwargs)