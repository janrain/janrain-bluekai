# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from bluekai.config import *
from bluekai.config import _ENV_VARS
from freezegun import freeze_time

class getConfigTests(TestCase):

    @patch('os.getenv')
    def test_boolean_false(self, getenv_mock):
        getenv_mock.return_value = 'FALSE'
        config = get_config()
        self.assertIs(config['DEBUG'], False)

    @patch('os.getenv')
    def test_boolean_true(self, getenv_mock):
        getenv_mock.return_value = 'T'
        config = get_config()
        self.assertIs(config['DEBUG'], True)

    @patch('os.getenv')
    def test_valid_int(self, getenv_mock):
        getenv_mock.return_value = '1'
        config = get_config()
        self.assertIs(config['REMOTE_PORT'], 1)

    @patch('os.getenv')
    def test_invalid_int(self, getenv_mock):
        getenv_mock.return_value = 'a'
        config = get_config()
        self.assertEqual(config['REMOTE_PORT'], 22)

    @patch('os.getenv')
    def test_valid_list(self, getenv_mock):
        _ENV_VARS['LIST'] = [];
        getenv_mock.return_value = '["a"]'
        config = get_config()
        self.assertEqual(config['LIST'], ["a"])

    @patch('os.getenv')
    def test_invalid_list(self, getenv_mock):
        _ENV_VARS['LIST'] = [];
        getenv_mock.return_value = 'a'
        config = get_config()
        self.assertEqual(config['LIST'], [])

    @patch('os.getenv')
    def test_valid_dict(self, getenv_mock):
        _ENV_VARS['DICT'] = {};
        getenv_mock.return_value = '{"a":1}'
        config = get_config()
        self.assertEqual(config['DICT'], {"a":1})

    @patch('os.getenv')
    def test_invalid_dict(self, getenv_mock):
        _ENV_VARS['DICT'] = {};
        getenv_mock.return_value = 'a'
        config = get_config()
        self.assertEqual(config['DICT'], {})

class remoteFilenameTests(TestCase):

    frozen_datetime="2016-01-02 12:00:01"

    @freeze_time(frozen_datetime)
    def test_with_clientName(self):
        config = {
            'BLUEKAI_PARTNERNAME': "partnername",
            'BLUEKAI_CLIENTNAME': 'clientname',
            'BLUEKAI_SITEID': 'siteid',
        }
        actual = remote_filename(config)
        expected = ("partnername_clientname_siteid_1451764801.0.bzip2", "partnername_clientname_siteid_1451764801.0.bzip2.trigger")
        self.assertEqual(actual, expected)

    @freeze_time(frozen_datetime)
    def test_without_clientName(self):
        config = {
            'BLUEKAI_PARTNERNAME': "partnername",
            'BLUEKAI_SITEID': 'siteid',
        }
        actual = remote_filename(config)
        expected = ("partnername_siteid_1451764801.0.bzip2", "partnername_siteid_1451764801.0.bzip2.trigger")
        self.assertEqual(actual, expected)
