# Deduper

* [swissarmyknife](README.md)
* [Code](deduper)

This is a reasonably useful file deduplicator, based on and inspired by [`find_duplicates.py`][find-duplicates].

## Usage

```
usage: deduper [-h] [--match MATCHER] [--strategy STRATEGY]
               [--dry-run | --no-dry-run] [--no-verbose | --verbose]
               [--no-debug | --debug] [--no-force | --force]
               [--no-progress | --progress]
               STARTDIR

A reasonably useful file deduplicator

positional arguments:
  STARTDIR             start directory for scan

optional arguments:
  -h, --help           show this help message and exit
  --match MATCHER      matcher used to compare files
  --strategy STRATEGY  deduplication strategy to employ
  --dry-run            perform scan but do not delete files (default)
  --no-dry-run         perform scan and delete files
  --no-verbose         do not show extra logging (default)
  --verbose            show extra logging
  --no-debug           do not show extra diagnostics (default)
  --debug              show extra diagnostics
  --no-force           do not override safety check on protected directories
                       (default)
  --force              override safety check on protected directories
  --no-progress        do not show progress (default)
  --progress           show progress

https://github.com/rcook/swissarmyknife
```

## Example

```
./deduper --strategy keep-first --dry-run --verbose .
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[find-duplicates]: https://gist.github.com/jinie/b51f75fa1ece7c02ca3f/
[licence]: LICENSE
