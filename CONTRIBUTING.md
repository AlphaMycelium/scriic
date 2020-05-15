# Contributing to Scriic

## Commit Messages

Scriic is released automatically using [Python Semantic Release][psr].
Therefore, we must follow the [Angular commit style guide][angular-commits] in
all commit messages.

The scope of your commit should be:

- A single command you are modifying (e.g. `SUB` or `DO`)
- `scriicsics` if you are making changes to the Scriicsics package

It is safe to leave the scope blank if you are changing many areas or
something not listed above, please use your common sense.

## Scriicsics

If you are making a breaking change to one of the Scriicsics files, please copy
it into a new file for the new version, e.g. `sayV2.scriic`, instead of marking
your commit as a breaking change. This will prevent lots of major releases of
the full project being made for Scriicsics changes.


[psr]: https://github.com/relekang/python-semantic-release/
[angular-commits]: https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-guidelines
