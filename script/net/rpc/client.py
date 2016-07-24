#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from tornado import ioloop, gen

from net import TcpClient, NetAddress
from common import RpcBase
from stub import stub_factory


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

	def create_stub(self, service_stub_class):
		channel = self._client.connection.context
		assert channel, "there is not valid channel"
		return stub_factory(service_stub_class, channel)


@gen.coroutine
def test_stub(rpcClient):
	from services import helloworld_pb2
	stub = rpcClient.create_stub(helloworld_pb2.GreeterServer_Stub)
	request = helloworld_pb2.HelloRequest()
	request.name = "Client"
	response = yield stub.SayHello(request)
	# response = yield stub.SayHelloWithCoroutine(request)
	print "receive: ", response.message


def test_one_loop():
	netAddress = NetAddress('127.0.0.1', 8002)
	from net.io_loop import IOLoop
	io_loop = IOLoop()
	io_loop.prepare()
	client = RpcClient(io_loop, netAddress)
	from services.test_service import GreeterClientImp
	client.register_service(GreeterClientImp())
	io_loop.call_later(1, test_stub, client)
	client.connect()
	while True:
		io_loop.one_loop(2)


if __name__ == '__main__':
	# netAddress = NetAddress('127.0.0.1', 8002)
	# # io_loop = ioloop.IOLoop.instance()
	# from net.io_loop import IOLoop
	# io_loop = IOLoop()
	# client = RpcClient(io_loop, netAddress)
	# from services.test_service import GreeterClientImp
	# client.register_service(GreeterClientImp())
	# io_loop.call_later(1, test_stub, client)
	# client.connect()
	# io_loop.start()
	test_one_loop()

