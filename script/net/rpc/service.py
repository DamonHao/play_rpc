#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


class RpcService(object):

	@property
	def name(self):
		"""___service_interface__ is set by decorator ServiceInterface"""
		return repr(self.___service_interface_cls__)

	def server(self):
		"""a server stub"""
		pass

	def ownClient(self):
		pass

	def otherClients(self):
		pass

	def allClients(self):
		pass


class Stub(object):
	pass