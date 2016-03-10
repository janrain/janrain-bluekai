from unittest import TestCase
from bluekai.bluekai_tsv import *

class bluekai_test(TestCase):

  def test_fromRecord(self):
    record = { "uuid": "a-b-c", "key1": "value1", "key2":"value2" }
    actual = fromRecord(record)
    expected = "a-b-c\tkey2=value2|key1=value1\n"
    self.assertEqual(actual, expected)

  def test_fromRecords(self):
    record1 = { "uuid": "a-b-c", "key1": "value1" }
    record2 = { "uuid": "x-y-z", "key2": "value2" }
    records = [record1, record2]
    actual = fromRecords(records)
    expected = "a-b-c\tkey1=value1\nx-y-z\tkey2=value2\n"
    self.assertEqual(actual, expected)