import argparse

def parse_args():
  parser = argparse.ArgumentParser('nt')

  parser.add_argument(
    '-v', '--version',
    help='print version',
    action='store_true'
  )

  subparsers = parser.add_subparsers(dest='cmd')
  new_parser = subparsers.add_parser('new', help='new note')
  ls_parser = subparsers.add_parser('ls', help='list objects')

  args = parser.parse_args()
  return parser, args
