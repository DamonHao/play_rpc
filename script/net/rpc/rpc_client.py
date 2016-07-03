#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from tornado import ioloop

from net import TcpClient, NetAddress
from net.rpc import RpcBase


class RpcClient(RpcBase):
	def __init__(self, io_loop, netAddress):
		super(RpcClient, self).__init__()
		self._client = TcpClient(io_loop, netAddress)
		self._client.set_connection_callback(self._on_connection)
		self._services = {}  # service name: service

	def connect(self):
		self._client.connect()

	@property
	def _inner_mgr(self):
		return self._client


if __name__ == '__main__':
	from service.test_service import TestServiceClient
	netAddress = NetAddress('127.0.0.1', 8002)
	client = RpcClient(ioloop.IOLoop.instance(), netAddress)
	client.register_service(TestServiceClient())
	client.connect()
