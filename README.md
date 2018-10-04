# Minimal-dependency file utilities in Python

These scripts are designed to perform file and backup housekeeping operations with minimal or no external dependencies: these are specifically intended to be used on constrained environments like network-attached storage devices or Raspberry Pis.

Unless specifically called out, all these scripts should work on a standard Python 2.7.x installation with no additional package requirements. I have extracted some shared code into a shared module. We'll see how that works out.

I have deliberately chosen to write these scripts in Python (2.7.x, specifically) for the following reasons:

* I like Python
* Python 2.7.x is almost universally available on all platforms I care about (Linux, macOS, Windows)
* Python is reasonably portable
* Python 2.7.x is installed by default on Linux and macOS

Scripts available:

* [Deduper](#deduper)
* [Photosort](#photosort)
* [Treesize](#treesize)

## Deduper

This is a reasonably useful file deduplicator, based on and inspired by [`find_duplicates.py`][find-duplicates].

### Usage

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

https://github.com/rcook/pyfileutils
```

### Example

```
python ./deduper.py --strategy keep-first --dry-run --verbose .
```

## Photosort

This script walks a directory tree containing `.jpg` image files and arranges them into a year-month hierarchy.

Additional dependencies: [ExifRead][exifread], `pip install --user exifread`

### Usage

```
usage: photosort.py [-h] INPUTDIR OUTPUTDIR

Sort JPEGs into year/month directory structure

positional arguments:
  INPUTDIR
  OUTPUTDIR

optional arguments:
  -h, --help  show this help message and exit

https://github.com/rcook/pyfileutils
```

### Example

```
python ./photosort.py input-dir output-dir
```

## Treesize

This scripts walks a directory tree and outputs the total file count and total file size in bytes. This is useful because the macOS's version of `du` does not support `--apparent-size` unlike GNU's.

### Usage

```
usage: treesize.py [-h] [--recursive | --no-recursive] STARTDIR

Report total file count and file bytes for directory tree

positional arguments:
  STARTDIR

optional arguments:
  -h, --help      show this help message and exit
  --recursive     recurse into directory
  --no-recursive  do not recurse into directory
  --progress      show files as they are processed
  --no-progress   do not show files as they are processed

https://github.com/rcook/pyfileutils
```

### Example

```
python ./treesize.py .
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[exifread]: https://pypi.org/project/ExifRead/
[find-duplicates]: https://gist.github.com/jinie/b51f75fa1ece7c02ca3f/
[licence]: LICENSE
