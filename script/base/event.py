#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'damonhao'


class Event(object):
	def __init__(self):
		self.listeners = []

	def __call__(self, *args, **kwargs):
		for l in self.listeners:
			l(*args, **kwargs)

	def __iadd__(self, listener):
		self.listeners.append(listener)
		return self

	def __isub__(self, listener):
		try:
			self.listeners.remove(listener)
		except ValueError:
			pass
		return self
