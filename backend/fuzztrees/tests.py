from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from fuzztrees.models import Graph, Node, Edge

class ApiTestCase(unittest.TestCase):
	graphid=1		# from fixture in initial_data.json

	def setUp(self):
		self.c=Client()
		self.c.login(username='testadmin', password='testadmin')

	def testGetGraph(self):
		response=self.c.get('/api/graphs/%u'%self.graphid,
		                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		response=self.c.get('/api/graphs/9999',
		                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 404)

	def testGetRedos(self):
		response=self.c.get('/api/graphs/%u/redos'%self.graphid,
		                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)

	def testGetUndos(self):
		response=self.c.get('/api/graphs/%u/undos'%self.graphid,
		                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)

	def testCreateNode(self):
		parentid=Node.objects.all()[0].pk
		response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
							 {'parent':parentid, 'type':'foo'},
							 **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		# test invalid parent ID
		response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
							 {'parent':-1, 'type':'foo'},
							 **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 400)
		#TODO: Check invalid type

	def testDeleteNode(self):
		delid=Node.objects.all()[0].pk
		response=self.c.delete('/api/graphs/%u/nodes/%u'%(self.graphid, delid),
		                       **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		#TODO: Check if really gone

	def testRelocateNode(self):
		node1id=Node.objects.all()[0].pk
		node2id=Node.objects.all()[1].pk
		response=self.c.put('/api/graphs/%u/nodes/%u'%(self.graphid, node1id),
							{'parent':node2id},
		                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		#TODO: Check if really done

	def testPropertyChange(self):
		nodeid=Node.objects.all()[0].pk
		response=self.c.put('/api/graphs/%u/nodes/%u'%(self.graphid, nodeid),
							{'key':'foo', 'val':'bar'},
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		#TODO: Check if really done

	def testMorphNode(self):
		morphid=Node.objects.all()[0].pk
		response=self.c.put('/api/graphs/%u/nodes/%u'%(self.graphid, morphid),
							data={'type':'t'},
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		#TODO: Check if really done

	def testRedo(self):
		response=self.c.post('/api/graphs/%u/redos'%(self.graphid),
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		#TODO: Check if really done
					
	def testUndo(self):
		response=self.c.post('/api/graphs/%u/undos'%(self.graphid),
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 200)
		#TODO: Check if really done
				
				
		
		