'''This module handles single todo list items.'''

from dataclasses import dataclass
from datetime import datetime as dt

from . import glob
from .glob import f

@dataclass
class TodoItem:
  '''TodoItem is a direct mapping of JSON data.'''

  parent: object
  id: int
  content: str
  due_date: dt
  priority: int
  completed: bool

  def __str__(self):
    if self.completed:
      completed = self.parent.config.completed_str
    else:
      completed = self.parent.config.uncompleted_str

    if self.due_date is None:
      due = ''
    else:
      if dt.now() < self.due_date:
        fmt = 'due'
      else:
        fmt = 'overdue'
      due = f'{f:{fmt}}{self.due_date.strftime(glob.date_fmt)}{f:e}'

    p = '' if self.priority is None else self.priority
    priority = f'{f:priority}{p}{f:e}'

    content = self.content.split(' ')
    for i, word in enumerate(content):
      for prefix, prefix_data in self.parent.config.prefixes.items():
        if word.startswith(prefix):
          color = prefix_data['color']
          content[i] = f'{f:fg({color})}{word}{f:e}'
          continue
    content = ' '.join(content)

    out = f'{f:index}{self.id:4}{f:e}    {completed:30}    {priority}\n'
    out += f'    {content}\n'
    return out

  @staticmethod
  def from_dict(parent, data):
    '''Returns a TodoItem from dictionary. The first argument specifies a
    TodoList to which the TodoItem belongs.'''

    if data['due_date'] is None:
      due = None
    else:
      due = dt.strptime(data['due_date'], glob.date_fmt)

    item = TodoItem(
      parent=parent,
      id=data['id'],
      content=data['content'],
      due_date=due,
      priority=data['priority'],
      completed=data['completed']
    )
    return item

  def to_dict(self):
    '''Returns a dict representation of the class.'''

    if self.due_date is None:
      due = None
    else:
      due = self.due_date.strftime(glob.date_fmt)

    data = {
      'id': self.id,
      'content': self.content,
      'due_date': due,
      'priority': self.priority,
      'completed': self.completed
    }
    return data

  def get_prefixes(self, prefix):
    '''Returns a list of words in TodoItem content that begins with a
    certain prefix.'''

    prefixes = []
    for word in self.content.split(' '):
      if word.startswith(prefix):
        prefixes.append(word[1:].strip('\t.,;:/'))
    return prefixes
