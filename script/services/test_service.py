#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

import helloworld_pb2


class GreeterImp(helloworld_pb2.Greeter):

	def SayHello(self,controller,request, done):
		name = request.name
		response = helloworld_pb2.HelloReply()
		response.message = "Hello: " + name
		print 'SayHello', response.message
		done(response)
