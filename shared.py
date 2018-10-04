#!/usr/bin/env python
# Shared functions
# https://github.com/rcook/pyfileutils

import hashlib
import os

GITHUB_URL = "https://github.com/rcook/pyfileutils"

BLOCK_SIZE = 1024

GIB_THRESHOLD = 1024 * 1024 * 1024
MIB_THRESHOLD = 1024 * 1024

def compute_sha1(path, partial=False, include_file_size=True, block_size=1024):
    """
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(delete=True) as f:
    ...     f.write("hello world\\n")
    ...     f.flush()
    ...     r0 = compute_sha1(f.name)
    ...     r1 = compute_sha1(f.name, block_size=4)
    ...     r2 = compute_sha1(f.name, partial=True)
    ...     r3 = compute_sha1(f.name, partial=True, block_size=4)
    >>> r0
    '12:22596363b3de40b06f981fb85d82312e8c0ed511'
    >>> r1
    '12:22596363b3de40b06f981fb85d82312e8c0ed511'
    >>> r2
    '12:22596363b3de40b06f981fb85d82312e8c0ed511'
    >>> r3
    '12:a5cec7af5f7aab769cf0d4aa440e01c7bfc371b2'
    """
    file_size = os.stat(path).st_size
    if partial:
        block_count = 1
    else:
        block_count = (file_size / block_size) + (1 if (file_size % block_size) > 0 else 0)

    m = hashlib.sha1()
    with open(path, "rb") as f:
        for _ in range(0, block_count):
            m.update(f.read(block_size))

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
