from django.test import TestCase
from django.test.client import Client
from FuzzEd.models.graph import Graph
from FuzzEd.models.node import Node

class ApiTestCase(TestCase):
    fixtures = ['test_data.json']
    graphid=1       # from fixture 
    nodeid='99'     # from fixture
    node2id='4711'

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



    # def testGetRedos(self):
    #     response=self.c.get('/api/graphs/%u/redos'%self.graphid,
    #                         **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    #     self.assertEqual(response.status_code, 200)

    # def testGetUndos(self):
    #     response=self.c.get('/api/graphs/%u/undos'%self.graphid,
    #                         **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    #     self.assertEqual(response.status_code, 200)

    def testCreateNode(self):
        oldncount=Graph.objects.get(pk=self.graphid).nodes.count()
        parent=Node.objects.get(pk=5) # from fixture, gate for CPU components
        response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
                             {'parent':parent.pk, 'kind': 'orGate', 'id':self.nodeid, 'x':10, 'y':7},    # Basic event
                             **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response)
        self.assertEqual(oldncount+1, Graph.objects.get(pk=self.graphid).nodes.count() )
        # test invalid parent ID
        response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
                             {'parent':-1, 'kind': 'orGate', 'xcoord':10, 'ycoord':7},
                             **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 400)
        # Check invalid type
        response=self.c.post('/api/graphs/%u/nodes'%self.graphid,
                             {'parent':parent.pk, 'kind': 'fooVar', 'xcoord':10, 'ycoord':7},
                             **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 400)

    def testDeleteNode(self):
        response=self.c.delete('/api/graphs/%u/nodes/%s'%(self.graphid, self.nodeid),
                               **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really gone, including edge 

    def testRelocateNode(self):
        response=self.c.post('/api/graphs/%u/nodes/%s'%(self.graphid, self.nodeid),
                            {'parent':self.node2id, 'ycoord': 8, 'xcoord':10}, # OR gate for TOP event, from fixture
                            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really done, including edge rearrangement

    def testPropertyChange(self):
        response=self.c.post('/api/graphs/%u/nodes/%s'%(self.graphid, self.nodeid),
                            {'key':'foo', 'value':'bar'},
                            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really done

    def testMorphNode(self):
        response=self.c.post('/api/graphs/%u/nodes/%s'%(self.graphid, self.nodeid),
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
        response=self.c.post(   '/api/graphs',
                                data={"kind": "fuzztree", "name":"Second graph"},
                                **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Location', response)
        # test invalid type
        response=self.c.post(   '/api/graphs',
                                data={"kind": "foo", "name":"Third graph"},
                                **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 400)

    def testCutSet(self):
        response=self.c.get('/api/graphs/%u/cutsets'%self.graphid,
                            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('[{"nodes": [88, 12345]}, {"nodes": [99, 12345]}]', response.content)


        