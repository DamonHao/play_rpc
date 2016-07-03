#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from tornado import ioloop

from tcp_server import TcpServer
from codec import LengthHeaderCodec


class RpcServer(object):

	def __init__(self, io_loop=None):
		self._server = TcpServer(io_loop)
		self._codec = LengthHeaderCodec(self._on_message)
		self._server.set_message_callback(self._codec.on_message)
		self._server.set_connection_callback(self._on_connection)

	def _on_message(self, conn, message):
		print "[RPCServer]_on_message", conn.name, message
		pass

	def _on_connection(self, conn):
		print "[RPCServer]_on_connection", conn.name, conn.is_connected

	def listen(self, port, ip=""):
		self._server.listen(port, ip)

	def register_service(self, service):
		pass


if __name__ == '__main__':
	server = RpcServer()
	server.listen(8002)
	ioloop.IOLoop.instance().start()

