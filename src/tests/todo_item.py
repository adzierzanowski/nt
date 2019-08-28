import unittest
from datetime import datetime as dt

from nt.todo_item import TodoItem
from nt.todo_list import TodoList

class TodoItemTest(unittest.TestCase):
  def setUp(self):
    self.content = 'Hello @context, I am working on my +project regarding #tag and #another-tag'
    self.todo_item = TodoItem(
      parent=TodoList(),
      id=0,
      content=self.content,
      priority=10,
      due_date=dt(2020, 1, 1, 12, 0),
      completed=False
    )

  def test_init(self):
    self.assertIsNotNone(self.todo_item.parent)
    self.assertEqual(self.todo_item.id, 0)
    self.assertEqual(self.todo_item.priority, 10)
    self.assertEqual(self.todo_item.due_date, dt(2020, 1, 1, 12, 0))
    self.assertEqual(self.todo_item.content, self.content)
    self.assertFalse(self.todo_item.completed)

  def test_str(self):
    s = str(self.todo_item)

    self.assertIn('0', s)
    self.assertIn(self.content.split(' ')[0], s)
    self.assertIn(str('10'), s)

  def test_contexts(self):
    self.assertEqual(['context'], self.todo_item.get_prefixes('@'))

  def test_projects(self):
    self.assertEqual(['project'], self.todo_item.get_prefixes('+'))

  def test_tags(self):
    prefixes = self.todo_item.get_prefixes('#')
    self.assertIn('tag', prefixes)
    self.assertIn('another-tag', prefixes)
  
  def test_from_dict(self):
    item_dict = {
      'id': 1,
      'content': 'Hello, world',
      'priority': None,
      'completed': True,
      'due_date': '22.06.19 12:12',
    }
    item = TodoItem.from_dict(self.todo_item.parent, item_dict)

    self.assertEqual(item.id, 1)
    self.assertEqual(item.content, 'Hello, world')
    self.assertIsNone(item.priority, 1)
    self.assertTrue(item.completed)
    self.assertEqual(item.due_date, dt(2019, 6, 22, 12, 12))

  def test_to_dict(self):
    d = self.todo_item.to_dict()

    self.assertIn('id', d)
    self.assertIn('content', d)
    self.assertIn('priority', d)
    self.assertIn('due_date', d)
    self.assertIn('completed', d)

    self.assertEqual(d['id'], 0)
    self.assertEqual(d['content'], self.content)
    self.assertEqual(d['priority'], 10)
    self.assertEqual(d['due_date'], dt(2020, 1, 1, 12, 0).strftime('%d.%m.%y %H:%M'))
    self.assertFalse(d['completed'])
