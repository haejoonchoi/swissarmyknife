#!/usr/bin/env python
# Treesize
# Report total file count and file bytes for directory tree
# https://github.com/rcook/pyfileutils

import argparse
import os
import sys

def scan(start_dir, recursive=False):
    for containing_dir, subdir_names, file_names in os.walk(start_dir):
        if not recursive:
            del subdir_names[:]
        for file_name in sorted(file_names):
            full_path = os.path.join(containing_dir, file_name)
            yield full_path

def add_switch_with_inverse(parser, name, default, help=None, inverse_help=None):
    group = parser.add_mutually_exclusive_group()
    dest = name.replace("-", "_")
    group.add_argument(
        "--{}".format(name),
        dest=dest,
        action="store_true",
        default=default,
        help=help)
    group.add_argument(
        "--no-{}".format(name),
        dest=dest,
        action="store_false",
        default=default,
        help=inverse_help)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Report total file count and file bytes for directory tree",
        epilog="https://github.com/rcook/pyfileutils")
    parser.add_argument("start_dir", metavar="STARTDIR", type=os.path.abspath)
    add_switch_with_inverse(
        parser,
        "recursive",
        default=True,
        help="recurse into directory",
        inverse_help="do not recurse into directory")
    add_switch_with_inverse(
        parser,
        "progress",
        default=True,
        help="show files as they are processed",
        inverse_help="do not show files as they are processed")

    args = parser.parse_args(argv)

    file_count = 0
    symlink_count = 0
    total_bytes = 0
    for p in scan(args.start_dir, recursive=args.recursive):
        if args.progress:
            print(p)
        if os.path.islink(p):
            symlink_count += 1
        else:
            file_count += 1
            file_size = os.stat(p).st_size
            total_bytes += file_size

    print("{} files, {} bytes, {} symlinks".format(file_count, total_bytes, symlink_count))

if __name__ == "__main__":
    main()
