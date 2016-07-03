#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from collections import deque
from struct import unpack, pack

from tornado.iostream import _merge_prefix

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