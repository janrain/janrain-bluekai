# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from mock import Mock
from datetime import datetime
import pynamodb.models
from pynamodb.exceptions import DoesNotExist
from pynamodb.exceptions import PutError
from bluekai.models import *
from freezegun import freeze_time

frozen_datetime="2016-01-01"

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

    @patch.object(JobModel, 'save')
    @freeze_time(frozen_datetime)
    def test_start(self, save_mock):


        job = JobModel()
        result = job.start()

        self.assertEqual(job.started, datetime.strptime(frozen_datetime, '%Y-%m-%d'))
        self.assertIsNone(job.ended)
        self.assertTrue(job.running)
        self.assertIsNone(job.error)
        save_mock.assert_called_once_with(_running__null=True)
        self.assertTrue(result)

    @patch.object(JobModel, 'save')
    @freeze_time(frozen_datetime)
    def test_start_when_job_is_alread_running(self, save_mock):

        save_mock.side_effect = PutError('ConditionalCheckFailedException')

        job = JobModel()
        result = job.start()

        self.assertEqual(job.started, datetime.strptime(frozen_datetime, '%Y-%m-%d'))
        self.assertIsNone(job.ended)
        self.assertTrue(job.running)
        self.assertIsNone(job.error)
        save_mock.assert_called_once_with(_running__null=True)
        self.assertFalse(result)

    @patch.object(JobModel, 'save')
    @freeze_time(frozen_datetime)
    def test_start_error(self, save_mock):

        save_mock.side_effect = PutError()

        job = JobModel()
        with self.assertRaises(PutError):
            result = job.start()

        self.assertEqual(job.started, datetime.strptime(frozen_datetime, '%Y-%m-%d'))
        self.assertIsNone(job.ended)
        self.assertTrue(job.running)
        self.assertIsNone(job.error)
        save_mock.assert_called_once_with(_running__null=True)

    def test_lastUpdated_getter_when_none(self):

        job = JobModel()
        result = job.lastUpdated

        self.assertIsNone(result)

    def test_lastUpdated_getter_when_not_none(self):

        job = JobModel()
        job._last_updated = 0
        result = job.lastUpdated

        self.assertEqual(result, datetime.utcfromtimestamp(0))

    @patch.object(JobModel, 'save')
    def test_lastUpdated_setter_when_none(self, save_mock):

        job = JobModel()
        job.lastUpdated = None

        self.assertIsNone(job._last_updated)
        save_mock.assert_called_with()

    @patch.object(JobModel, 'save')
    def test_lastUpdated_setter_when_not_none(self, save_mock):

        job = JobModel()
        job.lastUpdated = datetime.utcfromtimestamp(0)

        self.assertEqual(job._last_updated, 0)
        save_mock.assert_called_with()

    def test_started_getter_when_none(self):

        job = JobModel()
        result = job.started

        self.assertIsNone(result)

    def test_started_getter_when_not_none(self):

        job = JobModel()
        job._started = 0
        result = job.started

        self.assertEqual(result, datetime.utcfromtimestamp(0))

    def test_ended_getter_when_none(self):

        job = JobModel()
        result = job.started

        self.assertIsNone(result)

    def test_ended_getter_when_not_none(self):

        job = JobModel()
        job._started = 0
        result = job.started

        self.assertEqual(result, datetime.utcfromtimestamp(0))

    def test_running(self):

        job = JobModel()
        job._running = True
        result = job.running

        self.assertTrue(result)

    def test_error_getter(self):

        message = "test error message"

        job = JobModel()
        job._error = message
        result = job.error

        self.assertEqual(result, message)

    def test_error_setter(self):

        message = "test error message"

        job = JobModel()
        job.error = message
        result = job.error

        self.assertEqual(result, message)


    @freeze_time(frozen_datetime)
    @patch.object(JobModel, 'save')
    def test_stop(self, save_mock):

        job = JobModel()
        job.stop()

        self.assertEqual(job.ended, datetime.strptime(frozen_datetime, '%Y-%m-%d'))
        self.assertIsNone(job.running)

    @patch.object(JobModel, 'appId')
    @patch.object(JobModel, '__init__')
    @patch.object(pynamodb.models.Model, 'get')
    def test_get_when_item_exists(self, model_get_mock, init_mock, appId_mock):
        app_id = "test appId"
        init_mock.return_value = None
        appId_mock.return_value = app_id

        JobModel.get(self.config)

        model_get_mock.assert_called_once_with(app_id)
        init_mock.assert_not_called()

    @patch.object(JobModel, 'appId')
    @patch.object(JobModel, '__init__')
    @patch.object(pynamodb.models.Model, 'get')
    def test_get_when_item_exists(self, model_get_mock, init_mock, appId_mock):
        app_id = "test appId"

        init_mock.return_value = None
        appId_mock.return_value = app_id
        model_get_mock.side_effect = DoesNotExist()

        JobModel.get(self.config)
        model_get_mock.assert_called_once_with(app_id)
        init_mock.assert_called_once_with(app_id)
