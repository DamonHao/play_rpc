#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from base import Event
from channel import RpcChannel


class RpcBase(object):

	def __init__(self):
		self._services = {}  # service name: service
		self.channel_up_event = Event()  # Event(channel)
		self.channel_down_event = Event()  # Event(channel)

	def _on_connection(self, connection):
		print "connection:{0} is connected:{1}".format(connection.name, connection.is_connected)
		if connection.is_connected:
			channel = RpcChannel(connection)
			channel.services = self._services
			connection.set_message_callback(channel.on_message)
			connection.context = channel
			self.channel_up_event(channel)
		else:
			self.channel_down_event(connection.context)
			connection.context = None

	def register_service(self, service):
		service.init_on_register(self)
		self._services[service.GetDescriptor().full_name] = service

	@property
	def _inner_mgr(self):
		raise NotImplementedError()

	@property
	def io_loop(self):
		return self._inner_mgr.io_loop

