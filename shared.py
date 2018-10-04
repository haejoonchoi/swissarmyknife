#!/usr/bin/env python
# Shared functions
# https://github.com/rcook/pyfileutils

GIB_THRESHOLD = 1024 * 1024 * 1024
MIB_THRESHOLD = 1024 * 1024

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
