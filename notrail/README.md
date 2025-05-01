# notrail: Remove trailing whitespaces from files

**notrail** is a simple one-file utility that helps you to remove whitespaces from you files. It can even do so recursively!

## Dependencies

The only thing you'll need is python3. I used version 3.11. There is no guarantee that it will work on earlier versions  :(

## How to use it

You can use --help to see a help message:

```
$ ./notrail.py --help
usage: notrail [-h] [-R] [-s] [--overwrite] [-p] [-c] [--show-where] FILE [FILE ...]

Helps you remove trailing whitespace from files

positional arguments:
  FILE                  File from which the whitespace will be removed. When -R flag is enabled, a directory can be given

options:
  -h, --help            show this help message and exit
  -R, --recursive       Go through directory recursively and remove whitespace from all files along the way
  -s, --save-originals  Save original files into <filename>.<extension>.notrail_original
  --overwrite           If an original file with name <filename>.<extension>.notrail_original old already exists, overwrite it
  -p, --preview         Display files with visible whitespaces
  -c, --check           Check and tell if the file has trailing whitespaces. Returns 0 if the file contains no trailing ws, and 1 otherwise
  --show-where          Show where check found a trailing whitespace
```

The general principle though is simple: give all the files you want to be notrail'ed as positional arguments. If you want to notrail the whole directory recursively, you can do that by using an -R flag.

```
$ ./notrail.py file1 file2 file3

# or

$ ./notrail.py -R dir
```

If you are worried that the originals will get overwritten, you may want to use *--save-originals* flag. It will create a file with ".notrail\_original" suffix alongside original ones.

You can run notrail with --check flag to see whether or not a file has trailing whitespaces in it. If you see that it returned "1" then you can use --show-where flag, it will show precisely on which lines in the file trailing whitespaces were found.
