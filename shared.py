#!/usr/bin/env python
# Shared functions
# https://github.com/rcook/pyfileutils

import hashlib
import os

GITHUB_URL = "https://github.com/rcook/pyfileutils"

BLOCK_SIZE = 1024

GIB_THRESHOLD = 1024 * 1024 * 1024
MIB_THRESHOLD = 1024 * 1024

def compute_sha1(path, partial=False, include_file_size=True):
    file_size = os.stat(path).st_size
    if partial:
        block_count = 1
    else:
        block_count = (file_size / BLOCK_SIZE) + (1 if (file_size % BLOCK_SIZE) > 0 else 0)

    m = hashlib.sha1()
    with open(path, "rb") as f:
        for _ in range(0, block_count):
            m.update(f.read(BLOCK_SIZE))

    d = m.hexdigest()
    if include_file_size:
        return "{}:{}".format(file_size, d)
    else:
        return d

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

def pretty_byte_count(n):
    if n >= GIB_THRESHOLD:
        return "{0:0.1f} GiB".format(float(n) / GIB_THRESHOLD)
    elif n >= MIB_THRESHOLD:
        return "{0:0.1f} MiB".format(float(n) / MIB_THRESHOLD)
    else:
        return "{} bytes".format(n)
