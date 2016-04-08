from unittest import TestCase
from collections import OrderedDict
from bluekai.bluekai_tsv import *
from datetime import date
from datetime import datetime
from freezegun import freeze_time

frozen_datetime="2016-01-02 10:20:30"
frozen_date="2016-01-02"

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

  def test_fromRecord_with_extra_paths(self):
    record = { "uuid": "a-b-c" }
    actual = fromRecord(record, ["path1","path2"])
    expected = "a-b-c\tpath1=|path2=\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_list_types(self):
    record = { "uuid": "a-b-c", "list": ["value1"] }
    with self.assertRaises(TypeError):
        fromRecord(record, ["list"])

  def test_fromRecord_dict_types(self):
    record = { "uuid": "a-b-c", "dict": {"key":"value"} }
    with self.assertRaises(TypeError):
        fromRecord(record, ["dict"])

  def test_fromRecord_none_types(self):
    record = { "uuid": "a-b-c", "none": None }
    actual = fromRecord(record, ["none"])
    expected = "a-b-c\tnone=\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_bool_types(self):
    record = { "uuid": "a-b-c", "value": True }
    actual = fromRecord(record, ["value"])
    expected = "a-b-c\tvalue=True\n"
    self.assertEqual(actual, expected)
    record = { "uuid": "a-b-c", "value": False }
    actual = fromRecord(record, ["value"])
    expected = "a-b-c\tvalue=False\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_int_types(self):
    record = { "uuid": "a-b-c", "value": 0 }
    actual = fromRecord(record, ["value"])
    expected = "a-b-c\tvalue=0\n"
    self.assertEqual(actual, expected)
    record = { "uuid": "a-b-c", "value": 1 }
    actual = fromRecord(record, ["value"])
    expected = "a-b-c\tvalue=1\n"
    self.assertEqual(actual, expected)

  @freeze_time(frozen_datetime)
  def test_fromRecord_datetime_types(self):
    value = datetime.now()
    record = { "uuid": "a-b-c", "value": value }
    actual = fromRecord(record, ["value"])
    expected = "a-b-c\tvalue={}\n".format(frozen_datetime)
    self.assertEqual(actual, expected)

  @freeze_time(frozen_date)
  def test_fromRecord_date_types(self):
    value = date.today()
    record = { "uuid": "a-b-c", "value": value }
    actual = fromRecord(record, ["value"])
    expected = "a-b-c\tvalue={}\n".format(frozen_date)
    self.assertEqual(actual, expected)

  def test_fromRecord_plural_types(self):
    record = { "uuid": "a-b-c", "plurals": [ { 'plural': "a" }, { 'plural': "b" }]}
    actual = fromRecord(record, ["plurals.plural"])
    expected = "a-b-c\tplurals.plural=a,b\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_plural_types_with_empty_str(self):
    record = { "uuid": "a-b-c", "plurals": [ { 'plural': "" }, { 'plural': "b" }]}
    actual = fromRecord(record, ["plurals.plural"])
    expected = "a-b-c\tplurals.plural=b\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_plural_types_with_empty_lists(self):
    record = { "uuid": "a-b-c", "plurals": [] }
    actual = fromRecord(record, ["plurals.plural"])
    expected = "a-b-c\tplurals.plural=\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_plural_types_with_mapping(self):
    record = { "uuid": "a-b-c", "plurals": [ { 'plural': "a" }, { 'plural': "b" }]}
    actual = fromRecord(record, {"plurals.plural": "plurals"})
    expected = "a-b-c\tplurals=a,b\n"
    self.assertEqual(actual, expected)

  def test_fromRecord_plural_types_with_error(self):
    record = { "uuid": "a-b-c", "plurals": [ { 'plural': "a" }, { 'plural': "b" }]}
    with self.assertRaises(TypeError):
        fromRecord(record, ["plurals"])

  def test_fromRecord_plural_object_with_error(self):
    record = { "uuid": "a-b-c", "object": { 'plural': "a" } }
    with self.assertRaises(TypeError):
        fromRecord(record, ["object"])

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
