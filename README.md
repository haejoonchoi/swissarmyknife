# Swiss Army Knife

_Minimal-dependency file utilities in Python_

These scripts are designed to perform file and backup housekeeping operations with minimal or no external dependencies: these are specifically intended to be used on constrained environments like network-attached storage devices, routers or Raspberry Pis.

Unless specifically called out, all these scripts should work on a standard Python 2.7.x installation with no additional package requirements. I have extracted some shared code into a shared module. We'll see how that works out.

I have deliberately chosen to write these scripts in Python (2.7.x, specifically) for the following reasons:

* I like Python
* Python 2.7.x is almost universally available on all platforms I care about (Linux, macOS, Windows)
* Python is reasonably portable
* Python 2.7.x is usually installed by default on Linux and macOS

Scripts available:

* [Deduper](DEDUPER.md)
* [Photosort](PHOTOSORT.md)
* [Sha1sumex](SHA1SUMEX.md)
* [Treesize](TREESIZE.md)

## Downloading in constrained environments

An [installation](install) script is provided to download all tools on environments which do not have direct access to Git:

```
mkdir swissarmyknife && cd swissarmyknife && wget -qO- https://raw.githubusercontent.com/rcook/swissarmyknife/master/install | sh
```

Once the directory has been bootstrapped like this, you can just run `install` from this directory in future to update to the latest version of the scripts.

## Licence

Released under [MIT License][licence]

Copyright &copy; 2018, Richard Cook. All rights reserved.

[exifread]: https://pypi.org/project/ExifRead/
[find-duplicates]: https://gist.github.com/jinie/b51f75fa1ece7c02ca3f/
[licence]: LICENSE
