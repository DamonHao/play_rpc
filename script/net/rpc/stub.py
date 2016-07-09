#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from net.rpc.controller import RpcController


def stub_factory(service_stub_class, channel):
	return _ServiceStub(service_stub_class, channel)
	pass


class _ServiceStub(object):

	def __init__(self, service_stub_class, channel):
		self._rawStub = service_stub_class(channel)
		self._channel = channel
		service_stub = self
		for method in service_stub_class.GetDescriptor().methods:
			rpc = lambda request: service_stub.__call_stub_method___(service_stub_class.__dict__[method.name], request)
			setattr(self, method.name, rpc)

	def __call_stub_method___(self, method, request):
		def done_callback():
			pass
		controller = RpcController()
		method(self._rawStub, controller, request, done_callback)
