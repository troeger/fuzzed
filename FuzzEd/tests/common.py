'''
    This is the test suite.

    TODO: Several test would look better if the model is checked afterwards for the changes being applied
        (e.g. node relocation). Since we use the LiveServerTestCase base, this is not possible, since
        database modifications are not commited at all. Explicit comitting did not help ...
'''

import json

from django.test import LiveServerTestCase, TestCase
from django.test.client import Client



# This disables all the debug output from the FuzzEd server, e.g. Latex rendering nodes etc.
#import logging
#logging.disable(logging.CRITICAL)

# The fixtures used in different test classes
fixt_analysis = {
                'files' :  ['analysis.json', 'testuser.json'], 
                'graphs':  {7: 'faulttree', 8: 'faulttree'},
                'results': {7: 'results/rate_tree.xml', 8: 'results/prdc_tree.xml'},               
                'rate_faulttree': 7,                # Graph PK
                'prdc_fuzztree': 8,                # Graph PK
                'prdc_configurations': 8,           # Decomposition number
                'prdc_peaks': [0.31482, 0.12796, 0.25103, 0.04677, 0.36558, 0.19255, 0.30651, 0.11738]
                }

fixt_simple = {
                'files' : ['simple.json', 'testuser.json'], 
                'graphs': {1: 'faulttree', 2: 'fuzztree', 3: 'rbd'},
                'pkProject': 1,
                'pkFaultTree': 1,
                'pkDFD': 1,  # TODO: This is a hack, since nobody checks the validity of node groups for the graph kind so far
                'clientIdEdge': 4,
                'clientIdAndGate': 1,
                'clientIdBasicEvent': 2
              }

fixt_mincut = {
                'files': ['mincut1.json', 'testuser.json'],
                'mincut_faulttree': 1,
                'mincut_numcuts': 3
              }

fixt_unicode = {
                'files': ['unicode.json', 'testuser.json'],
                'graphs': {1: 'faulttree'},
                'pkProject': 1,
                'pkFaultTree': 1
    
               }

class FuzzEdTestHelpers():
    """
        The base class for all test cases that rely on a reachable web server during testing.

        This is need when the backend daemon needs to call back, or if some HTTP redirection target
        is needed.

        Mainly provides helper functions for deal with auth stuff.
    """

    def setUpAnonymous(self):
        ''' If the test case wants to have a anonymous login session, it should call this function in setUp().'''
        self.c = Client()

    def setUpLogin(self):
        ''' If the test case wants to have a functional login session, it should call this function in setUp().'''
        self.c = Client()
        self.c.login(username='testadmin', password='testadmin')

    def get(self, url):
        return self.c.get(url)

    def post(self, url, data):
        return self.c.post(url, data)

    def getWithAPIKey(self, url):
        return self.c.get(url, **{'HTTP_AUTHORIZATION': 'ApiKey f1cc367bc09fc95720e6c8a4225ae2b912fff91b'})

    def postWithAPIKey(self, url, data, content_type):
        return self.c.post(url, data, content_type,
                           **{'HTTP_AUTHORIZATION': 'ApiKey f1cc367bc09fc95720e6c8a4225ae2b912fff91b'})

    def ajaxGet(self, url):
        return self.c.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def ajaxPost(self, url, data, content_type):
        """
        :rtype : django.http.response.HttpResponse
        """
        return self.c.post(url, data, content_type, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

    def ajaxPatch(self, url, data, content_type):
        """
        :rtype : django.http.response.HttpResponse
        """
        return self.c.patch(url, data, content_type, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

    def ajaxDelete(self, url):
        return self.c.delete(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def requestJob(self, base_url, graph, kind):
        """ 
            Helper function for requesting a job. Waits for the result and returns its URL.
        """
        newjob = json.dumps({'kind': kind})
        response = self.ajaxPost(base_url + '/graphs/%u/jobs/' % graph, newjob, 'application/json')
        self.assertNotEqual(response.status_code, 500)  # the backend daemon is not started
        self.assertEqual(response.status_code, 201)  # test if we got a created job
        assert ('Location' in response)
        jobUrl = response['Location']
        code = 202
        assert (not jobUrl.endswith('jobs/'))
        print "Waiting for result from " + jobUrl,
        while (code == 202):
            response = self.ajaxGet(jobUrl)
            code = response.status_code
        self.assertEqual(response.status_code, 200)
        assert ('Location' in response)
        resultUrl = response['Location']
        return response

class FuzzEdLiveServerTestCase(LiveServerTestCase, FuzzEdTestHelpers):
    pass

class FuzzEdTestCase(TestCase, FuzzEdTestHelpers):
    pass






