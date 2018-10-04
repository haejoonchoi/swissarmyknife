#!/usr/bin/env python
# Deduper
# A reasonably useful file deduplicator
# https://github.com/rcook/pyfileutils

import argparse
import datetime
import hashlib
import logging
import os
import re
import sys

from shared import *

##################################################

def prune(d):
    return { k : paths for k, paths in d.iteritems() if len(paths) > 1 }

##################################################

class SignatureMatcher(object):
    NAME = "sig"

    def find_duplicates(self, root_dir, debug, show_progress):
        # Group by size
        size_map = self.scan(root_dir, show_progress=show_progress)
        self.dump(root_dir, size_map)

        logging.info("Size scan found {} candidate files".format(self.compute_file_count(size_map)))

        # Group by partial signature
        sig_map0 = self.compute_signatures(size_map, partial=True, show_progress=show_progress)
        self.dump(root_dir, sig_map0)

        logging.info("Signature scan found {} candidate files".format(self.compute_file_count(sig_map0)))

        # Group by full signature
        sig_map1 = self.compute_signatures(sig_map0, partial=False, show_progress=show_progress)
        self.dump(root_dir, sig_map1)

        duplicate_file_count, duplicate_byte_count = self.compute_wastage(sig_map1, debug=debug)
        logging.info("Found {} duplicate files occupying {}".format(
            duplicate_file_count,
            pretty_byte_count(duplicate_byte_count)))

        return sig_map1

    def __repr__(self): return self.NAME

    @staticmethod
    def scan(start_dir, show_progress):
        with Progress(show_progress) as p:
            result = {}
            for root_dir, _, file_names in os.walk(start_dir):
                for file_name in file_names:
                    p.step()
                    path = os.path.join(root_dir, file_name)
                    file_size = os.stat(path).st_size
                    if file_size not in result:
                        result[file_size] = []
                    result[file_size].append(path)

        return prune(result)

    @staticmethod
    def compute_signatures(d, partial, show_progress):
        with Progress(show_progress) as p:
            result = {}
            for _, paths in d.iteritems():
                for path in paths:
                    p.step()
                    sig = SignatureMatcher.compute_signature(path, partial)
                    if sig not in result:
                        result[sig] = []
                    result[sig].append(path)

        return prune(result)

    @staticmethod
    def compute_signature(path, partial=False):
        file_size = os.stat(path).st_size
        if partial:
            block_count = 1
        else:
            block_count = (file_size / BLOCK_SIZE) + 1 if (file_size % BLOCK_SIZE) > 0 else 0

        m = hashlib.sha1()
        with open(path, "rb") as f:
            for i in range(0, block_count):
                m.update(f.read(BLOCK_SIZE))

        return "{}:{}".format(file_size, m.hexdigest())

    @staticmethod
    def dump(root_dir, d):
        # Potentially expensive logging
        if debug_logging():
            entries = ["{}: {}".format(key, pretty_list(map(lambda p: os.path.relpath(p, root_dir), paths))) for key, paths in d.iteritems()]
            logging.debug("Files: {}".format(pretty_list(entries)))

    @staticmethod
    def compute_file_count(d):
        file_count = sum([len(paths) for _, paths in d.iteritems()])
        return file_count

    @staticmethod
    def compute_wastage(d, debug):
        duplicate_file_count = sum([len(paths) - 1 for _, paths in d.iteritems()])
        duplicate_byte_count = sum([os.stat(paths[0]).st_size * (len(paths) - 1) for _, paths in d.iteritems()])

        if debug:
            is_valid = True
            for _, paths in d.iteritems():
                p0 = paths[0]
                for p in paths:
                    if not compare_files(p0, p):
                        is_valid = False
                        logging.info("File comparison failed: {} vs {}".format(p0, p))

            if not is_valid:
                raise RuntimeError("Diagnostics failed")

        return duplicate_file_count, duplicate_byte_count

