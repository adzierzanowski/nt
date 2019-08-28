# nt

`nt` is a JSON todo-list CLI frontend. Just like
[ultralist](https://github.com/ultralist/ultralist) but a little bit different.

It is highly inspired by this thing that was the closest to my preferences
but I have some issues with it. For one thing, `nt` is a little bit more
customizable.

## FAQ

### Why?

None of todo-list suited my needs. So here's another! Yay!

By the way, it's pretty interesting that it's so hard to make such a simple
piece of software good.

### Why `nt`?

Because it is easy to type and is not associated with any unix utility
(at least not with one that I heard of).

### Is it good?

It's good for me.

### How is it different?

* It requires less typing.
* It's dead simple and small
* It provides git-like command editing in a text editor of your choice.
* Configurable prefixes per list. Default are `@context`, `#tag` and `+project`.
* It depends on nothing beyond standard Python3 and widely-used unix
utilities (namely `neovim` and `less`). And you're not limited to `neovim`,
you can change it to some lame editor.

## Installation

```bash
    $ git clone https://github.com/adzierzanowski/nt.git
    $ cd nt
    $ pip3 install .
```

## Usage

Type

```bash
    $ nt
```

to get all uncompleted items. This can be piped to `less` by passing `-l`
switch to `nt ls` command.

Type

    $ nt a[dd] content @context more content +project even more content #hashtag -d due-date -p priority

to add an entry to the exisiting list.

Alternatively

    $ nt a[dd]

will open a text editor ([nvim](https://github.com/neovim/neovim) by default;
edit `~/.ntrc` to change the editor) to edit passed parameters.

Same goes with `e[dit]` command.

### Some workflow examples

[![asciicast](https://asciinema.org/a/AzMcet2kVExAoxHtKhngTob5n.svg)](https://asciinema.org/a/AzMcet2kVExAoxHtKhngTob5n)

## Configuration

Example of `.ntrc`:

```ini
    editor=nvim
    list_fname=.todo.json
    date_fmt=%d.%m.%y %H:%M
    date_fmt=%m-%d
    pretty_json=true
    completed_str=[x]
    uncompleted_str=[ ]
```

### Configuration precedence

    ~/.ntrc < .ntrc < .todo.json config dict

## TODO

See `.todo.json` ;)

## zsh completions

    compdef _gnu_generic nt
