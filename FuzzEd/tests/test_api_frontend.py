import json

from django.contrib.auth.models import User

from FuzzEd.models import Node, Notification, Edge
from common import fixt_simple, FuzzEdLiveServerTestCase


class FrontendApiTestCase(FuzzEdLiveServerTestCase):
    """
        Tests for the Frontend API called from JavaScript.
    """
    fixtures = fixt_simple['files']

    baseUrl = '/api/front'

    def setUp(self):
        self.setUpLogin()

    #TODO: Test that session authentication is checked in the API implementation
    #TODO: Test that the user can only access his graphs, and not the ones of other users

    def _testValidGraphJson(self, content):
        for key in ['id', 'seed', 'name', 'type', 'readOnly', 'nodes', 'edges', 'nodeGroups']:
            self.assertIn(key, content)

    def testGetGraph(self):
        for id, kind in fixt_simple['graphs'].iteritems():
            url = self.baseUrl + '/graphs/%u' % fixt_simple['pkFaultTree']
            response = self.ajaxGet(url)
            self.assertEqual(response.status_code, 200)
            content = json.loads(response.content)
            self._testValidGraphJson(content)
        response = self.ajaxGet(self.baseUrl + '/graphs/9999')
        self.assertEqual(response.status_code, 404)

    def testGraphDownload(self):
        for id, kind in fixt_simple['graphs'].iteritems():
            for format, test_str in [('graphml', '<graphml'), ('json', '{'), ('tex', '\\begin')]:
                url = self.baseUrl + '/graphs/%u?format=%s' % (fixt_simple['pkFaultTree'], format)
                response = self.ajaxGet(url)
                self.assertEqual(response.status_code, 200)
                self.assertIn(test_str, response.content)

    def testGetGraphs(self):
        url = self.baseUrl + '/graphs/'
        response = self.ajaxGet(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        assert ('graphs' in content)

    def testGraphFiltering(self):
        url = self.baseUrl + '/graphs/?kind=faulttree'
        response = self.ajaxGet(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        assert ('graphs' in content)

    def testCreateNode(self):
        initial_properties = {"name": "foo"}
        newnode = json.dumps({'y': 3,
                              'x': 7,
                              'kind': 'basicEvent',
                              'client_id': 888,
                              'properties': initial_properties})

        response = self.ajaxPost(self.baseUrl + '/graphs/%u/nodes/' % fixt_simple['pkFaultTree'],
                                 newnode,
                                 'application/json')
        self.assertEqual(response.status_code, 201)
#        newid = int(response['Location'].split('/')[-1])
#        newnode = Node.objects.get(client_id=newid, deleted=False)
#        self.assertItemsEqual(initial_properties, newnode.get_properties())

    def testCreateNodeGroup(self):
        nodes = [fixt_simple['clientIdAndGate'], fixt_simple['clientIdBasicEvent']]
        initial_properties =  {"name": "foo"}
        newgroup = json.dumps({'client_id': 999, 'nodeIds': nodes, "properties": initial_properties})
        response = self.ajaxPost(
                    self.baseUrl + '/graphs/%u/nodegroups/' % fixt_simple['pkDFD'],
                    newgroup,
                    'application/json')
        self.assertEqual(response.status_code, 201)
        print response['Location']
        newid = int(response['Location'].split('/')[-1])
        #TODO: Doesn't work due to non-saving of LiveServerTestCase
        #       newgroup = NodeGroup.objects.get(client_id=newid, deleted=False)
        #       saved_nodes=newgroup.nodes.all()
        #       self.assertItemsEqual(nodes, saved_nodes)

        # Get complete graph and see if the node group is registered correctly
        url = self.baseUrl + '/graphs/%u' % fixt_simple['pkDFD']
        response = self.ajaxGet(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        for group in content['nodeGroups']:
            self.assertEqual(group['id'], 999)
            self.assertItemsEqual(group['nodeIds'], nodes)
            self.assertItemsEqual(group['properties'], initial_properties)

    def testDeleteNode(self):
        response = self.ajaxDelete(
            self.baseUrl + '/graphs/%u/nodes/%u' % (fixt_simple['pkFaultTree'], fixt_simple['clientIdBasicEvent'])
        )
        self.assertEqual(response.status_code, 204)

    def testDeleteNodeGroup(self):
        #TODO: Fixture should have a node group, instead of creating it here
        nodes = [fixt_simple['clientIdAndGate'], fixt_simple['clientIdBasicEvent']]
        newgroup = json.dumps({'client_id': 999, 'nodeIds': nodes})
        response = self.ajaxPost(self.baseUrl + '/graphs/%u/nodegroups/' % fixt_simple['pkDFD'],
                                 newgroup,
                                 'application/json')
        self.assertEqual(response.status_code, 201)
        newgroup = response['Location']
        # Try delete
        response = self.ajaxDelete(newgroup)
        self.assertEqual(response.status_code, 204)

    def testRelocateNode(self):
        newpos = json.dumps({'properties': {"y": 3, "x": 7}})
        response = self.ajaxPatch(
                    self.baseUrl + '/graphs/%u/nodes/%u' % (fixt_simple['pkFaultTree'], fixt_simple['clientIdBasicEvent']),
                    newpos,
                    "application/json")
        self.assertEqual(response.status_code, 202)

    def testNodePropertyChange(self):
        newprop = json.dumps({"properties": {"name": "bar"}})
        response = self.ajaxPatch(self.baseUrl + '/graphs/%u/nodes/%u' % (fixt_simple['pkFaultTree'], fixt_simple['clientIdBasicEvent']),
                                  newprop,
                                  "application/json")
        self.assertEqual(response.status_code, 202)
        #TODO: Fetch graph and check that the property is really stored


    def testNodeGroupPropertyChange(self):
        #TODO: Fixture should have a node group, instead of creating it here
        nodes = [fixt_simple['clientIdAndGate'], fixt_simple['clientIdBasicEvent']]
        newgroup = json.dumps({'client_id': 999, 'nodeIds': nodes})
        response = self.ajaxPost(self.baseUrl + '/graphs/%u/nodegroups/' % fixt_simple['pkDFD'],
                                 newgroup,
                                 'application/json')
        self.assertEqual(response.status_code, 201)
        newgroup = response['Location']
        # Try changing
        newprop = json.dumps({"properties": {"name": "bar"}})
        response = self.ajaxPatch(newgroup,
                                  newprop,
                                  "application/json")
        self.assertEqual(response.status_code, 202)
        #TODO: Fetch graph and check that the property is really stored

    def testNodeGroupNodesChange(self):
        #TODO: Fixture should have a node group, instead of creating it here
        nodes1 = [fixt_simple['clientIdAndGate']]
        newgroup = json.dumps({'client_id': 999, 'nodeIds': nodes1})
        response = self.ajaxPost(self.baseUrl + '/graphs/%u/nodegroups/' % fixt_simple['pkDFD'],
                                 newgroup,
                                 'application/json')
        self.assertEqual(response.status_code, 201)
        newgroup = response['Location']
        # Try changing
        nodes2 = [fixt_simple['clientIdAndGate'], fixt_simple['clientIdBasicEvent']]
        newnodes = json.dumps({"nodeIds": nodes2})
        response = self.ajaxPatch(newgroup,
                                  newnodes,
                                  "application/json")
        self.assertEqual(response.status_code, 202)
        # Get complete graph and see if the node group is registered correctly
        url = self.baseUrl + '/graphs/%u' % fixt_simple['pkDFD']
        response = self.ajaxGet(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        for group in content['nodeGroups']:
            self.assertItemsEqual(group['nodeIds'], nodes2)

    def testEdgePropertyChange(self):
        newprop = json.dumps({"properties": {"name": "bar"}})
        response = self.ajaxPatch(self.baseUrl + '/graphs/%u/edges/%u' % (fixt_simple['pkDFD'], fixt_simple['clientIdEdgeDfd']),
                                  newprop,
                                  "application/json")
        self.assertEqual(response.status_code, 202)
        #TODO: Fetch graph and check that the property is really stored

    def testDeleteEdge(self):
        response = self.ajaxDelete(
            self.baseUrl + '/graphs/%u/edges/%u' % (fixt_simple['pkFaultTree'], fixt_simple['clientIdEdge']))
        self.assertEqual(response.status_code, 204)

    def testCreateEdge(self):
        initial_properties =  {"name": "foo"}
        newedge = json.dumps(
            {   'client_id': 4714,
                'source': fixt_simple['clientIdProcess'],
                'target': fixt_simple['clientIdStorage'],
                'properties': initial_properties
            }
        )
        # Only DFD edges support properties, so we use them here
        response = self.ajaxPost(self.baseUrl + '/graphs/%u/edges/' % fixt_simple['pkDFD'],
                                 newedge,
                                 'application/json')
        self.assertEqual(response.status_code, 201)
#        print response['Location']
#        newid = int(response['Location'].split('/')[-1])
#        newedge = Edge.objects.get(client_id=newid, deleted=False)
#        self.assertItemsEqual(initial_properties, newedge.get_properties())

    def testNotificationDismiss(self):
        # Create notification entry in the database
        u = User.objects.get(username='testadmin')
        n = Notification(title="Test notification")
        n.save()
        n.users.add(u)
        n.save()
        # Now check the dismiss call
        response = self.ajaxDelete(self.baseUrl + '/notification/%u/' % n.pk)
        self.assertEqual(response.status_code, 204)
