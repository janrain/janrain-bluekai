from unittest import TestCase
from mock import MagicMock
from mock import call
from bluekai.bluekai_writter import *
from freezegun import freeze_time

@freeze_time("2016-01-02 12:00:01")
class bluekai_writter_test(TestCase):

  def setUp(self):
    self.file_mock = MagicMock()
    self.writter_mock = MagicMock()
    self.writter_mock.file.return_value = self.file_mock;
    self.config = {
      'BLUEKAI_PARTNERNAME': "partnername",
      'BLUEKAI_CLIENTNAME': 'clientname',
      'BLUEKAI_SITEID': 'siteid',
    }
    self.bluekai_writter = BlueKaiWritter(self.writter_mock, self.config)
    self.valid_data = "abc\ta=1|b=2\nefg\ta=10|b=20\n"

  def test_init(self):
    self.writter_mock.file.assert_has_calls([
      call('partnername_clientname_siteid_1451764801.0.bzip2', mode='w'),
      call('partnername_clientname_siteid_1451764801.0.bzip2.trigger', mode='w'),
    ])

  def test_write(self):
    self.bluekai_writter.write(self.valid_data)
    self.file_mock.assert_has_calls([
      call.write('abc\ta=1|b=2\nefg\ta=10|b=20\n'),
      call.write('FILE=partnername_clientname_siteid_1451764801.0.bzip2\nSIZE=26\nMD5SUM=5309154b2b0cd3ae147a0d5f4f39da31')
    ])

  def test_close(self):
    self.bluekai_writter.close()
    self.file_mock.assert_has_calls([
      call.close(),
      call.close()
    ])
