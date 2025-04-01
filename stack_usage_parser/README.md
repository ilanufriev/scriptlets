# su_parser

This is a little scriptlet that parses .su files dumped by the -fstack-usage option in gcc:

```console
$ cat /path/to/file.c.su
/path/to/file.c:23:6:some_function	24	static
/path/to/file.c:41:6:some_function2	288	static
/path/to/file.c:79:6:some_function3	288	static
/path/to/file.c:121:6:some_function4	288	static
...
```

The output of the parse process is a prettier table with sizes of stacks for each function in the file. It also show the percentage, that the size of the stack of a particular function takes up in the grand total of all stack sizes. This script may be helpful to estimate the amount of bytes that stack takes at runtime.

## Usage

To see usage, use -h flag:

```console
$ python3 su_parser.py -h
usage: Parser of the -fstack-usage dumps [-h] [-f FILENAME] [-p] [--csv]

options:
  -h, --help            show this help message and exit
  -f FILENAME, --file FILENAME
                        read FILENAME instead of stdin
  -p, --full-paths      show full file paths instead of just filenames
  --csv                 print table in .csv format with ';' as a delimiter

```

## Examples

There are two ways of using su_parser.py

### 1. Pipe output of the nm command into it

Like this:

```console
$ cat example.txt | python3 su_parser.py
Filename    Line    Column    Function     Size, bytes    %         Stack type
file.c      23      6         function1    24             1.72%     static
file.c      41      6         function2    288            20.69%    static
file.c      79      6         function3    288            20.69%    static
file.c      121     6         function4    288            20.69%    static
file.c      153     6         function5    24             1.72%     static
file.c      170     6         function6    48             3.45%     static
file.c      178     6         function7    48             3.45%     static
file.c      191     6         function8    48             3.45%     static
file.c      210     6         function9    32             2.30%     static
file.c      229     6         functionA    16             1.15%     static
file.c      240     6         functionB    288            20.69%    static
Total: 1392

```

### 2. Run nm from the script and parse its input

Like this:

```console
$ python3 su_parser.py --file example.txt
Filename    Line    Column    Function     Size, bytes    %         Stack type
file.c      23      6         function1    24             1.72%     static
file.c      41      6         function2    288            20.69%    static
file.c      79      6         function3    288            20.69%    static
file.c      121     6         function4    288            20.69%    static
file.c      153     6         function5    24             1.72%     static
file.c      170     6         function6    48             3.45%     static
file.c      178     6         function7    48             3.45%     static
file.c      191     6         function8    48             3.45%     static
file.c      210     6         function9    32             2.30%     static
file.c      229     6         functionA    16             1.15%     static
file.c      240     6         functionB    288            20.69%    static
Total: 1392
```