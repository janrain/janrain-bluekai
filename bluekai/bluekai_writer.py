from . import bluekai_trigger
from .config import remote_filename

class BlueKaiWriter():
    def __init__(self, writer, config):
        (self.data_filename, self.trigger_filename) = remote_filename(config)
        self.data_fp = writer.file(self.data_filename, mode='w')
        self.trigger_fp = writer.file(self.trigger_filename, mode='w')

    def write(self, data):
        trigger_data = bluekai_trigger.fromData(self.data_filename, data)
        self.data_fp.write(data)
        self.trigger_fp.write(trigger_data)

    def close(self):
        self.data_fp.close()
        self.trigger_fp.close()

