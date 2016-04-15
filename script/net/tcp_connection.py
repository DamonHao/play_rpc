#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from collections import deque
from struct import unpack, pack

from tornado.iostream import _merge_prefix


class TcpConnection(object):

	def __init__(self, iostream, peer_addr):
		"""although iostream has read buffer, but provide a buffer object
		is more helpful for upper logic
		:param
		peer_addr (host, prot)
		"""
		self._iostream = iostream
		self._read_buffer = Buffer()
		self._peer_addr = peer_addr
		self._connection_cb = None
		self._write_complete_cb = None
		self._message_cb = None
		self._iostream.read_until_close(streaming_callback=self._on_message)
		self._is_connected = True

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


INT32_SIZE = 4


class Buffer(object):

	def __init__(self):
		self._buffer = deque()
		self._buffer_size = 0

	def append(self, data):
		self._buffer.append(data)
		self._buffer_size += len(data)

	def retrieve(self, len):
		if len == 0:
			return b''
		_merge_prefix(self._buffer, len)
		self._buffer_size -= len
		return self._buffer.popleft()

	def readable_bytes(self):
		return self._buffer_size

	def peekInt32(self):
		assert self._buffer_size >= INT32_SIZE
		need_chunk_index = 0
		sum_chunk_size = 0
		for chunk in self._buffer:
			sum_chunk_size += len(chunk)
			if sum_chunk_size >= INT32_SIZE:
				break
			need_chunk_index += 1
		if need_chunk_index > 0:
			_merge_prefix(self._buffer, sum_chunk_size)
		return unpack('i', self._buffer[0][:INT32_SIZE])[0]

	def retrieve_all(self):
		return self.retrieve(self._buffer_size)

	def prepend(self, byte_size):
		self._buffer.append(pack('i', byte_size))