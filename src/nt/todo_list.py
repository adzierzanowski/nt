'''This module handles most of the program's behavior.'''

import os
import sys
import json
import subprocess
from datetime import datetime as dt
from datetime import timedelta

from .todo_item import TodoItem
from .todo_list_config import TodoListConfig
from .constants import Constants
from .meta import __progname__

class TodoList:
  '''TodoList represents, wait for it... a todo list.'''

  def __init__(self):
    self.config = TodoListConfig()
    self.items = []
    self.max_id = -1

  @staticmethod
  def init():
    '''Initializes a list in the current directory. If a list exists, then it
    prints appropriate message to stderr and quits.'''

    if os.path.exists(Constants.list_fname):
      print('{} already exists'.format(Constants.list_fname), file=sys.stderr)
      print('remove it first with `{} rm list`'.format(__progname__),
        file=sys.stderr)
      exit(1)

    todo_list = TodoList()
    todo_list.to_file(force=True)
    print('successfully created {}'.format(Constants.list_fname))

  @staticmethod
  def from_file(fname):
    '''Returns an instance of TodoList based on data from a file.'''

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
    '''Returns a datetime.datetime instance based on an input string.'''

    if due_:
      for fmt in Constants.date_fmts:
        try:
          due = dt.strptime(due_, fmt)
          break
        except ValueError:
          weekdays = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

          if due_.lower() in weekdays:
            timeptr = dt.now() + timedelta(days=1)
            while all([
              timeptr.weekday() != weekdays.index(due_),
              timeptr - dt.now() < timedelta(days=8)
            ]):

              timeptr += timedelta(days=1)
            due = timeptr

          else:
            due = None
    else:
      due = None

    if due:
      now = dt.now()
      if due.year == 1900:
        due = due.replace(year=now.year)

    return due

  def get_item(self, id_):
    '''Returs a tuple (index, item) from list of items belonging to the list
    based on an item id. If the item is not found, it returns (-1, None).'''

    for index, item in enumerate(self.items):
      if item.id == id_:
        return index, item
    return -1, None

  def add_todo_item(self, item):
    '''Appends a TodoItem to the list's item list.'''

    self.items.append(item)

  def add_item(self, due_, content_, priority_):
    '''Adds an item to the list based on certain parameters.'''

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
    '''Updates TodoItem's fields.'''

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
    '''Marks an item as completed (or not).'''

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
    less=False,
    by_prefix=None):
    '''Lists items from the list.'''

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

    if by_prefix:
      prefix_groups = {'no prefix': []}

      for item in items:
        prefixes = item.get_prefixes(by_prefix)
        if prefixes:
          for prefix in prefixes:
            if prefix in prefix_groups:
              prefix_groups[prefix].append(item)
            else:
              prefix_groups[prefix] = [item]
        else:
          prefix_groups['no prefix'].append(item)

    out = ''
    if by_prefix:
      for group, items in prefix_groups.items():
        if group == 'no prefix':
          prefix_name = ''
          group_name = '~none'
        else:
          prefix_name = by_prefix
          group_name = group

        if items:
          out += '{}: \033[38;5;{}m{}{}\033[0m\n'.format(
            self.config.prefixes[by_prefix]['name'],
            self.config.prefixes[by_prefix]['color'],
            prefix_name,
            group_name)
          for item in items:
            out += str(item) + '\n'
    else:
      for item in items:
        out += str(item) + '\n'

    if less:
      with open(Constants.less_tmp_fname, 'w') as f:
        f.write(out)
      subprocess.call(['less', '-R', Constants.less_tmp_fname])
      os.remove(Constants.less_tmp_fname)
    else:
      print(out)

  def to_file(self, force=False):
    '''Saves the current state of the list to a file.'''

    if os.path.exists(Constants.list_fname) or force:
      with open(Constants.list_fname, 'w') as f:
        f.write(self.to_json())
    else:
      print('{} not found'.format(Constants.list_fname))
      print('init list with `nt init`')

  def to_json(self):
    '''Returns a JSON representation of the class' data.'''

    data = {
      'config': self.config.to_dict(),
      'items': [item.to_dict() for item in self.items]
    }
    return json.dumps(data)
