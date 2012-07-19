import json
import copy
import collections
import os

from django.core.exceptions import MiddlewareNotUsed

from fuzztrees.config.fuzztree import FUZZTREE_CONFIG
from fuzztrees.config.faulttree import FAULTTREE_CONFIG

class Generator(object):
	def __init__(self, config):
		self.config = copy.deepcopy(config)
		self.__flat__()

	def __flat__(self):
		for node_type, node in self.config['nodes'].items():
			self.__resolve_inheritance__(node_type, node)

	def __resolve_inheritance__(self, node_type, node):
		if ('inherits' in node):
			# resolve parent inheritance
			parent_type = node['inherits']
			parent      = self.config['nodes'][parent_type]
			parent      = self.__resolve_inheritance__(parent_type, parent)
			del node['inherits']

			# merge parent and node
			merged_node = self.__merge__(parent, node)
			self.config['nodes'][node_type] = merged_node

			# return merged node
			return merged_node

		else:
			return node

	def __merge__(self, parent, node):
		merged = copy.deepcopy(parent)
		for key, value in node.iteritems():
			if isinstance(value, collections.Mapping):
				merged[key] = self.__merge__(parent.get(key, {}), value)
			else:
				merged[key] = node[key]
		return merged

	def generate(self, name):
		path = os.getcwd() + '/fuzztrees/static/config/' + name
		handle = open(path, 'w')
		handle.write(json.dumps(self.config))
		handle.close()

class ConfigGenerator:
	def __init__(self):
		Generator(FUZZTREE_CONFIG).generate('fuzztree.json')
		Generator(FAULTTREE_CONFIG).generate('faulttree.json')

		raise MiddlewareNotUsed()
