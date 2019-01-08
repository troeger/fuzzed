import unittest
import subprocess
import sys
import os
from xml.dom.minidom import parse


class AnalysisTestCase(unittest.TestCase):
    """
        These are tests based on the analysis engine input files in ./analysis.
        They only test if the analysis engine crashes on them.
        The may later be translated to real tests with some expected output.
    """

    @unittest.skipUnless(
        sys.platform.startswith("linux"), "requires Linux")
    def testFileAnalysis(self):
        for root, dirs, files in os.walk('/ore-back/tests/analysis'):
            for f in files:
                fname = root + os.sep + f
                print "Testing " + fname
                retcode = subprocess.call(
                    '/ore-back/lib/ftanalysis_exe %s /tmp/output.xml /tmp' %
                    (fname), shell=True)
                self.assertEqual(retcode, 0, fname + " failed")
                parse('/tmp/output.xml')