class NameMatcher(object):
    NAME = "name"

    def find_duplicates(self, root_dir, debug, show_progress):
        with Progress(show_progress) as p:
            result = {}
            for base_dir, _, file_names in os.walk(root_dir):
                for file_name in file_names:
                    p.step()
                    path = os.path.join(base_dir, file_name)
                    if file_name not in result:
                        result[file_name] = []
                    result[file_name].append(path)

        return prune(result)

    def __repr__(self): return self.NAME

class FuzzyNameMatcher(object):
    NAME = "fuzzy"

    def find_duplicates(self, root_dir, debug, show_progress):
        with Progress(show_progress) as p:
            result = {}
            for base_dir, _, file_names in os.walk(root_dir):
                for file_name in file_names:
                    p.step()
                    path = os.path.join(base_dir, file_name)
                    fuzzy_name = self.normalize_path(path)
                    if fuzzy_name not in result:
                        result[fuzzy_name] = []
                    result[fuzzy_name].append(path)

        return prune(result)

    def __repr__(self): return self.NAME

    @staticmethod
    def normalize_path(path):
        parts = path.lower().split("/")
        n = len(parts)
        if n == 0:
            return ""
        elif n == 1:
            return FuzzyNameMatcher.normalize_part(parts[0])
        else:
            return FuzzyNameMatcher.normalize_part(parts[-2]) + "/" + FuzzyNameMatcher.normalize_part(parts[-1])

    @staticmethod
    def normalize_part(s):
        orig_n, orig_ext = os.path.splitext(os.path.basename(s))
        return FuzzyNameMatcher.normalize_fragment(orig_n) + FuzzyNameMatcher.normalize_fragment(orig_ext)

    @staticmethod
    def normalize_fragment(s):
        return re.sub("[_\- ]+", " ", s)

##################################################

class DoNotRemoveDuplicatesStrategy(object):
    NAME = "nop"

    def apply(self, paths):
        return paths, []

    def __repr__(self): return self.NAME

class KeepFirstInCopyAwareOrderStrategy(object):
    NAME = "keep-first"

    def apply(self, paths):
        sorted_paths = sorted(paths, cmp=self.copy_aware_path_compare)
        return [sorted_paths[0]], sorted_paths[1:]

    def __repr__(self): return self.NAME

    @staticmethod
    def has_prefix(prefix, file_name):
        if file_name.startswith(prefix):
            return True, file_name[len(prefix):]
        return False, file_name

    @staticmethod
    def copy_aware_path_compare(p0, p1):
        d0 = os.path.dirname(p0)
        d1 = os.path.dirname(p1)
        if d0 != d1:
            return cmp(p0, p1)

        n0 = os.path.basename(p0)
        result0, b0 = KeepFirstInCopyAwareOrderStrategy.has_prefix("Copy of ", n0)
        n1 = os.path.basename(p1)
        result1, b1 = KeepFirstInCopyAwareOrderStrategy.has_prefix("Copy of ", n1)

        if b0 == b1:
            if result0:
                return 1
            if result1:
                return -1
            raise RuntimeError("Unreachable")

        return cmp(n0, n1)

##################################################

PROGRESS_STEP = 1

BLOCK_SIZE = 1024

DEFAULT_MATCHER = SignatureMatcher()
MATCHERS = [
    DEFAULT_MATCHER,
    NameMatcher(),
    FuzzyNameMatcher()
]

DEFAULT_STRATEGY = DoNotRemoveDuplicatesStrategy()
STRATEGIES = [
    DEFAULT_STRATEGY,
    KeepFirstInCopyAwareOrderStrategy()
]

##################################################

class Progress(object):
    def __init__(self, is_enabled):
        self._is_enabled = is_enabled
        self._i = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._is_enabled:
            sys.stdout.write("\n")

    def step(self):
        if self._is_enabled:
            if self._i % PROGRESS_STEP == 0:
                sys.stdout.write(".")
                sys.stdout.flush()
            self._i += 1

def debug_logging():
    return logging.getLogger().isEnabledFor(logging.DEBUG)

def pretty_list(items):
    return "(empty)" if len(items) == 0 else ", ".join(items)

