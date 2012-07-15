import json
import copy
import collections

from django.core.exceptions import MiddlewareNotUsed

from fuzztrees.config.fuzztree import FUZZTREE_CONFIG

class Generator(object):
	def __init__(self, config):
		self.config = copy.deepcopy(config)
		self.flat()

	def flat(self):
		for node_type, node in self.config['nodes'].items():
			self.__resolve_inheritance__(node_type, node)

	def __resolve_inheritance__(self, node_type, node):
		if ('inherits' in node):
			# resolve parent inheritance
			parent_type = node['inherits']
			parent      = self.config['nodes'][parent_type]
			self.__resolve_inheritance__(parent_type, parent)
			del node['inherits']

			# merge parent and node
			self.config['nodes'][node_type] = self.__merge__(parent, node)

			# return merged node
			return node

		else:
			return node

	def __merge__(self, parent, node):
		merged = {}
		for key, value in node.iteritems():
			if isinstance(value, collections.Mapping):
				merged[key] = self.__merge__(parent.get(key, {}), value)
			else:
				merged[key] = node[key]
		return merged

	def generate(self):
		print self.config

class ConfigGenerator:
	def __init__(self):
		Generator(FUZZTREE_CONFIG).generate()

		raise MiddlewareNotUsed()
