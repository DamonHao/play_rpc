#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from net.rpc import Rpc, RpcService
import helloworld_pb2
from tornado import gen


class GreeterServerImp(RpcService, helloworld_pb2.GreeterServer):

	@Rpc
	def SayHello(self, request, controller):
		name = request.name
		response = helloworld_pb2.HelloReply()
		response.message = "Server Hello: " + name
		print 'Server', response.message
		self.GreetBack(controller.channel)
		return response

	@Rpc
	@gen.coroutine
	def SayHelloWithCoroutine(self, request, controller):
		name = request.name
		response = helloworld_pb2.HelloReply()
		response.message = "Hello: " + name
		print 'SayHello', response.message
		yield gen.sleep(2)
		raise gen.Return(response)

	@gen.coroutine
	def GreetBack(self, channel):
		from services import helloworld_pb2
		yield gen.sleep(2)
		print "GreetBack1"
		stub = self.create_stub(helloworld_pb2.GreeterClient_Stub, channel)
		request = helloworld_pb2.HelloRequest()
		request.name = "Server"
		response = yield stub.SayHello(request)
		print "receive: ", response.message


class GreeterClientImp(RpcService, helloworld_pb2.GreeterClient):

	@Rpc
	def SayHello(self, request, controller):
		name = request.name
		response = helloworld_pb2.HelloReply()
		response.message = "Client Hello: " + name
		print 'Client', response.message
		return response