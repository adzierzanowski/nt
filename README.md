# nt

`nt` is a JSON todo-list CLI frontend. Just like
[ultralist](https://github.com/ultralist/ultralist) but a little bit different.

## FAQ

**Why?**

None of todo-list suited my needs. So here's another! Yay!

By the way, it's pretty interesting that it's so hard to make such a simple
piece of software good.

**Why `nt`?**

Because it is easy to type and is not associated with any unix utility
(at least not with one that I heard of).

**Is it good?**

It's good for me.

**How is it different?**

* Configurable prefixes per list. Default are `@context`, `#tag` and `+project`.
* It requires less typing.
* It provides git-like command editing in a text editor of your choice.
* It's dead simple and small and depends on nothing outside standard Python3
and widely-used unix utilities (namely `neovim` and `less`). And you're not
limited to `neovim`, you can change it to some lame editor.

## Installation

    $ git clone https://github.com/adzierzanowski/nt.git
    $ cd nt
    $ pip3 install .

## Usage

Type

    $ nt

to get all uncompleted items piped to `less`.

[![asciicast](https://asciinema.org/a/0tvEpZ3P4h9pbrEa0lXWQOrKG.svg)](https://asciinema.org/a/0tvEpZ3P4h9pbrEa0lXWQOrKG)

Type

    $ nt a[dd] content @context more content +project even more content #hashtag -d due-date -p priority

to add an entry to the exisiting list.

Alternatively

    $ nt a[dd]

will open a text editor ([nvim](https://github.com/neovim/neovim) by default;
edit `~/.ntrc` to change the editor) to edit passed parameters.

Same goes with `e[dit]` command.

## ~/.ntrc

    editor=nvim
    list_fname=.todo.json

## TODO

* Better due date parsing.

## zsh completions

    compdef _gnu_generic nt
