import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_does_fail_when_we_want(self):
        self.fail("Finish")
        pass

if __name__ == '__main__':
    unittest.main()
