# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from mock import Mock
from mock import call
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
        run(self.jobModel_mock, self.writter_mock, self.config, self.logger_mock, self.datalib_mock, self.converter_mock)
        self.jobModel_mock.get.assert_called_once_with(self.config)
        self.job_mock.stop.assert_called_once_with()
        self.logger_mock.exception.assert_not_called()
        self.logger_mock.error.assert_not_called()
        self.logger_mock.info.assert_has_calls([ call("start"), call("end (1 seconds)") ])

    @patch('bluekai.job.do_job')
    def test_with_errors(self, do_job_mock):
        error = "test_error"
        exception = Exception(error)
        do_job_mock.side_effect = exception
        run(self.jobModel_mock, self.writter_mock, self.config, self.logger_mock, self.datalib_mock, self.converter_mock)
        self.jobModel_mock.get.assert_called_once_with(self.config)
        self.job_mock.stop.assert_called_once_with()
        self.logger_mock.exception.assert_called_once_with(exception)
        self.logger_mock.error.assert_called_once_with(error)
        self.logger_mock.info.assert_has_calls([ call("start"), call("end (1 seconds)") ])
