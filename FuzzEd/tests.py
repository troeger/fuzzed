import json
from xml.dom import minidom
from django.test import TestCase
from django.test.client import Client
from FuzzEd.models.graph import Graph
from FuzzEd.models.node import Node

class FuzzTreesTestCase(TestCase):
    fixtures = ['test_data.json']
    """ This fixture tree looks like this, with pk and client_id per node:
        graph(1)
            topEvent (1, -2147483647)
                andGate (2, 4711)
                    basicEvent (3, 12345)
                    orGate (4, 222)
                        basicEvent (5, 88)
                        basicEvent (6, 99)

        The following edges are defined, with pk and client_id:
            1 / 65: 1->2
            2 / 66: 2->3
            3 / 77: 2->4
            4 / 88: 4->5
            5 / 99: 4->6
    """

    def setUp(self):
        self.c=Client()
        self.c.login(username='testadmin', password='testadmin')

    def ajaxGet(self, url):
        return self.c.get( url, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest' )

    def ajaxPost(self, url, data):
        return self.c.post( url, data, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest' )

    def ajaxPostNode(self, data):
        return self.ajaxPost('/api/graphs/1/nodes/88', {'properties': json.dumps(data)})

    def ajaxDelete(self, url):
        return self.c.delete( url, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest' )

class BasicApiTestCase(FuzzTreesTestCase):
    def testGetGraph(self):
        response=self.ajaxGet('/api/graphs/1')
        self.assertEqual(response.status_code, 200)
        response=self.ajaxGet('/api/graphs/9999')
        self.assertEqual(response.status_code, 404)

    def testCreateNode(self):
        oldncount=Graph.objects.get(pk=1).nodes.count()
        response=self.ajaxPost('/api/graphs/1/nodes', {'kind': 'orGate', 'id':4712, 'x':10, 'y':7})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'].startswith('http://'), True)
        self.assertEqual(oldncount+1, Graph.objects.get(pk=1).nodes.count() )
        # Check invalid type
        response=self.ajaxPost('/api/graphs/1/nodes', {'kind': 'foobar', 'id':4712, 'x':10, 'y':7})
        self.assertEqual(response.status_code, 400)

    def testDeleteNode(self):
        response=self.ajaxDelete('/api/graphs/1/nodes/88')
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really gone, including edge 

    def testRelocateNode(self):
        response=self.ajaxPostNode({"y": 8, "x":10}) 
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really done, including edge rearrangement

    def testPropertyChange(self):
        response=self.ajaxPostNode({"key": "foo", "value":"bar"})
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really done

    def testMorphNode(self):
        response=self.ajaxPostNode({"type":"t"})
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really done

    def testCreateGraph(self):
        response=self.ajaxPost('/api/graphs', {"kind": "fuzztree", "name":"Second graph"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'].startswith('http://'), True)
        # test invalid type
        response=self.ajaxPost('/api/graphs', {"kind": "foo", "name":"Third graph"})
        self.assertEqual(response.status_code, 400)

    def testDeleteEdge(self):
        response=self.ajaxDelete('/api/graphs/1/edges/66')
        self.assertEqual(response.status_code, 204)
        #TODO: Check if really gone 

    def testCreateEdge(self):
        # Delete edge before re-creating it
        response=self.ajaxDelete('/api/graphs/1/edges/77')
        self.assertEqual(response.status_code, 204)
        response=self.ajaxPost('/api/graphs/1/edges', {'id': 4714, 'source':4711, 'destination':222} )
        self.assertEqual(response.status_code, 201)
        #TODO: Check if really created 

class AnalysisTestCase(FuzzTreesTestCase):
    def requestAnalysis(self):
        """ Helper function for requesting an analysis run. Returns the analysis result as dictionary."""
        response=self.ajaxGet('/api/graphs/1/analysis/topEventProbability')
        self.assertNotEqual(response.status_code, 500) # you forgot to start the analysis server
        self.assertEqual(response.status_code, 201)
        jobUrl = response['Location']
        self.assertEqual(jobUrl.startswith('http://testserver/api/jobs/'), True) # check job creation
        response=self.ajaxGet(jobUrl)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content)

    def testStandardFixtureAnalysis(self):
        result=self.requestAnalysis()
        self.assertEqual(bool(result['validResult']),True)
        self.assertEqual(result['errors'],{})
        self.assertEqual(result['warnings'],{})



