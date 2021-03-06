# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from mock import Mock
from datetime import datetime
from bluekai.records import *

frozen_datetime="2016-01-01"

class models_test(TestCase):

    def test_recordsNewerThan(self):
        records_iterator_mock = Mock()

        capture_schema_mock = Mock()
        capture_schema_mock.records.iterator.return_value = records_iterator_mock

        capture_app_mock = Mock()
        capture_app_mock.get_schema.return_value = capture_schema_mock

        datetime_now = datetime.utcfromtimestamp(0)
        config = {
            'JANRAIN_SCHEMA_NAME': "schemaName",
            'JANRAIN_ATTRIBUTE_KEYS': ["a"],
            'JANRAIN_BATCH_SIZE': 1000,
        }

        result = recordsNewerThan(capture_app_mock, config, datetime_now)

        self.assertIs(result, records_iterator_mock)

        capture_app_mock.get_schema.assert_called_once_with(config['JANRAIN_SCHEMA_NAME'])

        capture_schema_mock.records.iterator.assert_called_once_with(
            filtering="lastUpdated > '{}'".format(datetime_now.strftime("%Y-%m-%d %H:%M:%S")),
            batch_size=config['JANRAIN_BATCH_SIZE'],
            attributes=['a', 'lastUpdated', 'uuid']
        )

    def test_recordsNewerThan_with_none_date(self):
        records_iterator_mock = Mock()

        capture_schema_mock = Mock()
        capture_schema_mock.records.iterator.return_value = records_iterator_mock

        capture_app_mock = Mock()
        capture_app_mock.get_schema.return_value = capture_schema_mock

        datetime_now = datetime.utcfromtimestamp(0)
        config = {
            'JANRAIN_SCHEMA_NAME': "schemaName",
            'JANRAIN_ATTRIBUTE_KEYS': [],
            'JANRAIN_BATCH_SIZE': 1000,
        }

        result = recordsNewerThan(capture_app_mock, config)

        self.assertIs(result, records_iterator_mock)

        capture_app_mock.get_schema.assert_called_once_with(config['JANRAIN_SCHEMA_NAME'])

        capture_schema_mock.records.iterator.assert_called_once_with(
            filtering="lastUpdated > '{}'".format(datetime_now.strftime("%Y-%m-%d %H:%M:%S")),
            batch_size=config['JANRAIN_BATCH_SIZE'],
            attributes=['lastUpdated', 'uuid']
        )


