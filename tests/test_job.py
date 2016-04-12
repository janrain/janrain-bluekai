# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from mock import Mock
from mock import MagicMock
from mock import call
from datetime import datetime
from bluekai.date_utils import toModelDateTime
from bluekai.job import *

class run_test(TestCase):

    def setUp(self):
        self.config = {
        }
        self.jobModel_mock = Mock()
        self.writter_mock = Mock()
        self.logger_mock = Mock()
        self.datalib_mock = Mock()
        self.converter_mock = Mock()
        self.job_mock = Mock()
        self.job_mock.ended = 3
        self.job_mock.started = 2
        self.jobModel_mock.get.return_value = self.job_mock

    @patch('bluekai.job.do_job')
    def test_with_out_errors(self, do_job_mock):
        run(self.job_mock, self.writter_mock, self.config, self.logger_mock, self.datalib_mock, self.converter_mock)
        self.job_mock.stop.assert_called_once_with()
        self.logger_mock.exception.assert_not_called()
        self.logger_mock.error.assert_not_called()
        self.logger_mock.info.assert_has_calls([ call("start"), call("end (1 seconds)") ])

    @patch('bluekai.job.do_job')
    def test_with_errors(self, do_job_mock):
        error = "test_error"
        exception = Exception(error)
        do_job_mock.side_effect = exception
        run(self.job_mock, self.writter_mock, self.config, self.logger_mock, self.datalib_mock, self.converter_mock)
        self.job_mock.stop.assert_called_once_with()
        self.logger_mock.error.assert_called_with(str(exception))
        self.logger_mock.error.assert_called_with(error)
        self.logger_mock.info.assert_has_calls([ call("start"), call("end (1 seconds)") ])

class do_job_test(TestCase):

    def setUp(self):
        self.config = {
            'JANRAIN_URI': 'test_janrain_uri',
            'JANRAIN_CLIENT_ID': 'test_janrain_client_id',
            'JANRAIN_CLIENT_SECRET': 'test_janrain_client_secret',
            'JANRAIN_SCHEMA_NAME': 'test_janrain_schema_name',
            'JANRAIN_ATTRIBUTE_KEYS': '',
            'JANRAIN_BATCH_SIZE': 2,
        }
        self.jobModel_mock = Mock()
        self.writter_mock = MagicMock()
        self.logger_mock = Mock()
        self.converter_mock = Mock()
        self.job_mock = MagicMock()
        self.records_iterator = [
            { "lastUpdated": "2016-01-01 01:01:01.000000" },
            { "lastUpdated": "2016-01-02 01:01:01.000000" },
            { "lastUpdated": "2016-02-01 01:01:01.000000 +0000" },
            { "lastUpdated": "2016-02-04 01:01:01.000000" },
        ]
        self.capture_schema_mock = Mock()
        self.capture_schema_mock.records.iterator.return_value = self.records_iterator
        self.capture_app_mock = Mock()
        self.capture_app_mock.get_schema.return_value = self.capture_schema_mock
        self.datalib_mock = Mock()
        self.datalib_mock.get_app.return_value = self.capture_app_mock
        self.job_mock.lastUpdated = datetime.utcfromtimestamp(0)

    def test_run(self):

        do_job(self.job_mock, self.writter_mock, self.config,
            self.logger_mock, self.datalib_mock, self.converter_mock)

        self.writter_mock.__enter__.assert_called_once_with()
        self.writter_mock.__exit__.assert_called_once_with(None, None, None)
        self.converter_mock.assert_has_calls([
            call(self.records_iterator[0], ''),
            call(self.records_iterator[1], ''),
            call(self.records_iterator[2], ''),
            call(self.records_iterator[3], ''),
        ])
        self.logger_mock.debug.assert_has_calls([
            call("wrote record 2"),
            call("wrote record 4"),
        ])
        self.logger_mock.info.assert_called_once_with("exported 4 records")

    def test_error(self):

        self.records_iterator = [
            { "lastUpdated": "2016-01-01 01:01:01.000000", "list": [] }
        ]
        self.capture_schema_mock.records.iterator.return_value = self.records_iterator
        self.converter_mock.side_effect = TypeError

        with self.assertRaises(SystemExit):
            do_job(self.job_mock, self.writter_mock, self.config,
                self.logger_mock, self.datalib_mock, self.converter_mock)

        self.writter_mock.__enter__.assert_called_once_with()
        self.converter_mock.assert_has_calls([
            call(self.records_iterator[0], ''),
        ])
        self.logger_mock.debug.assert_has_calls([])
        self.logger_mock.error.assert_called_once_with("")
