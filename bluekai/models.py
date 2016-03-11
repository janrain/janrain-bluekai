import pynamodb.attributes
import pynamodb.models
from pynamodb.exceptions import DoesNotExist
from datetime import datetime
from .config import get_config
from .date_utils import fromModelDateTime
from .date_utils import toModelDateTime

config = get_config()

class JobModel(pynamodb.models.Model):
    """DyanmoDB table structure."""

    class Meta:
        region = config['AWS_DEFAULT_REGION']
        table_name = config['AWS_DYNAMODB_TABLE']
        host = config['AWS_DYNAMODB_URL']

    app_id = pynamodb.attributes.UnicodeAttribute(hash_key=True)
    _last_updated = pynamodb.attributes.NumberAttribute(null=True)
    _started = pynamodb.attributes.NumberAttribute(null=True)
    _ended = pynamodb.attributes.NumberAttribute(null=True)
    _running = pynamodb.attributes.BooleanAttribute(null=True)
    _error = pynamodb.attributes.UnicodeAttribute(null=True)

    def start(self):
        """Start the job. Can only be started if not currently running.

        Args:
            filename: name of file

        Returns:
            bool (whether start succeeded)
        """
        self._started = toModelDateTime(datetime.now())
        self._ended = None
        self._running = True
        self._error = None
        try:
            # only start job if not currently running
            self.save(_running__null=True)
        except pynamodb.exceptions.PutError as ex:
            if 'ConditionalCheckFailedException' in str(ex):
                return False
            raise
        return True

    def stop(self):
        """Stop the job."""
        self._ended = toModelDateTime(datetime.now())
        self._running = None

    @property
    def lastUpdated(self):
        last_updated = self._last_updated
        if last_updated is not None:
            return fromModelDateTime(last_updated)
        else:
            return None

    @lastUpdated.setter
    def lastUpdated(self, last_updated):
        self._last_updated = last_updated and toModelDateTime(last_updated)
        self.save()

    @property
    def started(self):
        started = self._started
        if started is not None:
            return fromModelDateTime(started)
        else:
            return None

    @property
    def ended(self):
        ended = self._ended
        if ended is not None:
            return fromModelDateTime(ended)
        else:
            return None

    @property
    def running(self):
        return self._running

    @property
    def error(self):
        return self._error

    @classmethod
    def get(cls, config):
        app_id = cls.appId(config)
        try:
          return super(JobModel, cls).get(app_id)
        except DoesNotExist:
          return cls(app_id)

    @classmethod
    def appId(cls, config):
        janrain_uri = config.get('JANRAIN_URI')
        janrain_schema_name = config.get('JANRAIN_SCHEMA_NAME')
        return "{}:{}".format(janrain_uri, janrain_schema_name)
