# Sha1sumex

* [swissarmyknife](README.md)
* [Code](sha1sumex)

An improved version of `sha1sum` that will recurse a directory structure

## Usage

```
usage: sha1sumex [-h] {generate,verify,show} ...

An improved sha1sum

positional arguments:
  {generate,verify,show}
    generate            generate checksum file
    verify              verify files in checksum file
    show                show signatures for one or more files

optional arguments:
  -h, --help            show this help message and exit

https://github.com/rcook/swissarmyknife
```

## Example

```
./sha1sumex generate /path/to/files.txt .
./sha1sumex verify /path/to/files.txt .
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[exifread]: https://pypi.org/project/ExifRead/
[find-duplicates]: https://gist.github.com/jinie/b51f75fa1ece7c02ca3f/
[licence]: LICENSE
