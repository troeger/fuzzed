import json, logging
from xml.dom import minidom
from django.test import TestCase
from django.test.client import Client
from FuzzEd.models.graph import Graph
from FuzzEd.models.node import Node

# This is the test suite.
#
# The typical workflow to add new tests is the following:
# 1.) Get yourself an empty local database with 'fab reset_db'.
# 2.) Draw one or more test graphs. 
# 3.) Create a fixture file from it with 'fab fixture_save:<filename.json>'. 
# 4.) Write your test class / methods as the ones below. Make heavy use of 
#     all the helper functions in FuzzTreesTestCase.
# 5.) Run the tests with 'fab run_tests'.
# 6.) Edit your fixture file by loading it into the local database 
#     with 'fab fixture_load:<filename.json>'

# This disables all the debug output. Sometimes it may be helpful.
logging.disable(logging.CRITICAL)

class FuzzTreesTestCase(TestCase):
    def setUp(self):
        self.c=Client()
        self.c.login(username='testadmin', password='testadmin') # added by 'fab fixture_save'

    def ajaxGet(self, url):
        return self.c.get( url, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest' )

    def ajaxPost(self, url, data):
        return self.c.post( url, data, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest' )

    def ajaxPostNode(self, data):
        return self.ajaxPost('/api/graphs/1/nodes/88', {'properties': json.dumps(data)})

    def ajaxDelete(self, url):
        return self.c.delete( url, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest' )

    def requestAnalysis(self, graph_id):
        """ Helper function for requesting an analysis run. 
            Returns the analysis result as dictionary as received by the frontend.
        """
        response=self.ajaxGet('/api/graphs/%u/analysis/topEventProbability'%graph_id)
        self.assertNotEqual(response.status_code, 500) # you forgot to start the analysis server
        self.assertEqual(response.status_code, 201)    # you got the wrong graph ID
        jobUrl = response['Location']
        self.assertEqual(jobUrl.startswith('http://testserver/api/jobs/'), True) # check job creation
        code = 202
        while (code == 202):
            response=self.ajaxGet(jobUrl)
            code = response.status_code 
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content)


class BasicApiTestCase(FuzzTreesTestCase):
    fixtures = ['basic.json']
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
    fixtures = ['analysis.json']

    def testStandardFixtureAnalysis(self):
        result=self.requestAnalysis(4)
        self.assertEqual(bool(result['validResult']),True)
        self.assertEqual(result['errors'],{})
        self.assertEqual(result['warnings'],{})
        self.assertEqual(result['configurations'][0]['alphaCuts']['1.0'],[0.5, 0.5])
        self.assertEqual(result['configurations'][1]['alphaCuts']['1.0'],[0.4, 0.4])




