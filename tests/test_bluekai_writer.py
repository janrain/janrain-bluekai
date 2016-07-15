from unittest import TestCase
from datetime import datetime
from mock import MagicMock
from mock import call
from bluekai.bluekai_writer import *
from freezegun import freeze_time

frozen_datetime="2016-01-02 12:00:01"

@freeze_time(frozen_datetime)
class bluekai_writer_test(TestCase):

  def setUp(self):
    self.data_file_mock = MagicMock()
    self.trigger_file_mock = MagicMock()
    self.writer_mock = MagicMock()
    self.writer_mock.file.side_effect = [
      self.data_file_mock,
      self.trigger_file_mock,
    ]
    self.config = {
      'BLUEKAI_PARTNERNAME': "partnername",
      'BLUEKAI_CLIENTNAME': 'clientname',
      'BLUEKAI_SITEID': 'siteid',
    }
    self.bluekai_writer = BlueKaiWriter(self.writer_mock, self.config)
    self.valid_data = "abc\ta=1|b=2\nefg\ta=10|b=20\n"
    self.date = datetime.now().timestamp()

  def test_init(self):
    self.writer_mock.file.assert_has_calls([
      call('partnername_clientname_siteid_{}.bz2'.format(self.date), mode='w'),
      call('partnername_clientname_siteid_{}.bz2.trigger'.format(self.date), mode='w'),
    ])

  def test_write(self):
    self.bluekai_writer.write(self.valid_data)
    self.data_file_mock.write.assert_called_with(
      b'BZh91AY&SYs"\xc4\xde\x00\x00\x08I\x80\x000p\x02;\x80\x00\x04 \x00!*\x0fSOI\x90\x80h\x02\xa5A\x1d\x06H\xc9\xb1-\xd5\xbf|]\xc9\x14\xe1BA\xcc\x8b\x13x')
    self.trigger_file_mock.write.assert_called_with(
      'FILE=partnername_clientname_siteid_{}.bz2\nSIZE=60\nMD5SUM=7714feae50126fedd232fc08b41aa44c'.format(self.date))

  def test_close(self):
    self.bluekai_writer.close()
    self.data_file_mock.close.assert_called_once_with()
    self.trigger_file_mock.close.assert_called_once_with()
