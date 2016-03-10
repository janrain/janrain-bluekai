# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from mock import Mock
from bluekai.models import *

class models_test(TestCase):

    def setUp(self):
        self.config = {
            'JANRAIN_URI': "test-janrain-uri",
            'JANRAIN_SCHEMA_NAME': "test-janrain-schema-name",
        }

    def test_appId(self):
        actual = JobModel.appId(self.config)
        expected = "{}:{}".format(self.config['JANRAIN_URI'], self.config['JANRAIN_SCHEMA_NAME'])
        self.assertEqual(actual, expected)
