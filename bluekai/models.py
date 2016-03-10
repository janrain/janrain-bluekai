import pynamodb.attributes
import pynamodb.exceptions
import pynamodb.models
from .config import get_config
from .date_utils import fromModelDateTime
from .date_utils import toModelDateTime

config = get_config()

class Model(pynamodb.models.Model):
    """DyanmoDB table structure."""

    class Meta:
        region = config['AWS_DEFAULT_REGION']
        table_name = config['AWS_DYNAMODB_TABLE']
        host = config['AWS_DYNAMODB_URL']

    app_id = pynamodb.attributes.UnicodeAttribute(hash_key=True)
    last_updated = pynamodb.attributes.NumberAttribute()

    def update(self, last_updated):
      self.last_updated = last_updated
      self.save()

def loadLastUpdated(modelClass, config):
    item = getItem(modelClass, config)
    last_updated = item.last_updated or 0
    return fromModelDateTime(last_updated)

def saveLastUpdated(modelClass, config, lastUpdated):
    item = getItem(modelClass, config)
    item.update(toModelDateTime(lastUpdated))

def appId(config):
    return "{}:{}".format(config['JANRAIN_URI'], config['JANRAIN_SCHEMA_NAME'])

def getItem(modelClass, config):
    app_id = appId(config)
    try:
        return modelClass.get(app_id)
    except DoesNotExist:
        return modelClass(app_id)
