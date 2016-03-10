from unittest import TestCase
from bluekai.date_utils import *
from datetime import datetime

class record_datetime_test(TestCase):

  def setUp(self):
    self.datetime_string = "1970-01-01 00:00:00.000000 +0000"
    self.datetime_number = 0
    self.datetime_object = datetime.utcfromtimestamp(self.datetime_number)

  def test_fromRecordDateTime(self):
    actual = fromRecordDateTime(self.datetime_string)
    expected = self.datetime_object
    self.assertEqual(actual, expected)

  def test_toRecordDateTime(self):
    actual = toRecordDateTime(self.datetime_object)
    expected = self.datetime_string.replace(' +0000', '')
    self.assertEqual(actual, expected)

  def test_fromModelDateTime(self):
    actual = fromModelDateTime(self.datetime_number)
    expected = self.datetime_object
    self.assertEqual(actual, expected)

  def test_toModelDateTime(self):
    actual = toModelDateTime(self.datetime_object)
    expected = self.datetime_number
    self.assertEqual(actual, expected)
