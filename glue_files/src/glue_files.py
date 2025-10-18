import os
import sys
import argparse


parser = argparse.ArgumentParser(prog="glue_files",
                                 description="Glue files and with path marks")

parser.add_argument("-R", "--recursive", action="store_true", dest="RECURSE",
                    help="Glue files recursively, "
                    + "including files from subdirectories")

INPATH_HELP = "Path to an input file input directory. In case INPATH " + \
            "is a directory, all files in this directory and its subdirectories " + \
            "will be glued together if -R flag is specified, then files from " + \
            "subfolders of the INPATH will also be glued"

parser.add_argument("INPATH", help=INPATH_HELP, nargs="+")

parser.add_argument("-p", "--preview", "--dry-run",
                    action="store_true", dest="PREVIEW",
                    help="Display files that will be glued together")

parser.add_argument("-o", "--output", dest="OUTPUT",
                    help="Output file")

args = parser.parse_args()


def run(path: str, ofile):
    print(f"Opening: {path}")

    lines = []
    with open(path, "r") as file:
        try:
            lines = file.readlines()
        except UnicodeDecodeError:
            print(f"File {path} is probably binary or not UNICODE, skipped")
            return

    # File closed
    print("", file=ofile)
    print(f"==== FILE: {path} ====", file=ofile)
    print("", file=ofile)

    for line in lines:
        ofile.write(line)


def get_recursive_path_list(root: str):
    path_list = []
    scan = os.scandir(root)
    for e in scan:
        if e.is_dir():
            path_list.extend(get_recursive_path_list(e.path))
        else:
            path_list.append(e.path)

    return path_list


def get_yn(msg):
    while True:
        yn = input(msg + " ([y]es/[n]o) ").lower()
        if yn == "y" or yn == "yes":
            return True
        if yn == "n" or yn == "no":
            return False
        print("Please choose yes or no")


def main(argv):
    if args.OUTPUT is None:
        print("Output file should be specified with -o flag")
        return


    if os.path.exists(args.OUTPUT):
        if not os.path.isfile(args.OUTPUT):
            print(f"Output '{args.OUTPUT}' is a directory, please choose a file")
            return

        print(f"File {args.OUTPUT} already exists.")
        print("IT WILL GET OVERWRITTEN!")
        yes = get_yn("Continue?")

        if not yes:
            print("Ok, not doing anything")
            return

    with open(args.OUTPUT, "w") as of:
        if args.INPATH is None:
            return

        for path in args.INPATH:
            if os.path.isfile(path):
                run(path, of)
            elif args.RECURSE:
                path_list = get_recursive_path_list(path)
                for path in path_list:
                    if os.path.isfile(path):
                        run(path, of)
            else:
                command = [argv[0], "-R"] + argv[1:]
                print(f"Path {path} is a directory and -R flag is not specified.")
                print(f"Try running: {' '.join(command)}")
                return


if __name__ == "__main__":
    sys.exit(main(sys.argv))
