from django.test import TestCase
import os
import subprocess
import unittest


def mocha_exists():
    try:
        subprocess.call(["mocha-phantomjs", "-V"])
        return True
    except OSError as e:
        return False


class JavaScriptTestCase(TestCase):

    """
        Call JavaScript test framework to do the job.
    """
    @unittest.skipUnless(mocha_exists(), "requires mocha-phantomjs")
    def testJavaScriptCode(self):
        subprocess.call(
            ["mocha-phantomjs", "FuzzEd/tests/js-tests/src/test_runner.html"])
