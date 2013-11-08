import unittest as test  # @UnusedWildImport
import os
lib_path = os.path.abspath("../../trunk")
os.system("rm trunk 2> .log")
os.system("ln -s %s trunk 2> .log" % lib_path)


from TesteTV import *  # @UnusedWildImport
from TesteSOM import *  # @UnusedWildImport
from TesteResidencia import *  # @UnusedWildImport
from TesteComodo import *  # @UnusedWildImport


def SuiteTest():
    suite = test.TestSuite()
    suite.addTest(test.makeSuite(TesteTV))
    suite.addTest(test.makeSuite(TesteSOM))
    suite.addTest(test.makeSuite(TesteResidencia))
    suite.addTest(test.makeSuite(TesteComodo))
    return suite

if __name__ == "__main__":
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    runner = test.TextTestRunner()
    test_suite = SuiteTest()
    runner.run(test_suite)
