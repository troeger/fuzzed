import json
import os

from FuzzEd.models import Graph
from .common import fixt_simple, FuzzEdLiveServerTestCase, FuzzEdTestCase

import logging
logging.basicConfig(level=logging.DEBUG)


class ExternalAPITestCase(FuzzEdLiveServerTestCase):

    """
        Tests for the Tastypie API.
    """
    fixtures = fixt_simple['files']

    def setUp(self):
        self.setUpAnonymous()

    def testMissingAPIKey(self):
        response = self.get('/api/v1/project/?format=json')
        self.assertEqual(response.status_code, 401)

    def testOriginalAPIKeyFormat(self):
        ''' We have our own APIKey format, so the original Tastypie version should no longer work.'''
        response = self.c.get('/api/v1/project/?format=json',
                              **{'HTTP_AUTHORIZATION': 'ApiKey testadmin:f1cc367bc09fc95720e6c8a4225ae2b912fff91b'})
        self.assertEqual(response.status_code, 401)

    def testRootResource(self):
        ''' Root view of external API should provide graph and project resource base URLs, even without API key.'''
        response = self.get('/api/v1/?format=json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        assert ('graph' in data)
        assert ('project' in data)

    def testProjectListResource(self):
        response = self.getWithAPIKey('/api/v1/project/?format=json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        assert ('objects' in data)
        assert ('graphs' in data['objects'][0])

    def testGraphListResource(self):
        response = self.getWithAPIKey('/api/v1/graph/?format=json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

    def testSingleProjectResource(self):
        response = self.getWithAPIKey(
            '/api/v1/project/%u/?format=json' %
            fixt_simple['pkProject'])
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

    def testJsonExport(self):
        for id, kind in fixt_simple['graphs'].iteritems():
            response = self.get('/api/v1/graph/%u/?format=json' % id)
            self.assertEqual(response.status_code, 401)
            response = self.getWithAPIKey('/api/v1/graph/%u/?format=json' % id)
            data = json.loads(response.content)
            self.assertEqual(response.status_code, 200)

    def testLatexExport(self):
        for id, kind in fixt_simple['graphs'].iteritems():
            if kind in ['faulttree', 'fuzztree']:
                response = self.get('/api/v1/graph/%u/?format=tex' % id)
                self.assertEqual(response.status_code, 401)
                response = self.getWithAPIKey(
                    '/api/v1/graph/%u/?format=tex' %
                    id)
                self.assertEqual(response.status_code, 200)
                assert ("tikz" in response.content)

    def testGraphmlExport(self):
        for id, kind in fixt_simple['graphs'].iteritems():
            if kind in ['faulttree', 'fuzztree']:
                # Should only be possible with API key authentication
                response = self.get('/api/v1/graph/%u/?format=graphml' % id)
                self.assertEqual(response.status_code, 401)
                response = self.getWithAPIKey(
                    '/api/v1/graph/%u/?format=graphml' %
                    id)
                self.assertEqual(response.status_code, 200)
                assert ("<graphml" in response.content)

    def testGraphmlImport(self):
        for id, kind in fixt_simple['graphs'].iteritems():
            # First export GraphML
            print "Testing graph %u (%s)" % (id, kind)
            response = self.getWithAPIKey(
                '/api/v1/graph/%u/?format=graphml' %
                id)
            self.assertEqual(response.status_code, 200)
            graphml = response.content
            # Now import the same GraphML
            response = self.postWithAPIKey('/api/v1/graph/?format=graphml&project=%u' % fixt_simple['pkProject'], graphml,
                                           'application/xml')
            self.assertEqual(response.status_code, 201)
            # Check if the claimed graph really was created
            newid = int(response['Location'].split('/')[-2])
            original = Graph.objects.get(pk=id)
            copy = Graph.objects.get(pk=newid)
            self.assertTrue(original.same_as(copy))

    def testInvalidGraphImportProject(self):
        # First export valid GraphML
        response = self.getWithAPIKey(
            '/api/v1/graph/%u/?format=graphml' %
            fixt_simple['pkFaultTree'])
        self.assertEqual(response.status_code, 200)
        graphml = response.content
        # Now send request with wrong project ID
        response = self.postWithAPIKey(
            '/api/v1/graph/?format=graphml&project=99',
            graphml,
            'application/xml')
        self.assertEqual(response.status_code, 403)

    def testMissingGraphImportProject(self):
        # First export valid GraphML
        response = self.getWithAPIKey(
            '/api/v1/graph/%u/?format=graphml' %
            fixt_simple['pkFaultTree'])
        self.assertEqual(response.status_code, 200)
        graphml = response.content
        # Now send request with wrong project ID
        response = self.postWithAPIKey(
            '/api/v1/graph/?format=graphml',
            graphml,
            'application/xml')
        self.assertEqual(response.status_code, 403)

    def testInvalidGraphImportFormat(self):
        for wrong_format in ['json', 'tex', 'xml']:
            response = self.postWithAPIKey('/api/v1/graph/?format=%s&project=%u' % (wrong_format, fixt_simple['pkProject']),
                                           "<graphml></graphml>", 'application/text')
            self.assertEqual(response.status_code, 413)

    def testInvalidContentType(self):
        for format in ['application/text',
                       'application/x-www-form-urlencoded']:
            response = self.postWithAPIKey('/api/v1/graph/?format=graphml&project=%u' % (fixt_simple['pkProject']),
                                           "<graphml></graphml>", format)
            self.assertEqual(response.status_code, 413)

    def testFoo(self):
        ''' Leave this out, and the last test will fail. Dont ask me why.'''
        assert (True)


class GraphMLFilesTestCase(FuzzEdTestCase):

    """
        Testing different GraphML file imports.
        The fixture gives us existing user accounts and a valid project ID.
    """
    fixtures = fixt_simple['files']

    def setUp(self):
        self.setUpAnonymous()

    def testImportFiles(self):
        files = [
            f for f in os.listdir('FuzzEd/fixtures') if f.endswith(".graphml")]
        print files
        for f in files:
            print("Testing " + f)
            text = open('FuzzEd/fixtures/' + f).read()
            # Now import the same GraphML
            response = self.postWithAPIKey(
                '/api/v1/graph/?format=graphml&project=%u' % fixt_simple[
                    'pkProject'],
                text,
                'application/xml')
            self.assertEqual(response.status_code, 201)
