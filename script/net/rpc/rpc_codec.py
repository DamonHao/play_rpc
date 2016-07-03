#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from net.buffer import Buffer
from net.rpc.rpc_pb2 import RpcMessage

HEADER_LEN = 4


class RpcCodec(object):

	def __init__(self, message_callback):
		""":param message_callback: (connection, RpcMessage)"""
		self._message_cb = message_callback

	def on_message(self, connection, read_buffer):
		while read_buffer.readable_bytes() >= HEADER_LEN:
			byte_size = read_buffer.peekInt32()
			if byte_size >= 65536 or byte_size < 0:
				print "invalid content len", byte_size
				connection.shut_down()
				break
			elif read_buffer.readable_bytes() >= byte_size + HEADER_LEN:
				read_buffer.retrieve(HEADER_LEN)
				content = read_buffer.retrieve(byte_size)
				message = RpcMessage.ParseFromString(content)
				self._message_callback(connection, message)
			else:
				break

	def send(self, connection, message):
		""":param message: RpcMessage
		"""
		buffer = Buffer()
		message_byte = message.SerializeToString()
		byte_size = len(message_byte)
		buffer.prepend(byte_size)
		buffer.append(message_byte)
		connection.send(buffer)