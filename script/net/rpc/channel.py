#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


import google.protobuf.service as service

from net.rpc.codec import RpcCodec
from net.rpc.rpc_pb2 import RpcMessage, REQUEST, RESPONSE, ERROR
from net.rpc.controller import RpcController, ServiceSideController


class RpcChannel(service.RpcChannel):
	"""Abstract interface for an RPC channel. An RpcChannel represents a communication
	line to a Service which can be used to call that Service's methods.
	The Service may be running on another machine. Normally, you should not call an RpcChannel
	directly, but instead construct a stub Service wrapping it.
	"""
	def __init__(self, connection):
		self._conn = connection
		self._codec = RpcCodec(self._on_rpc_message)
		self._id = 0
		self._outstandings = {}  # id : OutStandingCall
		self._services = {}  # the ref from RpcServer
		self._context = None

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
			self._handle_response(message)
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
			controller = ServiceSideController(self)
			method_name = message.method
			method = service.DESCRIPTOR.FindMethodByName(method_name)
			request_class = service.GetRequestClass(method)
			request_inst = request_class()
			request_inst.ParseFromString(message.request)
			done = DoneCallback(self, message.id)
			service.CallMethod(method, controller, request_inst, done)
		else:
			raise RuntimeError('can not find service: {0}'.format(service_name))

	def _handle_response(self, message):
		message_id = message.id
		outstanding_call = self._outstandings.get(message_id, None)
		if outstanding_call:
			if outstanding_call.response_class:
				response_inst = outstanding_call.response_class()
				response_inst.ParseFromString(message.response)
				if outstanding_call.done_callback:
					outstanding_call.done_callback(response_inst)
			del self._outstandings[message_id]

	@property
	def services(self):
		return self._services

	@services.setter
	def services(self, value):
		self._services = value

	def send_message(self, message):
		self._codec.send(self._conn, message)

	@property
	def context(self):
		return self._context

	@context.setter
	def context(self, value):
		self._context = value


class OutstandingCall(object):
	def __init__(self, response_class, done_callback):
		self.response_class = response_class
		self.done_callback = done_callback


class DoneCallback(object):

	def __init__(self, channel, messageId):
		self._channel = channel
		self._messageId = messageId

	def __call__(self, response_inst):
		message = RpcMessage()
		message.type = RESPONSE
		message.id = self._messageId
		message.response = response_inst.SerializeToString()
		self._channel.send_message(message)



