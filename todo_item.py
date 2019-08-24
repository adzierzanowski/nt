from datetime import datetime as dt

from constants import Constants

class TodoItem:
  def __init__(self, id_, content, due_date, priority, completed=False):
    self.id = id_
    self.content = content
    self.due_date = due_date
    self.priority = priority
    self.completed = completed

  def __str__(self):
    completed = 'x' if self.completed else ' '
    due = '' if self.due_date is None else 'due: \033[38;5;2m' + self.due_date.strftime(Constants.date_fmt) + '\033[0m'
    priority = '' if self.priority is None else 'priority: \033[38;5;3m' + str(self.priority) + '\033[0m'
    return '\033[38;5;4m{:4}\033[0m [{}]    {} {}\n     {}'.format(
      self.id, completed, due, priority, self.content)
    
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
