import pynamodb.attributes
import pynamodb.models
from pynamodb.exceptions import DoesNotExist
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
    _last_updated = pynamodb.attributes.NumberAttribute()

    @property
    def lastUpdated(self):
        last_updated = self._last_updated or 0
        return fromModelDateTime(last_updated)

    @lastUpdated.setter
    def lastUpdated(self, last_updated):
        self._last_updated = last_updated
        self.save()

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

