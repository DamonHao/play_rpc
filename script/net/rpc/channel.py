#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


import google.protobuf.service as service

from net.rpc.codec import RpcCodec
from net.rpc.rpc_pb2 import RpcMessage, REQUEST, RESPONSE, ERROR
from net.rpc.controller import RpcController


class RpcChannel(service.RpcChannel):
	"""Abstract interface for an RPC channel. An RpcChannel represents a communication
	line to a Service which can be used to call that Service's methods.
	The Service may be running on another machine. Normally, you should not call an RpcChannel
	directly, but instead construct a stub Service wrapping it.
	"""
	def __init__(self, connection, io_loop):
		self._conn = connection
		self._codec = RpcCodec(self._on_rpc_message)
		self._id = 0
		self._outstandings = {}  # id : OutStandingCall
		self._services = {}  # the ref from RpcServer
		self._io_loop = io_loop

	@property
	def on_message(self):
		return self._codec.on_message

	def _on_rpc_message(self, connection, message):
		"""
		:param message : RpcMessage
		"""
		if message.type == REQUEST:
			self._call_service_method(message)
		elif message.type == RESPONSE:
			pass
		elif message.type == ERROR:
			pass

	def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
		"""call the method of remote service"""
		message = RpcMessage()
		message.type = REQUEST
		message.id = self._id
		self._id += 1
		message.service = method_descriptor.containing_service.full_name
		message.method = method_descriptor.name
		message.request = request.SerializeToString()
		self._outstandings[message.id] = OutstandingCall(response_class, done)
		self._codec.send(self._conn, message)

	def _call_service_method(self, message):
		""":param message : RpcMessage"""
		service_name = message.service
		service = self._services.get(service_name, None)
		if service:
			controller = RpcController()
			method_name = message.method
			method = service.DESCRIPTOR.FindMethodByName(method_name)
			request_class = service.GetRequestClass(method)
			request_inst = request_class()
			request_inst.ParseFromString(message.request)
			done = DoneCallback(message.id)
			service.CallMethod(method, controller, request_inst, done)
		else:
			raise RuntimeError('can not find service: {0}'.format(service_name))

	def _handle_response(self, message):
		message_id = message.id
		outstanding_call = self._outstandings.get(message_id, None)
		if outstanding_call:
			if outstanding_call.response_type:
				response_inst = outstanding_call.response_type.ParseFromString(message.response)
				if outstanding_call.done_callback:
					outstanding_call.done_callback(response_inst)

	@property
	def services(self):
		return self._services

	@services.setter
	def services(self, value):
		self._services = value

	# def _done_callback(self, message_id, response_inst):
	# 	message = RpcMessage()
	# 	message.type = RESPONSE
	# 	message.id = message_id
	# 	message.response = response_inst.SerializeToString()
	# 	self._codec.send(self._conn, message)


class OutstandingCall(object):
	def __init__(self, response_type, done_callback):
		self.response_type = response_type
		self.done_callback = done_callback


class DoneCallback(object):

	def __init__(self, messageId):
		self._messageId = messageId

	def __call__(self, response_ins=None):
		print "DoneCallback", self._messageId