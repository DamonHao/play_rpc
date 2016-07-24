#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'

import weakref
from PyQt4 import uic
from PyQt4.QtGui import *
from PyQt4.QtCore import QString, QTimer,SIGNAL

from net import *
from net.rpc import *

from chat_room_pb2 import *


class MainWindow(QMainWindow):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		uic.loadUi('./guis/main.ui', self)
		self.centerOnScreen()
		self.sendBtn.clicked.connect(self._sendBtnClick)
		self.loginBtn.clicked.connect(self._loginBtnClick)
		self.stateLabel.setText(UserState.OFFLINE)

		io_loop = IOLoop()
		io_loop.prepare()
		self._io_loop = io_loop
		netAddress = NetAddress('127.0.0.1', 8002)
		client = RpcClient(io_loop, netAddress)
		client.channel_up_event += self._channel_up
		client.register_service(ChatClientImp(self))
		client.connect()
		self._client = client

		timer = QTimer()
		timer.connect(timer, SIGNAL("timeout()"), self._handle_network)
		timer.start(0)
		self._network_timer = timer

		self._user_token = None
		self._account = None
		self._is_login = False

	def centerOnScreen(self):
		"""centerOnScreen() Centers the window on the screen"""
		resolution = QDesktopWidget().screenGeometry()
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
		(resolution.height() / 2) - (self.frameSize().height()/2))

	def _handle_network(self):
		self._io_loop.one_loop()

	def _channel_up(self, channel):
		self._chat_stub = self._client.create_stub(ChatServer_Stub)

	def _loginBtnClick(self):
		if self._is_login:
			self._io_loop.spawn_callback(self._logout)
		else:
			self._io_loop.spawn_callback(self._login)

	@gen.coroutine
	def _login(self):
		account = self.accountLineEdit.displayText()
		password = self.passwordLineEdit.displayText()
		request = LoginRequest()
		request.account = account.toUtf8().data()
		request.password = password.toUtf8().data()
		reply = yield self._chat_stub.Login(request)
		if reply.state == LoginReply.OK:
			print "login succeed", account, password
			self._is_login = True
			self._user_token = reply.token
			self._account = account
			self.stateLabel.setText(UserState.ONLINE)
			self.loginBtn.setText(LOGOUT_TEXT)
		else:
			print "login error", reply.state

	@gen.coroutine
	def _logout(self):
		request = LogoutRequest()
		request.token = self._user_token
		reply = yield self._chat_stub.Logout(request)
		self._is_login = False
		self._clear_user_data()

	def _clear_user_data(self):
		self._user_token = None
		self._account = None
		self.userTextEdit.clear()
		self.chatTextBrowser.clear()
		self.accountLineEdit.clear()
		self.passwordLineEdit.clear()
		self.loginBtn.setText(LOGIN_TEXT)

	def _sendBtnClick(self):
		if not self._is_login:
			return
		input_text = self.userTextEdit.toPlainText()
		if input_text.isEmpty():
			return
		self._io_loop.spawn_callback(self._speak, input_text)

	@gen.coroutine
	def _speak(self, content):
		request = SpeakRequest()
		request.token = self._user_token
		request.content = content.toUtf8().data()
		reply = yield self._chat_stub.Speak(request)
		if reply.state == OK:
			print "speak succeed"
			self.userTextEdit.clear()
			self.show_word(self._account, content)
		else:
			print "speak error"

	def show_word(self, speaker_name, content):
		self.chatTextBrowser.append(speaker_name + ':')
		self.chatTextBrowser.append(content)


class ChatClientImp(RpcService, ChatClient):

	def __init__(self, ui_widget):
		self.ui_widget = weakref.proxy(ui_widget)

	@Rpc
	def ReceiveWord(self, request, controller):
		self.ui_widget.show_word(request.account, request.content)
		reply = ReceiveWorldReply()
		reply.state = OK
		return reply


class UserState(object):
	ONLINE = "State: Online"
	OFFLINE = "State: Offline"

LOGIN_TEXT = 'Login'
LOGOUT_TEXT = 'Logout'


if __name__ == '__main__':
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	app.exec_()
	app.deleteLater()