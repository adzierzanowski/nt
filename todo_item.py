from datetime import datetime as dt

from constants import Constants

class TodoItem:
  def __init__(self, id_, content, due_date, priority, completed=False):
    self.id = id_
    self.content = content
    self.due_date = due_date
    self.priority = priority
    self.completed = completed

  def __repr__(self):
    return str(self)

  def __str__(self):
    completed = 'x' if self.completed else ' '
    due = '' if self.due_date is None else self.due_date.strftime(Constants.date_fmt)
    priority = '' if self.priority is None else self.priority
    return '{:4} [{}] {:40} {:20} {}'.format(
      self.id, completed, self.content, due, priority)
    
  @staticmethod
  def from_json(data):
    item = TodoItem(
      data['id'],
      data['content'],
      None if data['due_date'] is None else dt.strptime(data['due_date'], Constants.date_fmt),
      data['priority'],
      data['completed']
    )
    return item

  def to_dict(self):
    due = None if self.due_date is None else self.due_date.strftime(Constants.date_fmt)
    data = {
      'id': self.id,
      'content': self.content,
      'due_date': due,
      'priority': self.priority,
      'completed': self.completed
    }
    return data
