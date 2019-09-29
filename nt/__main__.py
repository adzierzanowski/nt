#!/usr/bin/env python3

import os
import sys
import shlex
import subprocess

from . import glob
from .glob import f
from .todo_list import TodoList, PrefixNotDefined, NoMatchingItems
from .argparser import parse_args
from .meta import __progname__, __version__

def edit_command(cmd, args=None, content=''):
  def abort_with_msg(msg):
    print(f'{f:error}{msg}{f:e}', file=sys.stderr)
    os.remove(glob.command_tmp_fname)
    exit(1)

  if args is None:
    args = []

  with open(glob.command_tmp_fname, 'w') as f:
    f.write(content)
  
  editor_retcode = subprocess.call(
    [glob.editor, glob.command_tmp_fname])

  if editor_retcode:
    abort_with_msg('error: editor returned {}'.format(editor_retcode))

  with open(glob.command_tmp_fname, 'r') as f:
    fcmd = shlex.split(f.read())
    if fcmd == []:
      abort_with_msg('aborting due to empty command')

    retcode = subprocess.call([__progname__, cmd] + args + fcmd)
    if retcode:
      abort_with_msg('something went wrong')

    os.remove(glob.command_tmp_fname)

def parse_rcfile():
  rcfname = os.path.expanduser(glob.rcfile)

  if os.path.exists(glob.rcfile):
    rcfname = glob.rcfile
  elif os.path.exists(os.path.join(os.path.expanduser('~'), glob.rcfile)):
    rcfname = os.path.join(os.path.expanduser('~'), glob.rcfile)
  else:
    return

  with open(rcfname, 'r') as fh:
    data = fh.read()

  data = data.splitlines()
  date_fmt_cnt = 0
  for line in data:
    l = line.split('=')

    if l[0] == 'editor':
      glob.editor = l[1]

    elif l[0] == 'list_fname':
      glob.list_fname = l[1]

    elif l[0] == 'completed_str':
      glob.completed_str = l[1]

    elif l[0] == 'uncompleted_str':
      glob.uncompleted_str = l[1]

    elif l[0] == 'pretty_json':
      if l[1].lower() == 'true':
        glob.pretty_json = True

    elif l[0] == 'default_less_pipe':
      if l[1].lower() == 'true':
        glob.default_less_pipe = True

    elif l[0] == 'date_fmt':
      date_fmt_cnt += 1
      if date_fmt_cnt == 1:
        glob.date_fmt = l[1]
      glob.date_fmts += l[1]

def main():
  parse_rcfile()
  args, parser = parse_args()

  if args.directory:
    os.chdir(args.directory)

  if args.version:
    print('{} version {}'.format(__progname__, __version__))
    exit(0)

  if args.cmd is None:
    subprocess.call([__progname__, 'ls'])
    exit(0)

  if args.cmd == 'init':
    if TodoList.init():
      print(f'{f:success}successfully created {glob.list_fname}{f:e}')
      exit(0)
    else:
      exit(1)

  todo_list = TodoList.from_file(glob.list_fname)
  if not todo_list:
    print(f'{f:error}{glob.list_fname} not found{f:e}', file=sys.stderr)
    print('init first with `{} init`'.format(__progname__), file=sys.stderr)
    exit(1)

  # cmd:add
  if args.cmd in ('a', 'add'):
    if args.content:
      item = todo_list.add_item(args.due, args.content, args.priority)
      todo_list.to_file()
      print(item)
    else:
      edit_command('add')
    exit(0)

  # cmd:cfg
  if args.cmd in ('cfg', 'config'):
    if args.add_prefix:
      if any([not args.name, not args.color]):
        print(
          '{f:error}-n and -c switches are required when adding a prefix{f:e}',
          file=sys.stderr)
        exit(1)
      todo_list.config.add_prefix(args.add_prefix, args.name, args.color)
      todo_list.to_file()
      exit(0)

    elif args.remove_prefix:
      todo_list.config.remove_prefix(args.remove_prefix)
      todo_list.to_file()
      exit(0)

    else:
      todo_list.config.dump()

  # cmd:edit
  if args.cmd in ('e', 'edit'):
    if any([args.content, args.due, args.priority]):
      if todo_list.edit_item(args.id, args.content, args.due, args.priority):
        _, item = todo_list.get_item(args.id)
        todo_list.to_file()
        print(item)
        exit(0)
      else:
        print(f'{f:error}no such item{f:e}', file=sys.stderr)
        exit(1)
    else:
      _, item = todo_list.get_item(args.id)
      if item:
        content = '-c \'{}\''.format(item.content)
        if item.priority:
          content += ' -p {}'.format(item.priority)
        if item.due_date:
          content += ' -d \'{}\''.format(item.due_date.strftime(glob.date_fmt))

        edit_command('edit', args=[str(args.id)], content=content)

      else:
        print(f'{f:error}no such item{f:e}', file=sys.stderr)
        exit(1)
    exit(0)

  # cmd:ls
  if args.cmd in ('l', 'ls', 'i', 'items'):
    try:
      todo_list.list_items(
        priority=args.priority,
        due=args.due,
        all_=args.all,
        completed=args.completed,
        uncompleted=args.uncompleted,
        args=args.args,
        less=args.less,
        by_prefix=args.by_prefix,
        overdue=args.overdue
      )
    except PrefixNotDefined:
      print(f'{f:error}prefix {args.by_prefix} was not defined{f:e}',
        file=sys.stderr)
    except NoMatchingItems:
      print(f'{f:error}no matching items{f:e}', file=sys.stderr)
      exit(1)

    exit(0)

  # cmd:rm
  if args.cmd in ('r', 'd', 'rm'):
    if args.id == 'list':
      print('are you sure you want to delete the whole list? [y/n]', end=' ')
      yesno = input()
      if yesno in ['y', 'Y']:
        os.remove(glob.list_fname)
        print(f'{f:success}successfully removed the list{f:e}')
        exit(0)
      else:
        exit(0)
    else:
      if todo_list.remove_item(int(args.id)):
        todo_list.to_file()
        print(f'{f:success}item removed{f:e}')
        exit(0)
      else:
        print(f'{f:error}no such item{f:e}', file=sys.stderr)
        exit(1)

  # cmd:complete
  if args.cmd in ('complete', 'c'):
    if todo_list.set_completeness(args.id, True):
      todo_list.to_file()
      _, item = todo_list.get_item(args.id)
      print(item)
      exit(0)
    else:
      print(f'{f:error}no such item{f:e}', file=sys.stderr)
      exit(1)

  # cmd:uncomplete
  if args.cmd in ('uncomplete', 'u'):
    if todo_list.set_completeness(args.id, False):
      _, item = todo_list.get_item(args.id)
      print(item)
      todo_list.to_file()
      exit(0)
    else:
      print(f'{f:error}no such item{f:e}', file=sys.stderr)
      exit(1)

if __name__ == '__main__':
  main()
