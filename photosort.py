import argparse
import datetime
import exifread
import os
import sys

DATE_TIME_KEY = "EXIF DateTimeOriginal"

EXTS = map(lambda s: s.lower(), [
    ".jpg"
])

def get_date(path):
    with open(path, "rb") as f:
        tags = exifread.process_file(f)
        value = tags.get(DATE_TIME_KEY, None)
        if value is None:
            return None
        return datetime.datetime.strptime(str(value), "%Y:%m:%d %H:%M:%S")

def rename(input_path, output_dir):
    input_file_name = os.path.basename(input_path)
    d = get_date(input_path)
    if d is None:
        return

    target_file_name = "{0:04d}{1:02d}{2:02d}-{3}".format(d.year, d.month, d.day, input_file_name)
    target_subdir = os.path.join("{0:04d}".format(d.year), "{0:04d}-{1:02d}".format(d.year, d.month))
    target_dir = os.path.join(output_dir, target_subdir)
    target_path = os.path.join(target_dir, target_file_name)

    print("{} -> {}".format(input_path, target_path))

def rename_all(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        _, ext = os.path.splitext(file_name)
        if ext.lower() in EXTS:
            rename(os.path.join(input_dir, file_name), output_dir)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Create sorted directory structure for photos based on metadata")
    parser.add_argument("input_dir", metavar="INPUTDIR", type=os.path.abspath)
    parser.add_argument("output_dir", metavar="OUTPUTDIR", type=os.path.abspath)
    args = parser.parse_args(argv)
    rename_all(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
