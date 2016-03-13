# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from mock import Mock
from mock import MagicMock
import logging
from bluekai import create_app
from bluekai import logging_init
from bluekai import _add_headers
from bluekai._version import __version__

class create_app_test(TestCase):

    def setUp(self):
        self.config = {
            'DEBUG': "",
        }
        self.model_mock = Mock()

    def test_production(self):

        app = create_app(self.config, self.model_mock)
        self.assertIs(app.model, self.model_mock)
        self.model_mock.exists.assert_not_called()
        self.model_mock.create_table.assert_not_called()

    def test_debug_when_table_does_not_exist(self):
        self.config['DEBUG'] = True
        self.model_mock.exists.return_value = False
        app = create_app(self.config, self.model_mock)
        self.model_mock.exists.assert_called_once_with()
        self.model_mock.create_table.assert_called_once_with(
            read_capacity_units=1, write_capacity_units=1)

    def test_debug_when_table_exist(self):
        self.config['DEBUG'] = True
        self.model_mock.exists.return_value = True
        app = create_app(self.config, self.model_mock)
        self.model_mock.exists.assert_called_once_with()
        self.model_mock.create_table.assert_not_called()


class logging_init_test(TestCase):

    def setUp(self):

        self.config = {
            'DEBUG': "",
        }
        self.app = Mock()
        self.app.config = {
            'APP_LOG_FILE': 'test_app_log_file',
            'APP_LOG_NUM_BACKUPS': 'test_app_log_backups',
            'APP_LOG_FILESIZE': '1000',
            'LOGGER_NAME': 'test_logger_name',
        }

    def test_production(self):

        self.app.debug = False
        handler = logging_init(self.app)
        self.assertEqual(handler.level, logging.INFO)

    def test_debug(self):

        self.app.debug = True
        handler = logging_init(self.app)
        self.assertEqual(handler.level, logging.DEBUG)

class add_headers_test(TestCase):

    def test_run(self):
        response_mock = MagicMock()
        returned_response = _add_headers(response_mock)
        response_mock.headers.__setitem__.assert_called_once_with('X-App-Version', __version__)
        self.assertIs(response_mock, returned_response)
