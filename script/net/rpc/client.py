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


def test_stub(rpcClient):
	from net.rpc import stub_factory
	from services import helloworld_pb2
	print "test_stub", rpcClient
	channel = rpcClient._client.connection.context
	stub = stub_factory(helloworld_pb2.Greeter_Stub, channel)
	request = helloworld_pb2.HelloRequest()
	request.name = "haha"
	stub.SayHello(request)


if __name__ == '__main__':
	netAddress = NetAddress('127.0.0.1', 8002)
	io_loop_inst = ioloop.IOLoop.instance()
	client = RpcClient(io_loop_inst, netAddress)
	io_loop_inst.call_later(1, test_stub, client)
	client.connect()


