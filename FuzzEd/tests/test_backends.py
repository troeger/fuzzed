from xml.dom.minidom import parse
import subprocess
import unittest
import sys
import os

from common import FuzzEdTestCase


class AnalysisInputFilesTestCase(FuzzEdTestCase):
    """
        These are tests based on the analysis engine input files in fixture/analysis.
        They only test if the analysis engine crashes on them.
        The may later be translated to real tests with some expected output.
    """

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Vagrant Linux")
    def testFileAnalysis(self):
        for root, dirs, files in os.walk('FuzzEd/fixtures/analysis'):
            for f in files:
                fname = root + os.sep + f
                print "Testing " + fname
                retcode = subprocess.call('backends/lib/ftanalysis_exe %s /tmp/output.xml /tmp' % (fname), shell=True)
                self.assertEqual(retcode, 0, fname + " failed")
                dom = parse('/tmp/output.xml')
