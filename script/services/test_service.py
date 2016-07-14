#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from net.rpc import Rpc, RpcService
import helloworld_pb2
from tornado import gen


class GreeterImp(RpcService, helloworld_pb2.Greeter):

	def __init__(self, io_loop):
		super(GreeterImp, self).__init__(io_loop)

	@Rpc
	def SayHello(self, request):
		name = request.name
		response = helloworld_pb2.HelloReply()
		response.message = "Hello: " + name
		print 'SayHello', response.message
		return response

	@Rpc
	@gen.coroutine
	def SayHelloWithCoroutine(self, request):
		name = request.name
		response = helloworld_pb2.HelloReply()
		response.message = "Hello: " + name
		print 'SayHello', response.message
		yield gen.sleep(2)
		raise gen.Return(response)