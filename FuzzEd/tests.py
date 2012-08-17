from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
from nodes_config import NODE_TYPES
from FuzzEd.models.graph import Graph
from FuzzEd.models.node import Node
from FuzzEd.models.edge import Edge

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
		oldncount=Graph.objects.get(pk=self.graphid).nodes.count()
		parent=Node.objects.get(pk=5) # from fixture, gate for CPU components
		response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
							 {'parent':parent.pk, 'type':1, 'xcoord':10, 'ycoord':7},    # Basic event
							 **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 201)
		self.assertIn('Location', response)
		self.assertEqual(oldncount+1, Graph.objects.get(pk=self.graphid).nodes.count() )
		# test invalid parent ID
		response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
							 {'parent':-1, 'type':1, 'xcoord':10, 'ycoord':7},
							 **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 400)
		# Check invalid type
		response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
							 {'parent':parent.pk, 'type':9999, 'xcoord':10, 'ycoord':7},
							 **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 400)

	def testDeleteNode(self):
		response=self.c.delete('/api/graphs/%u/nodes/%u'%(self.graphid, 7),
		                       **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 204)
		#TODO: Check if really gone, including edge from 5

	def testRelocateNode(self):
		response=self.c.post('/api/graphs/%u/nodes/6'%self.graphid,
							{'parent':2, 'ycoord': 8, 'xcoord':10},	# OR gate for TOP event, from fixture
		                    **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 204)
		#TODO: Check if really done, including edge rearrangement

	def testPropertyChange(self):
		nodeid=Node.objects.filter(deleted=False)[0].pk
		response=self.c.post('/api/graphs/%u/nodes/%u'%(self.graphid, nodeid),
							{'key':'foo', 'val':'bar'},
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 204)
		#TODO: Check if really done

	def testMorphNode(self):
		morphid=Node.objects.filter(deleted=False)[0].pk
		response=self.c.post('/api/graphs/%u/nodes/%u'%(self.graphid, morphid),
							data={"type":"t"},
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 204)
		#TODO: Check if really done

	def testRedo(self):
		response=self.c.post('/api/graphs/%u/redos'%(self.graphid),
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 204)
		#TODO: Check if really done
					
	def testUndo(self):
		response=self.c.post('/api/graphs/%u/undos'%(self.graphid),
							**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 204)
		#TODO: Check if really done
				
	def testCreateGraph(self):
		response=self.c.post(	'/api/graphs',
								data={"type":1, "name":"Second graph"},
								**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 201)
		self.assertIn('Location', response)
		# test invalid type
		response=self.c.post(	'/api/graphs',
								data={"type":99999, "name":"Third graph"},
								**{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		self.assertEqual(response.status_code, 400)
		