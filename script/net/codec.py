#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


HEADER_LEN = 4

from net.tcp_connection import Buffer


class LengthHeaderCodec(object):

	def __init__(self, message_callback):
		self._message_callback = message_callback

	def on_message(self, connection, read_buffer):
		while read_buffer.readable_bytes() >= HEADER_LEN:
			byte_size = read_buffer.peekInt32()
			if byte_size >= 65536 or byte_size < 0:
				print "invalid content len"
				connection.shut_down()
				break
			elif read_buffer.readable_bytes() >= byte_size + HEADER_LEN:
				read_buffer.retrieve(HEADER_LEN)
				content = read_buffer.retrieve(byte_size)
				self._message_callback(connection, content)
			else:
				break

	def send(self, connection, message):
		buffer = Buffer()
		byte_size = len(message)
		buffer.prepend(byte_size)
		buffer.append(message)
		connection.send(buffer)

