#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from buffer import Buffer


class TcpConnection(object):

	def __init__(self, io_loop, iostream, peer_addr):
		"""although iostream has read buffer, but provide a buffer object
		is more helpful for upper logic
		:param
		peer_addr (host, prot)
		"""
		self.io_loop = io_loop
		self._iostream = iostream
		self._read_buffer = Buffer()
		self._peer_addr = peer_addr
		self._connection_cb = None
		self._write_complete_cb = None
		self._message_cb = None
		self._iostream.read_until_close(streaming_callback=self._on_message)
		self._is_connected = True
		self._context = None

	def set_connection_callback(self, callback):
		self._connection_cb = callback

	def set_message_callback(self, callback):
		"""callback(connection, buffer)"""
		self._message_cb = callback

	def _on_message(self, data):
		self._read_buffer.append(data)
		if self._message_cb:
			self._message_cb(self, self._read_buffer)

	def set_write_complete_callback(self, callback):
		self._write_complete_cb = callback

	def set_close_callback(self, callback):
		self._iostream.set_close_callback(lambda: callback(self))

	def connect_established(self):
		print "connect_established", self.name
		if self._connection_cb:
			self._connection_cb(self)

	def send(self, buffer):
		self._iostream.write(buffer.retrieve_all(), self._write_complete_cb)

	def shut_down(self):
		self._iostream.close()

	@property
	def name(self):
		addr = self._peer_addr
		name = (addr[0], ':', str(addr[1]))
		return ''.join(name)

	def connect_destroyed(self):
		"""no need to call self._iostream.close()"""
		print "connect_destroyed", self.name
		self._is_connected = False
		if self._connection_cb:
			self._connection_cb(self)

	@property
	def is_connected(self):
		return self._is_connected

	@property
	def context(self):
		return self._context

	@context.setter
	def context(self, value):
		self._context = value