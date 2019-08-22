import datetime as dt
import hashlib

class NTEntity:
  def __init__(self, type_, dir_):
    self.timestamp = dt.datetime.now().timestamp()
    self.dir = dir_
    self.type = type_
    self.uid = hashlib.sha256(
      '{}{}{}'.format(
        self.type, self.dir, self.timestamp).encode('ascii')).hexdigest()
