from django.test import TestCase

from FuzzEd.models.graph import Graph
from .common import fixt_unicode


@tag('front')
class UnicodeTestCase(TestCase):
    fixtures = fixt_unicode['files']

    def testTikzSerialize(self):
        g = Graph.objects.get(pk=fixt_unicode['pkFaultTree'])
        assert (len(g.to_tikz()) > 0)
