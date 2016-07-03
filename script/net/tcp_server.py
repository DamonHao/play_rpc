#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


from tornado.tcpserver import TCPServer as TornadoTCPServer
from tornado import ioloop

from tcp_connection import TcpConnection


class TcpServer(TornadoTCPServer):

	def __init__(self, io_loop=None, ssl_options=None, max_buffer_size=None,
		read_chunk_size=None):
		super(TcpServer, self).__init__(io_loop, ssl_options, max_buffer_size, read_chunk_size)
		self._connections = {}  # ip_port: connection
		self._connection_cb = None
		self._message_cb = None
		self._write_complete_cb = None

	def handle_stream(self, stream, address):
		conn = TcpConnection(stream, address)
		self._connections[conn.name] = conn
		conn.set_connection_callback(self._connection_cb)
		conn.set_message_callback(self._message_cb)
		conn.set_write_complete_callback(self._write_complete_cb)
		conn.set_close_callback(self._remove_connection)
		conn.connect_established()

	def set_connection_callback(self, callback):
		self._connection_cb = callback

	def set_message_callback(self, callback):
		self._message_cb = callback

	def set_write_complete_callback(self, callback):
		self._write_complete_cb = callback

	def _remove_connection(self, conn):
		del self._connections[conn.name]
		print "_remove_connection, remain:", list(self._connections.iterkeys())
		conn.connect_destroyed()

	def run(self):
		self.io_loop.start()


def test_on_message(conn, buffer):
	print "receive", conn.name, buffer.retrieve_all()


if __name__ == '__main__':
	server = TcpServer(io_loop=ioloop.IOLoop.instance())
	server.set_message_callback(test_on_message)
	server.listen(8002)
	server.run()