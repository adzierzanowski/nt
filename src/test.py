#!/usr/bin/env python3

import unittest

from tests import todo_item, todo_list_config

if __name__ == '__main__':
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTests([
    loader.loadTestsFromModule(todo_item),
    loader.loadTestsFromModule(todo_list_config),
  ])

  runner = unittest.TextTestRunner(verbosity=3)
  runner.run(suite)
