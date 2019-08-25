import os
import sys
import json
import subprocess
from datetime import datetime as dt

from .todo_item import TodoItem
from .todo_list_config import TodoListConfig
from .constants import Constants

class TodoList:
  def __init__(self):
    self.config = TodoListConfig()
    self.items = []
    self.max_id = -1

  @staticmethod
  def init():
    if os.path.exists(Constants.list_fname):
      print('{} already exists'.format(Constants.list_fname))
      print('remove it first with `nt rm list`')
      exit(1)

    todo_list = TodoList()
    todo_list.to_file(force=True)
    print('successfully created {}'.format(Constants.list_fname))

  @staticmethod
  def from_file(fname):
    todo_list = TodoList()
    try:
      with open(fname, 'r') as f:
        data = json.load(f)

      todo_list.config = TodoListConfig.from_json(data['config'])

      for item in data['items']:
        item = TodoItem.from_json(todo_list, item)
        todo_list.items.append(item)
        if item.id > todo_list.max_id:
          todo_list.max_id = item.id

      return todo_list

    except FileNotFoundError:
      return None

  @staticmethod
  def parse_date(due_):
    if due_:
      for fmt in Constants.date_fmts:
        try:
          due = dt.strptime(due_, fmt)
          break
        except ValueError:
          due = None
    else:
      due = None

    if due:
      now = dt.now()
      if due.year == 1900:
        due = due.replace(year=now.year)

    return due

  def get_item(self, id_):
    for index, item in enumerate(self.items):
      if item.id == id_:
        return index, item
    return -1, None

  def add_todo_item(self, item):
    self.items.append(item)

  def add_item(self, due_, content_, priority_):
    due = TodoList.parse_date(due_)

    item = TodoItem(
      self,
      self.max_id+1,
      ' '.join(content_),
      due,
      priority_)
    self.add_todo_item(item)
    self.to_file()
    print(item)

  def edit_item(self, id_, content_, due_, priority_):
    i, item = self.get_item(id_)
    if item:
        if content_:
          self.items[i].content = content_
        if priority_:
          self.items[i].priority = priority_
        if due_:
          due = TodoList.parse_date(due_)
          self.items[i].due_date = due
        self.to_file()
        print(item)
        return True
    return False

  def set_completeness(self, id_, complete):
    i, item = self.get_item(id_)
    if item:
      self.items[i].completed = complete
      self.to_file()
      print(item)
      return True
    return False

  def list_items(
    self,
    priority=False,
    due=False,
    all_=False,
    completed=False,
    uncompleted=False,
    args=None,
    less=False):
    items = self.items

    if priority:
      items = sorted(items,
        key=lambda m: 0 if m.priority is None else -m.priority)

    if due:
      items = sorted(items,
      key=lambda m: dt(1900, 1, 1) if m.due_date is None else m.due_date,
      reverse=True)

    if not all_:
      if completed:
        items = [item for item in items if item.completed]
      elif uncompleted:
        items = [item for item in items if not item.completed]

    for arg in args:
      items = [item for item in items if arg in item.content]

    if less:
      with open(Constants.less_tmp_fname, 'w') as f:
        out = ''
        for item in items:
          out += str(item) + '\n'
        f.write(out)

      subprocess.call(['less', '-R', Constants.less_tmp_fname])
      os.remove(Constants.less_tmp_fname)

    else:
      for item in items:
          print(item)

  def to_file(self, force=False):
    if os.path.exists(Constants.list_fname) or force:
      with open(Constants.list_fname, 'w') as f:
        f.write(self.to_json())
    else:
      print('{} not found'.format(Constants.list_fname))
      print('init list with `nt init`')

  def to_json(self):
    data = {
      'config': self.config.to_dict(),
      'items': [item.to_dict() for item in self.items]
    }
    return json.dumps(data)
