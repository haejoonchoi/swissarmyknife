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

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Compute total file size of directory tree")
    parser.add_argument("start_dir", metavar="STARTDIR", type=os.path.abspath)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--no-recursive", dest="recursive", action="store_false", default=True)
    group.add_argument("--recursive", dest="recursive", action="store_true", default=True)

    args = parser.parse_args(argv)

    file_count = 0
    total_bytes = 0
    for p in scan(args.start_dir, recursive=args.recursive):
        print(p)
        file_count += 1
        file_size = os.stat(p).st_size
        total_bytes += file_size

    print("{} files, {} bytes".format(file_count, total_bytes))

if __name__ == "__main__":
    main()
