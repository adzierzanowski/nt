import os
import json

from todo_item import TodoItem
from todo_list_config import TodoListConfig
from constants import Constants

class TodoList:
  def __init__(self):
    self.config = TodoListConfig()
    self.items = []
    self.max_id = -1

  def add_item(self, item):
    self.items.append(item)

  @staticmethod
  def from_file(fname):
    todo_list = TodoList()
    try:
      with open(fname, 'r') as f:
        data = json.load(f)

      todo_list.config = TodoListConfig.from_json(data['config'])

      for item in data['items']:
        item = TodoItem.from_json(item)
        todo_list.items.append(item)
        if item.id > todo_list.max_id:
          todo_list.max_id = item.id
      
      return todo_list

    except FileNotFoundError:
      print('{} not found', Constants.list_fname)
      print('init list with `nt init`')

  def to_file(self):
    if os.path.exists(Constants.list_fname):
      with open(Constants.list_fname, 'w') as f:
        f.write(self.to_json())
    else:
      print('{} not found', Constants.list_fname)
      print('init list with `nt init`')

  def to_json(self):
    data = {
      'config': self.config.to_dict(),
      'items': [item.to_dict() for item in self.items]
    }
    return json.dumps(data)
