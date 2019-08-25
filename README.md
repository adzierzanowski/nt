# nt

`nt` is a JSON todo-list CLI front-end. Just like
[ultralist](https://github.com/ultralist/ultralist) but a little bit different.

## FAQ

**Why?**

None of todo-list suited my needs. So here's another! Yay!

**Why `nt`?**

Because it is easy to type and is not associated with any unix utility
(at least not with one that I heard of).

**Is it good?**

It's good for me.

**How is it different?**

* It requires less typing.
* It provides git-like command editing in a text editor of your choice.
* It's dead simple.

# Usage

Type

    $ nt

to get all uncompleted items piped to `less`.

[![asciicast](https://asciinema.org/a/0tvEpZ3P4h9pbrEa0lXWQOrKG.svg)](https://asciinema.org/a/0tvEpZ3P4h9pbrEa0lXWQOrKG)

Type

    $ nt a[dd] content @context more content +project even more content #hashtag -d due-date -p priority

to add an entry to the exisiting list.

Alternatively

    $ nt a[dd]

will open a text editor to edit passed parameters.

Same goes with `e[dit]` command.

# TODO

* Better due date parsing.
