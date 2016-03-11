# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import Mock
from bluekai.sftpproxy import *

frozen_datetime="2016-01-01"

class SftpProxy_test(TestCase):

    def setUp(self):
        self.config = {
            'REMOTE_HOST': "http://example.com",
            'REMOTE_PORT': 22,
            'REMOTE_USERNAME': "testuser",
            'REMOTE_RSA_KEY': "",
            'REMOTE_PASSWORD': "",
        }
        self.remote_password = "test_remote_password"
        self.remote_rsa_key = "test_remote_rsa_key"
        self.name = "test_name"
        self.logger_mock = Mock(name="logger")
        self.sftp_mock = Mock(name="sftp")
        self.pkey_mock = Mock(name="pkey")
        self.transport_mock = Mock(name="transport")
        self.paramiko_mock = Mock(name="paramiko")
        self.paramiko_mock.Transport.return_value = self.transport_mock
        self.paramiko_mock.RSAKey.from_private_key_file.return_value = self.pkey_mock
        self.paramiko_mock.SFTPClient.from_transport.return_value = self.sftp_mock

    def test_init_password(self):

        self.config['REMOTE_PASSWORD'] = self.remote_password

        sftpProxy = SftpProxy(self.paramiko_mock, self.config, self.logger_mock)

        self.paramiko_mock.Transport.assert_called_once_with(
            (self.config['REMOTE_HOST'], self.config['REMOTE_PORT'])
        )
        self.transport_mock.use_compression.assert_called_once_with()
        self.transport_mock.connect.assert_called_once_with(
            **{
                "username": self.config['REMOTE_USERNAME'],
                "password": self.config['REMOTE_PASSWORD'],
            }
        )
        self.paramiko_mock.SFTPClient.from_transport.assert_called_once_with(self.transport_mock)
        self.assertIs(sftpProxy.transport, self.transport_mock)
        self.assertIs(sftpProxy.sftp, self.sftp_mock)

    def test_init_connection_error(self):
        self.transport_mock.connect.side_effect = Exception()

        with self.assertRaises(Exception):
            sftpProxy = SftpProxy(self.paramiko_mock, self.config, self.logger_mock)

        self.paramiko_mock.Transport.assert_called_once_with(
            (self.config['REMOTE_HOST'], self.config['REMOTE_PORT'])
        )
        self.transport_mock.use_compression.assert_called_once_with()
        self.transport_mock.connect.assert_called_once_with(
            **{
                "username": self.config['REMOTE_USERNAME'],
                "password": self.config['REMOTE_PASSWORD'],
            }
        )
        self.paramiko_mock.SFTPClient.from_transport.assert_not_called()

    def test_init_rsa_key(self):

        self.config['REMOTE_RSA_KEY'] = self.remote_rsa_key

        sftpProxy = SftpProxy(self.paramiko_mock, self.config, self.logger_mock)

        self.paramiko_mock.Transport.assert_called_once_with(
            (self.config['REMOTE_HOST'], self.config['REMOTE_PORT'])
        )
        self.transport_mock.use_compression.assert_called_once_with()
        self.paramiko_mock.RSAKey.from_private_key_file.assert_called_once_with(
            self.config['REMOTE_RSA_KEY']
        )
        self.transport_mock.connect.assert_called_once_with(
            **{
                "username": self.config['REMOTE_USERNAME'],
                "pkey": self.pkey_mock,
            }
        )
        self.paramiko_mock.SFTPClient.from_transport.assert_called_once_with(self.transport_mock)
        self.assertIs(sftpProxy.transport, self.transport_mock)
        self.assertIs(sftpProxy.sftp, self.sftp_mock)

    def test_init_rsa_key_with_password(self):

        self.config['REMOTE_RSA_KEY'] = self.remote_rsa_key
        self.config['REMOTE_PASSWORD'] = self.remote_password

        sftpProxy = SftpProxy(self.paramiko_mock, self.config, self.logger_mock)

        self.paramiko_mock.Transport.assert_called_once_with(
            (self.config['REMOTE_HOST'], self.config['REMOTE_PORT'])
        )
        self.transport_mock.use_compression.assert_called_once_with()
        self.paramiko_mock.RSAKey.from_private_key_file.assert_called_once_with(
            self.config['REMOTE_RSA_KEY'],
            password=self.config['REMOTE_PASSWORD'],
        )
        self.transport_mock.connect.assert_called_once_with(
            **{
                "username": self.config['REMOTE_USERNAME'],
                "pkey": self.pkey_mock,
            }
        )
        self.paramiko_mock.SFTPClient.from_transport.assert_called_once_with(self.transport_mock)
        self.assertIs(sftpProxy.transport, self.transport_mock)
        self.assertIs(sftpProxy.sftp, self.sftp_mock)

    def test_getattr(self):
        sftpProxy = SftpProxy(self.paramiko_mock, self.config, self.logger_mock)
        result = sftpProxy.get(self.name)

