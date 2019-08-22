import json
import datetime as dt
from ntentity import NTEntity

class NTNote(NTEntity):
  def __init__(self, dir_, title, content, date=None):
    NTEntity.__init__(self, type(self), dir_)
    self.title = title
    self.content = content
    self.date = dt.datetime.now() if date is None else date

  def to_json(self):
    out = {
      'title': self.title,
      'content': self.content,
      'date': self.date.strftime('%d.%m.%Y %H:%M:%S')
    }

    return json.dumps(out)
