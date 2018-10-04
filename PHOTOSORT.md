# Photosort

* [pyfileutils](README.md)
* [Code](photosort)

This script walks a directory tree containing `.jpg` image files and arranges them into a year-month hierarchy.

Additional dependencies: [ExifRead][exifread], `pip install --user exifread`

## Usage

```
usage: photosort [-h] INPUTDIR OUTPUTDIR

Sort JPEGs into year/month directory structure

positional arguments:
  INPUTDIR
  OUTPUTDIR

optional arguments:
  -h, --help  show this help message and exit

https://github.com/rcook/pyfileutils
```

## Example

```
./photosort input-dir output-dir
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[exifread]: https://pypi.org/project/ExifRead/
[find-duplicates]: https://gist.github.com/jinie/b51f75fa1ece7c02ca3f/
[licence]: LICENSE
