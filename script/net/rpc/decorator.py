#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from google.protobuf.empty_pb2 import Empty
from tornado.concurrent import Future


def Rpc(service_func):
	""" The Adapter between protobuf service method and user implemented service method.
	The later is more friendly and pythonic.
	if combine with coroutine decorator, it should come after the coroutine's, for example
	@Rpc
	@gen.coroutine
	def service_func(request)
	:param service_func: service_func(request)
	"""
	def wrapper(self, controller, request, done):
		response = service_func(self, request)
		if isinstance(response, Future):
			self.io_loop.add_future(response, lambda future: done(future.result()))
		else:
			if request is None:
				response = Empty()
			done(response)

	return wrapper


