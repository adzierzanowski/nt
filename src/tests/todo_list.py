import os
import unittest
from datetime import datetime as dt

from nt.todo_list import TodoList
from nt.todo_list_config import TodoListConfig

class TodoListTestWithoutItems(unittest.TestCase):
  def setUp(self):
    self.todo_list = TodoList()

  def test_init_(self):
    '''__init__()'''

    self.assertIsNotNone(self.todo_list)
    self.assertIsInstance(self.todo_list.config, TodoListConfig)
    self.assertEqual(self.todo_list.items, [])
    self.assertEqual(self.todo_list.max_id, -1)

class TodoListTestWithItems(unittest.TestCase):
  def setUp(self):
    self.todo_list = TodoList()
    self.todo_list.add_item('tue', '@context1 +project1 #tag1 hello world', 10)
    self.todo_list.add_item('25.06', '@context1 +project1 #tag2 content', 9)
    self.todo_list.add_item(
      '18.01.21 12:00', '@context1 +project2 #tag2 goodbye', 8)

  def test_init(self):
    '''init()'''

    try:
      self.todo_list.init()
    except SystemExit:
      pass

    self.assertTrue(os.path.exists('.todo.json'))
    os.remove('.todo.json')

  def test_parse_date(self):
    self.assertEqual(TodoList.parse_date('mon').weekday(), 0)
    self.assertEqual(TodoList.parse_date('Tue').weekday(), 1)
    self.assertEqual(TodoList.parse_date('WED').weekday(), 2)
    self.assertEqual(TodoList.parse_date('THu').weekday(), 3)
    self.assertEqual(TodoList.parse_date('fRI').weekday(), 4)
    self.assertEqual(TodoList.parse_date('saT').weekday(), 5)
    self.assertEqual(TodoList.parse_date('Sun').weekday(), 6)

    self.assertEqual(
      TodoList.parse_date('22.06.20 18:19'), dt(2020, 6, 22, 18, 19))

    self.assertEqual(TodoList.parse_date('22.06'), dt(2019, 6, 22))

  def test_group_by_prefix(self):
    pass

  def test_get_item(self):
    _, item = self.todo_list.get_item(0)

    self.assertIsNotNone(item)
    self.assertEqual(item.id, 0)

    index, item = self.todo_list.get_item(100)
    self.assertIsNone(item)
    self.assertEqual(index, -1)

  def test_add_item(self):
    item = self.todo_list.add_item('sat', 'content', None)
    self.assertIsNotNone(item)
    self.assertIn(item, self.todo_list.items)
    self.assertEqual(self.todo_list.max_id, 3)

  def test_remove_item(self):
    _, item0 = self.todo_list.get_item(0)
    _, item1 = self.todo_list.get_item(1)
    _, item2 = self.todo_list.get_item(2)

    self.todo_list.remove_item(0)
    self.assertEqual(self.todo_list.max_id, 2)

    self.todo_list.remove_item(2)
    self.assertEqual(self.todo_list.max_id, 1)

    self.assertNotIn(item0, self.todo_list.items)
    self.assertIn(item1, self.todo_list.items)
    self.assertNotIn(item2, self.todo_list.items)

  def test_set_completness(self):
    self.todo_list.set_completeness(0, False)
    self.todo_list.set_completeness(1, True)

    _, item0 = self.todo_list.get_item(0)
    _, item1 = self.todo_list.get_item(1)

    self.assertFalse(item0.completed)
    self.assertTrue(item1.completed)

  def test_edit_item(self):
    self.todo_list.edit_item(0, 'barf', None, 1)
    _, item = self.todo_list.get_item(0)

    self.assertEqual(item.content, 'barf')
    self.assertIsNotNone(item.due_date)
    self.assertEqual(item.priority, 1)
