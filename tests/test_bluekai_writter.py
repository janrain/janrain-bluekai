from unittest import TestCase
from datetime import datetime
from mock import MagicMock
from mock import call
from bluekai.bluekai_writter import *
from freezegun import freeze_time

frozen_datetime="2016-01-02 12:00:01"

@freeze_time(frozen_datetime)
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
    self.date = datetime.now().timestamp()

  def test_init(self):
    self.writter_mock.file.assert_has_calls([
      call('partnername_clientname_siteid_{}.bzip2'.format(self.date), mode='w'),
      call('partnername_clientname_siteid_{}.bzip2.trigger'.format(self.date), mode='w'),
    ])

  def test_write(self):
    self.bluekai_writter.write(self.valid_data)
    self.file_mock.assert_has_calls([
      call.write('abc\ta=1|b=2\nefg\ta=10|b=20\n'),
      call.write('FILE=partnername_clientname_siteid_{}.bzip2\nSIZE=26\nMD5SUM=5309154b2b0cd3ae147a0d5f4f39da31'.format(self.date))
    ])

  def test_close(self):
    self.bluekai_writter.close()
    self.file_mock.assert_has_calls([
      call.close(),
      call.close()
    ])
