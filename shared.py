#!/usr/bin/env python
# Shared functions
# https://github.com/rcook/swissarmyknife

import hashlib
import os

GITHUB_URL = "https://github.com/rcook/swissarmyknife"

GIB_THRESHOLD = 1024 * 1024 * 1024
MIB_THRESHOLD = 1024 * 1024
KIB_THRESHOLD = 1024

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
    """
    >>> pretty_byte_count(186129123987123)
    '173,346.3 GiB'
    >>> pretty_byte_count(186129123987)
    '173.3 GiB'
    >>> pretty_byte_count(186129123)
    '177.5 MiB'
    >>> pretty_byte_count(186129)
    '181.8 KiB'
    >>> pretty_byte_count(5000)
    '4.9 KiB'
    >>> pretty_byte_count(1024)
    '1.0 KiB'
    >>> pretty_byte_count(1000)
    '1,000 bytes'
    >>> pretty_byte_count(512)
    '512 bytes'
    """
    if n >= GIB_THRESHOLD:
        return "{:,.1f} GiB".format(float(n) / GIB_THRESHOLD)
    elif n >= MIB_THRESHOLD:
        return "{:,.1f} MiB".format(float(n) / MIB_THRESHOLD)
    elif n >= KIB_THRESHOLD:
        return "{:,.1f} KiB".format(float(n) / KIB_THRESHOLD)
    else:
        return "{:,} bytes".format(n)
