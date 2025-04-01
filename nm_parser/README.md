# nm_parser

This is a little scriptlet that parses the output of this command:

```console
$ nm --size-sort --print-size FILENAME
0000000000009058 0000000000000001 b completed.0
00000000000024bf 000000000000000b T SomeFunction
0000000000001962 000000000000002e t SomeStaticFunction
0000000000001a48 0000000000000034 T AnotherFunction
0000000000003340 0000000000000040 R AConstant1
0000000000003580 0000000000000040 R AConstant2
00000000000035c0 0000000000000040 R AConstant3
0000000000003600 0000000000000040 R AConstant4
0000000000003380 0000000000000040 R AConstant5
00000000000033c0 0000000000000040 R AConstant6
...
```

The output of the parse process is a table with total sizes of symbols of each type. This script may be helpful to determine the amount of bytes that static data takes up in the executable or library file.

## Usage

To see usage, use -h flag:

```console
$ python3 nm_parser.py -h
usage: nm_parser.py [-h] [--csv] [--run-nm FILENAME]

nm output parser for nm --size-sort --print-size

options:
  -h, --help         show this help message and exit
  --csv              output data in the .csv format
  --run-nm FILENAME  run nm --size-sort --print-size <FILE> and parse output
```

## Examples

There are two ways of using nm_parser.py

### 1. Pipe output of the nm command into it

Like this:

```console
$ nm --size-sort --print-size /path/to/file | python3 nm_parser.py
Reading from stdin

Result:
Type    Total size, Bytes    Total size (hex), bytes    Percentage    Type Description
b       65537                0x10001                    97.50%        Symbol in the uninitialized data section (BSS) with local (static) scope.
B       35                   0x23                       0.05%         Symbol in the uninitialized data section (BSS) with global scope.
D       20                   0x14                       0.03%         Symbol in the initialized data section with global scope.
R       4                    0x4                        0.01%         Symbol in the read-only data section with global scope.
r       37                   0x25                       0.06%         Symbol in the read-only data section with local (static) scope.
T       1202                 0x4b2                      1.79%         Symbol in the text (code) section with global scope (often functions).
t       145                  0x91                       0.22%         Symbol in the text (code) section with local (static) scope.
d       240                  0xf0                       0.36%         Symbol in the initialized data section with local (static) scope.
```

### 2. Run nm from the script and parse its input

Like this:

```console
$ python3 nm_parser.py --run-nm /path/to/file
Running command: nm --size-sort --print-size /path/to/file

Result:
Type    Total size, Bytes    Total size (hex), bytes    Percentage    Type Description
b       65537                0x10001                    97.50%        Symbol in the uninitialized data section (BSS) with local (static) scope.
B       35                   0x23                       0.05%         Symbol in the uninitialized data section (BSS) with global scope.
D       20                   0x14                       0.03%         Symbol in the initialized data section with global scope.
R       4                    0x4                        0.01%         Symbol in the read-only data section with global scope.
r       37                   0x25                       0.06%         Symbol in the read-only data section with local (static) scope.
T       1202                 0x4b2                      1.79%         Symbol in the text (code) section with global scope (often functions).
t       145                  0x91                       0.22%         Symbol in the text (code) section with local (static) scope.
d       240                  0xf0                       0.36%         Symbol in the initialized data section with local (static) scope.
```