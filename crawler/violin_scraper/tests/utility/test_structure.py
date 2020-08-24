import unittest


class TestStructure(unittest.TestCase):

    '''
    def test_upper(self):
        """
        Obsoleted
        """
        print("test_upper")

    def test_isupper(self):
        """
        Obsoleted
        """
        print("test_isupper")
    '''

    def test_split(self):
        print("test_split")

    def test_one(self):
        print("test_one")

# ========================== Fixture =====================================
    def setUp(self):
        print("setup")

    def tearDown(self):
        print("tearDown")

    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
