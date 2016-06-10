# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import Mock
from mock import patch
import flask
import paramiko
import janrain_datalib
from bluekai import bluekai_tsv
from datetime import datetime
from bluekai.models import JobModel
from bluekai.job import run as jobRunner
from bluekai.sftpproxy import SftpProxy
from bluekai.resources import export
from bluekai.resources import _export
from bluekai.bluekai_writter import BlueKaiWritter

class export_test(TestCase):

    def setUp(self):
        self.app = flask.Flask(__name__)
        self.config = {
            'LOGGER_NAME': "test_logger_name",
            'SFTP_BUFFER_SIZE': 1000,
        }
        self.job_mock = Mock()
        self.sftp_mock = Mock()
        self.last_updated = datetime.utcfromtimestamp(0)
        self.records_iterator = Mock()
        self.logging_mock = Mock()
        self.writter_mock = Mock()
        self.sftpProxy_mock = Mock()
        self.threadexecutor_mock = Mock()
        self.jobModel_mock = Mock()

    def test_export(self):

        with self.app.test_request_context():
            with patch('flask.current_app') as current_app_mock,\
                 patch('logging.getLogger') as logging_getLogger_mock,\
                 patch('bluekai.resources._export') as _export_mock:

                current_app_mock.config.copy = Mock(return_value=self.config)
                current_app_mock.threadexecutor = self.threadexecutor_mock
                logging_getLogger_mock.return_value = self.logging_mock

                result = export()

                self.assertEqual(result, ("ok", 200))
                _export_mock.assert_called_once_with(
                    self.config, JobModel, SftpProxy, BlueKaiWritter,
                    self.threadexecutor_mock, self.logging_mock)

    def test__export_starting_new_job(self):

        self.jobModel_mock.get.return_value = self.job_mock
        self.sftpProxy_mock.return_value = self.sftp_mock
        self.job_mock.start.return_value = True

        _export(self.config, self.jobModel_mock, self.sftpProxy_mock, self.writter_mock, self.threadexecutor_mock, self.logging_mock)

        self.jobModel_mock.get.assert_called_once_with(self.config)
        self.sftpProxy_mock.assert_called_once_with(paramiko, self.config, self.logging_mock)
        self.job_mock.start.assert_called_once_with()
        self.logging_mock.warning.assert_not_called()

    def test__export_job_already_started(self):

        self.jobModel_mock.get.return_value = self.job_mock
        self.sftpProxy_mock.return_value = self.sftp_mock
        self.sftp_mock.file.return_value = self.writter_mock
        self.job_mock.start.return_value = False

        _export(self.config, self.jobModel_mock, self.sftpProxy_mock, self.writter_mock, self.threadexecutor_mock, self.logging_mock)

        self.jobModel_mock.get.assert_called_once_with(self.config)
        self.sftpProxy_mock.assert_called_once_with(paramiko, self.config, self.logging_mock)
        self.job_mock.start.assert_called_once_with()
        self.threadexecutor_mock.submit.assert_not_called()
        self.logging_mock.warning.assert_called_once_with("export job already running")

