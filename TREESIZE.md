# Treesize

* [swissarmyknife](README.md)
* [Code](treesize)

This scripts walks a directory tree and outputs the total file count and total file size in bytes. This is useful because the macOS's version of `du` does not support `--apparent-size` unlike GNU's.

## Usage

```
usage: treesize [-h] [--recursive | --no-recursive]
                [--progress | --no-progress]
                STARTDIR

Report total file count and file bytes for directory tree

positional arguments:
  STARTDIR

optional arguments:
  -h, --help      show this help message and exit
  --recursive     recurse into directory (default)
  --no-recursive  do not recurse into directory
  --progress      show files as they are processed (default)
  --no-progress   do not show files as they are processed

https://github.com/rcook/swissarmyknife
```

## Example

```
./treesize .
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[licence]: LICENSE
