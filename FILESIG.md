# Filesig

* [swissarmyknife](README.md)
* [Code](filesig)

An improved version of `sha1sum` that will recurse a directory structure

## Usage

```
usage: filesig [-h] {generate,verify,show} ...

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
./filesig generate --format=full /path/to/files.txt .
./filesig verify /path/to/files.txt .
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[licence]: LICENSE
