#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

import base_lib

from tornado.tcpclient import TCPClient as TrnadoTCPClient
from tornado import gen,ioloop

from tcp_connection import TcpConnection


class TCPClient(object):

	def __init__(self):
		self._client = TrnadoTCPClient()
		self._connection_cb = None
		self._write_complete_cb = None
		self._message_cb = None
		self._conn = None

	@gen.coroutine
	def connect(self, host, port):
		iostream = yield self._client.connect(host, port)
		conn = TcpConnection(iostream, (host, port))
		conn.set_connection_callback(self._connection_cb)
		conn.set_message_callback(self._message_cb)
		conn.set_write_complete_callback(self._write_complete_cb)
		conn.set_close_callback(self._remove_connection)
		conn.connect_established()
		self._conn = conn

	def set_connection_callback(self, callback):
		""":param
		callback:(connection)"""
		self._connection_cb = callback

	def set_message_callback(self, callback):
		""":param
		callback:(connection, buffer)"""
		self._message_cb = callback

	def set_write_complete_callback(self, callback):
		self._write_complete_cb = callback

	def _remove_connection(self, conn):
		conn.connect_destroyed()


def on_connection(conn):
	if conn.is_connected:
		print "on_connection"
	else:
		print "disconnected"


if __name__ == '__main__':
	client = TCPClient()
	client.set_connection_callback(on_connection)
	ioloop.IOLoop.instance().run_sync(lambda: client.connect('127.0.0.1', 8002))
	ioloop.IOLoop.instance().start()

