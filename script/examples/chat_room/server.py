#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

from net.rpc import *
from net import IOLoop
from chat_room_pb2 import *


class ChatServerImp(RpcService, ChatServer):

	def __init__(self):
		self._token = 0
		self._users = {}  # token : user
		self._login_account = set([])

	def get_new_token(self):
		token = self._token
		self._token += 1
		return token

	@Rpc
	def Login(self, request, controller):
		print "Svr Login"
		reply = LoginReply()
		if request.account in self._login_account:
			reply.state = LoginReply.ALREADY_LOGIN
			return reply
		reply.state = LoginReply.OK
		token = self.get_new_token()
		reply.token = token

		channel = controller.channel
		channel.context = token
		self.service_mgr.channel_down_event += self._lost_connect
		chat_client_stub = stub_factory(ChatClient_Stub, channel)

		self._users[token] = User(request.account, chat_client_stub)
		self._login_account.add(request.account)

		print "Svr Login succeed", request.account
		return reply

	@Rpc
	def Logout(self, request, controller):
		reply = LogoutReply()
		reply.state = self._logout(request.token)
		return reply

	@Rpc
	def Speak(self, request, controller):
		speaker_token = request.token
		speaker = self._users.get(speaker_token, None)
		if not speaker:
			return
		for token, user in self._users.iteritems():
			if token != speaker_token:
				receive_world_req = ReceiveWorldRequest()
				receive_world_req.account = speaker.account
				receive_world_req.content = request.content
				self.io_loop.spawn_callback(user.chat_stub.ReceiveWord, receive_world_req)

		reply = SpeakReply()
		reply.state = OK
		return reply

	def _lost_connect(self, channel):
		token = channel.context
		self._logout(token)

	def _logout(self, token):
		user = self._users.get(token, None)
		if not user:
			return ERROR
		print "user: {0} logout".format(user.account)
		del self._users[token]
		self._login_account.remove(user.account)
		return OK


class User(object):

	def __init__(self, account, chat_client_stub):
		self.account = account
		self.chat_stub = chat_client_stub

if __name__ == '__main__':
		io_loop = IOLoop()
		server = RpcServer(io_loop)
		server.register_service(ChatServerImp())
		server.listen(8002)
		print "chat svr start"
		server.start()