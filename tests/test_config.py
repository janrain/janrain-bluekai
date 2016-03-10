# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from bluekai.config import *

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
        self.assertEqual(config['REMOTE_PORT'], 443)
