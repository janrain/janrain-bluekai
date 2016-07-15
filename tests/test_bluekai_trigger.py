from unittest import TestCase
from bluekai.bluekai_trigger import *

class bluekai_trigger_test(TestCase):

  def setUp(self):
    self.filename = "testfilename"
    self.valid_data = b"abc\ta=1|b=2\nefg\ta=10|b=20\n"

  def test_fromData(self):
    actual = fromData(self.filename, self.valid_data)
    expected = "FILE=testfilename\nSIZE=26\nMD5SUM=5309154b2b0cd3ae147a0d5f4f39da31"
    self.assertEqual(actual, expected)
