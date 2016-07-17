#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
__author__ = 'damonhao'

import select
from net.io_loop import EnhancedPollIoLoop


class EPollIOLoop(EnhancedPollIoLoop):
	def initialize(self, **kwargs):
			super(EPollIOLoop, self).initialize(impl=select.epoll(), **kwargs)