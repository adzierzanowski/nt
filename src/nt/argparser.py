'''This module parses command line arguments.'''

import argparse

from .meta import __progname__
from .glob import Glob

def parse_args():
  '''Define and parse command line arguments.
  Returns a tuple (parser, args)'''

  parser = argparse.ArgumentParser(__progname__)

  subparsers = parser.add_subparsers(dest='cmd')
  subparsers.add_parser('init')
  add_subparser = subparsers.add_parser(
    'add', aliases=['a'], help='add an item')
  cfg_subparser = subparsers.add_parser(
    'config', aliases=['cfg'], help='configure')
  edit_subparser = subparsers.add_parser(
    'edit', aliases=['e'], help='edit an item')
  rm_subparser = subparsers.add_parser(
    'rm', aliases=['r', 'd'], help='remove an item')
  ls_subparser = subparsers.add_parser(
    'ls', aliases=['l', 'i', 'items'], help='list items')
  complete_subparser = subparsers.add_parser(
    'complete', aliases=['c'], help='mark an item as completed')
  uncomplete_subparser = subparsers.add_parser(
    'uncomplete', aliases=['u'], help='mark an item as uncompleted')

  parser.add_argument(
    '-v', '--version', help='print version', action='store_true')

  add_subparser.add_argument('content', help='content', nargs='*')
  add_subparser.add_argument('-d', '--due', help='due date', type=str)
  add_subparser.add_argument('-p', '--priority', help='priority', type=int)

  cfg_subparser.add_argument(
    '-a', '--add-prefix', help='add a new prefix', type=str, metavar='SYMBOL')
  cfg_subparser.add_argument(
    '-c', '--color', type=int, metavar='N', help='color number')
  cfg_subparser.add_argument(
    '-n', '--name', help='prefix name', metavar='NAME', type=str)
  cfg_subparser.add_argument(
    '-r', '--remove-prefix', type=str, metavar='SYMBOL')

  edit_subparser.add_argument('id', help='id', type=int)
  edit_subparser.add_argument('-c', '--content', help='content', type=str)
  edit_subparser.add_argument('-d', '--due', help='due date', type=str)
  edit_subparser.add_argument('-p', '--priority', help='priority', type=int)

  rm_subparser.add_argument('id', help='item id', type=str)

  complete_subparser.add_argument('id', help='item id', type=int)
  uncomplete_subparser.add_argument('id', help='item id', type=int)

  ls_subparser.add_argument('args', help='arguments', type=str, nargs='*')
  ls_subparser.add_argument(
    '-a', '--all', help='show all', action='store_true')
  ls_subparser.add_argument(
    '-b', '--by-prefix', help='group by prefix', type=str)
  ls_subparser.add_argument(
    '-c', '--completed', help='show only completed', action='store_true')
  ls_subparser.add_argument(
    '-d', '--due', help='sort by due date', action='store_true')
  ls_subparser.add_argument(
    '-l', '--less', help='pipe the output to less',
    action='store_false' if Glob.default_less_pipe else 'store_true')
  ls_subparser.add_argument(
    '-o', '--overdue', help='list overdue', action='store_true')
  ls_subparser.add_argument(
    '-p', '--priority', help='sort by priority', action='store_true')
  ls_subparser.add_argument(
    '-u', '--uncompleted',
    help='show only uncompleted', action='store_false')

  args = parser.parse_args()

  return args, parser
