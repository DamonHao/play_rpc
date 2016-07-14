#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from channel import RpcChannel


class RpcBase(object):

	def __init__(self):
		self._services = {}  # service name: service

	def _on_connection(self, connection):
		print "[RpcBase]_on_connection", connection.name, connection.is_connected
		if connection.is_connected:
			channel = RpcChannel(connection, self._inner_mgr.io_loop)
			channel.services = self._services
			connection.set_message_callback(channel.on_message)
			connection.context = channel
		else:
			connection.context = None

	def register_service(self, service):
		self._services[service.GetDescriptor().full_name] = service

	@property
	def _inner_mgr(self):
		raise NotImplementedError()

	@property
	def io_loop(self):
		return self._inner_mgr.io_loop

