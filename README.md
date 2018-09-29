# Deduper

Minimal-dependency Python script for deduplicating a directory for use on Synology NASes and similar

Based on and inspired by [`find_duplicates.py`][find-duplicates]

## Usage

```
usage: deduper.py [-h] [--match MATCHER] [--strategy STRATEGY]
                  [--dry-run | --no-dry-run] [--verbose | --no-verbose]
                  [--debug | --no-debug] [--force | --no-force]
                  [--progress | --no-progress]
                  ROOTDIR

A reasonably useful file deduplicator

positional arguments:
  ROOTDIR              start directory for scan

optional arguments:
  -h, --help           show this help message and exit
  --match MATCHER      matcher used to compare files
  --strategy STRATEGY  deduplication strategy to employ
  --dry-run            perform scan but do not delete files
  --no-dry-run         perform scan and delete files
  --verbose            show extra logging
  --no-verbose         do not show extra logging
  --debug              show extra diagnostics
  --no-debug           do not show extra diagnostics
  --force              override safety check on protected directories
  --no-force           do not override safety check on protected directories
  --progress           show progress
  --no-progress        do not show progress

https://github.com/rcook/deduper
```

## Example

```
deduper.py --strategy keep-first --dry-run --verbose .
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[find-duplicates]: https://gist.github.com/jinie/b51f75fa1ece7c02ca3f/
[licence]: LICENSE
