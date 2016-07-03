#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from tornado import ioloop
from net import TcpServer
from net.rpc import RpcBase


class RpcServer(RpcBase):
	def __init__(self, io_loop):
		super(RpcServer, self).__init__()
		self._server = TcpServer(io_loop)
		self._server.set_connection_callback(self._on_connection)

	def listen(self, port, ip=""):
		self._server.listen(port, ip)

	def start(self):
		self._server.run()

	@property
	def _inner_mgr(self):
		return self._server

if __name__ == '__main__':
	from service.test_service import TestServiceServer
	server = RpcServer(ioloop.IOLoop.instance())
	server.register_service(TestServiceServer())
	server.listen(8002)
	server.start()








