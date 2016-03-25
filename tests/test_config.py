# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from bluekai.config import *
from bluekai.config import _ENV_VARS

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
