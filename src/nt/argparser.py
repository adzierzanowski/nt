import argparse

from .meta import __progname__

def parse_args():
  parser = argparse.ArgumentParser(__progname__)

  subparsers = parser.add_subparsers(dest='cmd')
  subparsers.add_parser('init')
  add_subparser = subparsers.add_parser('add', aliases=['a'])
  edit_subparser = subparsers.add_parser('edit', aliases=['e'])
  rm_subparser = subparsers.add_parser('rm', aliases=['r', 'd'])
  ls_subparser = subparsers.add_parser('ls', aliases=['l'])
  complete_subparser = subparsers.add_parser('complete', aliases=['c'])
  uncomplete_subparser = subparsers.add_parser('uncomplete', aliases=['u'])

  parser.add_argument(
    '-v', '--version', help='print version', action='store_true')

  add_subparser.add_argument('content', help='content', nargs='*')
  add_subparser.add_argument('-d', '--due', help='due date', type=str)
  add_subparser.add_argument('-p', '--priority', help='priority', type=int)

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
    '-l', '--less', help='pipe the output to less', action='store_true')
  ls_subparser.add_argument(
    '-p', '--priority', help='sort by priority', action='store_true')
  ls_subparser.add_argument(
    '-u', '--uncompleted',
    help='show only uncompleted', action='store_false')

  args = parser.parse_args()

  return args, parser
