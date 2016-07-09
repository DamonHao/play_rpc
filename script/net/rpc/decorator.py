#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from google.protobuf.empty_pb2 import Empty
from aenum import Enum


class RpcType(Enum):
	Command = 0
	Client = 1
	Server = 2


def CommandRpc(request_type=Empty, response_type=Empty):
	return _SetRpcSignature(RpcType.Command, request_type, response_type)


def ClientRpc(request_type=Empty, response_type=Empty):
	return _SetRpcSignature(RpcType.Client, request_type, response_type)


def ServerRpc(request_type=Empty, response_type=Empty):
	return _SetRpcSignature(RpcType.Server, request_type, response_type)


def _SetRpcSignature(rpc_type, request_type, response_type):
	def decorate_func(func):
		func.___rpc_type__ = rpc_type
		func.___request_type__ = request_type
		func.___response_type__ = response_type
		return func

	return decorate_func


def ServiceInterface(service_interface_cls):
	"""decorate the class that is the service interface"""
	def decorate_cls(child_cls):
		child_cls.___service_interface_cls__ = service_interface_cls
		return child_cls
	return decorate_cls