def compare_files(p0, p1):
    with open(p0, "rb") as f:
        d0 = f.read()
    with open(p1, "rb") as f:
        d1 = f.read()

    return d0 == d1

##################################################

def remove_duplicates(strategy, duplicate_map, dry_run, debug):
    bytes_freed = 0
    file_count = 0
    for _, paths in duplicate_map.iteritems():
        files_to_keep, files_to_remove = strategy.apply(paths)

        # Potentially expensive logging
        if debug_logging():
            logging.debug("{}: files to keep: {}, files to remove: {}".format(
                type(strategy).__name__,
                pretty_list(files_to_keep),
                pretty_list(files_to_remove)))

        file_count += len(files_to_remove)
        for path in files_to_remove:
            logging.debug("Removing {}".format(path))
            bytes_freed += os.stat(path).st_size
            if not dry_run:
                os.unlink(path)

    logging.info("Strategy \"{}\" deleted {} files and freed {}".format(
        strategy.NAME,
        file_count,
        pretty_byte_count(bytes_freed)))

##################################################

def get_matcher(name):
    matcher = next((m for m in MATCHERS if m.NAME == name), None)
    if matcher is None:
        raise argparse.ArgumentTypeError("Matcher must be one of ({})".format(", ".join(sorted(map(lambda m: "\"{}\"".format(m.NAME), MATCHERS)))))
    return matcher

def get_strategy(name):
    strategy = next((s for s in STRATEGIES if s.NAME == name), None)
    if strategy is None:
        raise argparse.ArgumentTypeError("Strategy must be one of ({})".format(", ".join(sorted(map(lambda s: "\"{}\"".format(s.NAME), STRATEGIES)))))
    return strategy

def is_safe_dir(path):
    parts = path.strip("/").split("/")
    return len(parts) >= 3

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="A reasonably useful file deduplicator",
        epilog="https://github.com/rcook/pyfileutils")
    parser.add_argument(
        "root_dir",
        metavar="ROOTDIR",
        type=os.path.abspath,
        help="start directory for scan")
    parser.add_argument(
        "--match",
        dest="matcher",
        type=get_matcher,
        default=DEFAULT_MATCHER,
        help="matcher used to compare files")
    parser.add_argument(
        "--strategy",
        dest="strategy",
        type=get_strategy,
        default=DEFAULT_STRATEGY,
        help="deduplication strategy to employ")
    add_switch_with_inverse(
        parser,
        "dry-run",
        default=True,
        help="perform scan but do not delete files",
        inverse_help="perform scan and delete files")
    add_switch_with_inverse(
        parser,
        "verbose",
        default=False,
        help="show extra logging",
        inverse_help="do not show extra logging")
    add_switch_with_inverse(
        parser,
        "debug",
        default=False,
        help="show extra diagnostics",
        inverse_help="do not show extra diagnostics")
    add_switch_with_inverse(
        parser,
        "force",
        default=False,
        help="override safety check on protected directories",
        inverse_help="do not override safety check on protected directories")
    add_switch_with_inverse(
        parser,
        "progress",
        default=False,
        help="show progress",
        inverse_help="do not show progress")

    args = parser.parse_args(argv)

    if not args.force and not is_safe_dir(args.root_dir):
        sys.stderr.write("Safety check failed: If you really want to run this command in this directory use --force?\n")
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s:%(message)s")

    for k, v in sorted(vars(args).iteritems()):
        logging.info("Argument: {}={}".format(k, v))

    start_time = datetime.datetime.now()
    logging.info("Deduplication started at {}".format(start_time))

    logging.info("Finding duplicates using \"{}\" matcher".format(args.matcher.NAME))
    duplicate_map = args.matcher.find_duplicates(
        args.root_dir,
        debug=args.debug,
        show_progress=args.progress)

    logging.info("Removing duplicates")
    remove_duplicates(
        args.strategy,
        duplicate_map,
        dry_run=args.dry_run,
        debug=args.debug)

    end_time = datetime.datetime.now()
    logging.info("Deduplication finished at {}, elapsed time: {}".format(end_time, end_time - start_time))

##################################################

if __name__ == "__main__":
    main()
