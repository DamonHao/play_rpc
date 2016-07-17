#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from tornado.tcpclient import TCPClient as TornadoTCPClient
from tornado import gen, ioloop

from tcp_connection import TcpConnection


class TcpClient(object):

	def __init__(self, io_loop, netAddress):
		self._client = TornadoTCPClient(io_loop=io_loop)
		self._connection_cb = None
		self._write_complete_cb = None
		self._message_cb = None
		self._conn = None
		self._netAddress = netAddress

	@gen.coroutine
	def _connect(self, host, port):
		iostream = yield self._client.connect(host, port)
		conn = TcpConnection(self.io_loop, iostream, (host, port))
		conn.set_connection_callback(self._connection_cb)
		conn.set_message_callback(self._message_cb)
		conn.set_write_complete_callback(self._write_complete_cb)
		conn.set_close_callback(self._remove_connection)
		conn.connect_established()
		self._conn = conn

	def connect(self):
		netAddress = self._netAddress
		io_loop = self._client.io_loop
		io_loop.run_sync(lambda: self._connect(netAddress.address, netAddress.port))
		io_loop.start()

	def set_connection_callback(self, callback):
		""":param callback:(connection)"""
		self._connection_cb = callback

	def set_message_callback(self, callback):
		""":param callback:(connection, buffer)"""
		self._message_cb = callback

	def set_write_complete_callback(self, callback):
		self._write_complete_cb = callback

	def _remove_connection(self, conn):
		conn.connect_destroyed()

	@property
	def io_loop(self):
		self._client.io_loop

	@property
	def connection(self):
		return self._conn

def on_connection(conn):
	if conn.is_connected:
		print "on_connection"
	else:
		print "disconnected"


if __name__ == '__main__':
	from net import NetAddress
	netAddress = NetAddress('127.0.0.1', 8002)
	client = TcpClient(ioloop.IOLoop.instance(), netAddress)
	client.set_connection_callback(on_connection)
	client.connect()

