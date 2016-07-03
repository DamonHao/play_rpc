#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

import types

import google.protobuf.service as service

from net.rpc.rpc_codec import RpcCodec
from net.rpc.rpc_pb2 import RpcMessage, REQUEST, RESPONSE, ERROR


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
		:param
		message : RpcMessage
		"""
		if message.type == REQUEST:
			self._call_service_method(message)
		elif message.type == RESPONSE:
			pass
		elif message.type == ERROR:
			pass

	def call_method(self, method, request_inst, response_type=None, done_callback=None):
		"""call the method of remote service"""
		message = RpcMessage()
		message.type = REQUEST
		message.id = self._id
		self._id += 1
		message.service = method.service.name
		message.method = method.name
		message.request = request_inst.SerializeToString()
		self._outstandings[message.id] = OutstandingCall(response_type, done_callback)
		self._codec.send(self._conn, message)

	def _call_service_method(self, message):
		""":param message : RpcMessage"""
		service_name = message.service
		service = self._services.get(service_name, None)
		method_name = message.method
		if service:
			method = getattr(service, method_name)
			request_type = method.___request_type__
			request_inst = request_type.ParseFromString(message.request)
			# if isinstance(method, types.GeneratorType):
			# 	raise Exception()
			# else:
			# TODO support generator
			response_inst = method(request_inst)
			self._done_callback(message.id, response_inst)
		else:
			raise Exception('can not find service: {0}'.format(service_name))

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

	def _done_callback(self, message_id, response_inst):
		message = RpcMessage()
		message.type = RESPONSE
		message.id = message_id
		message.response = response_inst.SerializeToString()
		self._codec.send(self._conn, message)


class OutstandingCall(object):
	def __init__(self, response_type, done_callback):
		self.response_type = response_type
		self.done_callback = done_callback
