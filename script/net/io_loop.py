#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
__author__ = 'damonhao'


import signal
import select
import heapq
import errno

from tornado.ioloop import PollIOLoop
from tornado.util import PY3, errno_from_exception, Configurable

if PY3:
	import _thread as thread
else:
	import thread


class EnhancedPollIoLoop(PollIOLoop):

	@classmethod
	def configurable_base(cls):
		return EnhancedPollIoLoop

	@classmethod
	def configurable_default(cls):
			if hasattr(select, "epoll"):
				from net.epoll import EPollIOLoop
				return EPollIOLoop
			if hasattr(select, "kqueue"):
				# Python 2.6+ on BSD or Mac
				from net.kqueue import KQueueIOLoop
				return KQueueIOLoop
			from net.select import SelectIOLoop
			return SelectIOLoop

	def initialize(self, **kwargs):
		super(EnhancedPollIoLoop, self).initialize(**kwargs)
		self._isNotReady = True

	def prepare(self):
		self._isNotReady = False
		if self._running:
			raise RuntimeError("IOLoop is already running")
		self._setup_logging()
		if self._stopped:
			self._stopped = False
			return
		# old_current = getattr(IOLoop._current, "instance", None)
		# IOLoop._current.instance = self
		self._thread_ident = thread.get_ident()
		self._running = True

	def one_loop(self, default_time_out=0):
		if self._isNotReady:
			raise RuntimeError("IoLoop is not prepared!")
		try:
			with self._callback_lock:
					callbacks = self._callbacks
					self._callbacks = []

			due_timeouts = []
			if self._timeouts:
				now = self.time()
				while self._timeouts:
					if self._timeouts[0].callback is None:
						# The timeout was cancelled.  Note that the
						# cancellation check is repeated below for timeouts
						# that are cancelled by another timeout or callback.
						heapq.heappop(self._timeouts)
						self._cancellations -= 1
					elif self._timeouts[0].deadline <= now:
						due_timeouts.append(heapq.heappop(self._timeouts))
					else:
						break
				if (self._cancellations > 512
							and self._cancellations > (len(self._timeouts) >> 1)):
					# Clean up the timeout queue when it gets large and it's
					# more than half cancellations.
					self._cancellations = 0
					self._timeouts = [x for x in self._timeouts
														if x.callback is not None]
					heapq.heapify(self._timeouts)

			for callback in callbacks:
				self._run_callback(callback)
			for timeout in due_timeouts:
				if timeout.callback is not None:
						self._run_callback(timeout.callback)
			# Closures may be holding on to a lot of memory, so allow
			# them to be freed before we go into our poll wait.
			callbacks = callback = due_timeouts = timeout = None

			if self._callbacks:
				# If any callbacks or timeouts called add_callback,
				# we don't want to wait in poll() before we run them.
				poll_timeout = 0.0
			elif self._timeouts:
				# If there are any timeouts, schedule the first one.
				# Use self.time() instead of 'now' to account for time
				# spent running callbacks.
				poll_timeout = self._timeouts[0].deadline - self.time()
				poll_timeout = max(0, min(poll_timeout, default_time_out))
			else:
				# No timeouts and no callbacks, so use the default.
				poll_timeout = default_time_out
			# if not self._running:
			# 	break
			if self._blocking_signal_threshold is not None:
				# clear alarm so it doesn't fire while poll is waiting for
				# events.
				signal.setitimer(signal.ITIMER_REAL, 0, 0)

			try:
				event_pairs = self._impl.poll(poll_timeout)
			except Exception as e:
				# Depending on python version and IOLoop implementation,
				# different exception types may be thrown and there are
				# two ways EINTR might be signaled:
				# * e.errno == errno.EINTR
				# * e.args is like (errno.EINTR, 'Interrupted system call')
				if errno_from_exception(e) == errno.EINTR:
					return
				else:
					raise

			if self._blocking_signal_threshold is not None:
				signal.setitimer(signal.ITIMER_REAL, self._blocking_signal_threshold, 0)

			# Pop one fd at a time from the set of pending fds and run
			# its handler. Since that handler may perform actions on
			# other file descriptors, there may be reentrant calls to
			# this IOLoop that modify self._events
			self._events.update(event_pairs)
			while self._events:
				fd, events = self._events.popitem()
				try:
					fd_obj, handler_func = self._handlers[fd]
					handler_func(fd_obj, events)
				except (OSError, IOError) as e:
					if errno_from_exception(e) == errno.EPIPE:
						# Happens when the client closes the connection
						pass
					else:
						self.handle_callback_exception(self._handlers.get(fd))
				except Exception:
					self.handle_callback_exception(self._handlers.get(fd))
			fd_obj = handler_func = None

		finally:
			# reset the stopped flag so another start/stop pair can be issued
			self._stopped = False
			if self._blocking_signal_threshold is not None:
					signal.setitimer(signal.ITIMER_REAL, 0, 0)


IOLoop = EnhancedPollIoLoop
