"""Sftp proxy"""
import io
import paramiko

class SftpProxy:

    def __init__(self, config, logger):
        # connect to remote
        remote = (config['REMOTE_HOST'], config['REMOTE_PORT'])
        self.transport = paramiko.Transport(remote)
        self.transport.use_compression()
        kwargs = {
            'username': config['REMOTE_USERNAME'],
        }
        # rsa key authentication
        if config['REMOTE_RSA_KEY']:
            key_file = config['REMOTE_RSA_KEY']
            if config['REMOTE_PASSWORD']:
                # decrypt the key
                kwargs['pkey'] = paramiko.RSAKey.from_private_key_file(key_file, password=config['REMOTE_PASSWORD'])
            else:
                kwargs['pkey'] = paramiko.RSAKey.from_private_key_file(key_file)
        # password only authentication
        else:
            kwargs['password'] = config['REMOTE_PASSWORD']

        try:
            self.transport.connect(**kwargs)
        except Exception as ex:
            logger.error("error connecting to remote: {}".format(ex))
            raise
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def __getattr__(self, name):
        return getattr(self.sftp, name)
