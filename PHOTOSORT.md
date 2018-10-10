# Photosort

* [swissarmyknife](README.md)
* [Code](photosort)

This script walks a directory tree containing `.jpg` image files and arranges them into a year-month hierarchy.

Additional dependencies: [ExifRead][exifread], `pip install --user exifread`

## Usage

```
usage: photosort [-h] [--dry-run | --no-dry-run] INPUTDIR OUTPUTDIR

Sort JPEGs into year/month directory structure

positional arguments:
  INPUTDIR
  OUTPUTDIR

optional arguments:
  -h, --help    show this help message and exit
  --dry-run     copy files (default)
  --no-dry-run  do not copy files

https://github.com/rcook/swissarmyknife
```

## Example

```
./photosort input-dir output-dir
```

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[exifread]: https://pypi.org/project/ExifRead/
[licence]: LICENSE
