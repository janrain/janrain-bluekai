from unittest import TestCase
from collections import OrderedDict
from bluekai.bluekai_tsv import *

class bluekai_test(TestCase):

  def test_fromRecord(self):
    record = { "uuid": "a-b-c", "key1": "value1", "key2":"value2" }
    record = OrderedDict(sorted(record.items(), key=lambda t: t[0]))
    actual = fromRecord(record,["key2","key1"])
    expected1 = "a-b-c\tkey1=value1|key2=value2\n"
    expected2 = "a-b-c\tkey2=value2|key1=value1\n"
    self.assertIn(actual, [expected1, expected2])

  def test_fromRecord_default_keys(self):
    record = { "uuid": "a-b-c", "key1": "value1", "key2":"value2" }
    record = OrderedDict(sorted(record.items(), key=lambda t: t[0]))
    actual = fromRecord(record,)
    expected = "a-b-c\t\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_list_types(self):
    record = { "uuid": "a-b-c", "list": ["value1"] }
    with self.assertRaises(TypeError):
        fromRecord(record, ["list"])

  def test_fromRecord_dict_types(self):
    record = { "uuid": "a-b-c", "dict": {"key":"value"} }
    with self.assertRaises(TypeError):
        fromRecord(record, ["dict"])

  def test_fromRecordsIterator(self):
    record1 = { "uuid": "a-b-c", "key": "value1" }
    record2 = { "uuid": "x-y-z", "key": "value2" }
    records = [record1, record2]
    records_iterator = fromRecordsIterator(records, ["key"])
    expected1 = "a-b-c\tkey=value1\n"
    expected2 = "x-y-z\tkey=value2\n"
    self.assertEqual(records_iterator.__next__(), expected1)
    self.assertEqual(records_iterator.__next__(), expected2)
    with self.assertRaises(StopIteration):
        records_iterator.__next__()

  def test_fromRecordsIterator_default_keys(self):
    record1 = { "uuid": "a-b-c", "key": "value1" }
    record2 = { "uuid": "x-y-z", "key": "value2" }
    records = [record1, record2]
    records_iterator = fromRecordsIterator(records)
    expected1 = "a-b-c\t\n"
    expected2 = "x-y-z\t\n"
    self.assertEqual(records_iterator.__next__(), expected1)
    self.assertEqual(records_iterator.__next__(), expected2)
    with self.assertRaises(StopIteration):
        records_iterator.__next__()

  def test_fromRecords(self):
    record1 = { "uuid": "a-b-c", "key": "value1" }
    record2 = { "uuid": "x-y-z", "key": "value2" }
    records = [record1, record2]
    actual = fromRecords(records, ["key"])
    expected = "a-b-c\tkey=value1\nx-y-z\tkey=value2\n"
    self.assertEqual(actual, expected)

  def test_fromRecords_key_map(self):
    record1 = { "uuid": "a-b-c", "key": "value1" }
    record2 = { "uuid": "x-y-z", "key": "value2" }
    records = [record1, record2]
    actual = fromRecords(records, {"key":"KEY"})
    expected = "a-b-c\tKEY=value1\nx-y-z\tKEY=value2\n"
    self.assertEqual(actual, expected)

  def test_fromRecords_default_keys(self):
    record1 = { "uuid": "a-b-c", "key": "value1" }
    record2 = { "uuid": "x-y-z", "key": "value2" }
    records = [record1, record2]
    actual = fromRecords(records, [])
    expected = "a-b-c\t\nx-y-z\t\n"
    self.assertEqual(actual, expected)
