#!/bin/python3

# Copyright 2025, Anufriev Ilia, anufriewwi@rambler.ru
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import argparse
import os

parser = argparse.ArgumentParser('Parser of the -fstack-usage dumps')
parser.add_argument('-f', '--file', type=str, dest='FILENAME',
                    help='read FILENAME instead of stdin')
parser.add_argument('-p', '--full-paths', action='store_true', dest='FULLPATH',
                    help='show full file paths instead of just filenames')
parser.add_argument('--csv', action='store_true', dest='CSV',
                    help='print table in .csv format with \';\' as a delimiter')
args = parser.parse_args()

class SuLine:
    file      : str
    file_short: str
    line      : int
    col       : int
    func      : str
    size      : int # in bytes
    type      : str

    def __init__(self, file: str, line: int, col: int, func: str, size: int, type: str):
        self.file = file
        self.line = line
        self.col  = col
        self.func = func
        self.size = size
        self.type = type
        self.file_short = os.path.basename(file)

    def __dict__(self):
        return {
                'file' : self.file,
                'line' : self.line,
                'col'  : self.col,
                'func' : self.func,
                'size' : self.size,
                'type' : self.type
            }

    def __str__(self):
        return str(self.__dict__())

    def to_str_list(self):
        return list(map(str, self.__dict__().values()))

    def to_str_list_short_filename(self):
        l = self.to_str_list()
        l[0] = self.file_short
        return l

def su_parse(istr: str) -> list[SuLine]:
    lines = list(map(str.strip, istr.strip().split('\n')))
    parsed_lines = []

    for line in lines:
        tokens = []
        tokens = line.split(':')
        last   = tokens.pop()
        tokens.extend(list(map(str.strip, last.split('\t'))))

        parsed_lines.append(
                SuLine(tokens[0],
                int(tokens[1]),
                int(tokens[2]),
                tokens[3],
                int(tokens[4]),
                tokens[5])
            )

    return parsed_lines

def su_count_totals(pdata: list[SuLine]):
    sizes = []

    for line in pdata:
        sizes.append(line.size)

    return sum(sizes)

def format_table(table:list[list[str]], padding = 4):
    out = ''
    is_first_line = True

    for line in table:
        for col in range(0, len(line)):
            if len(line[col]) > len(table[0][col]):
                table[0][col] = table[0][col].ljust(len(line[col]), ' ')

    for line in table:
        is_first = True
        if not is_first_line:
            out += '\n'

        for i in range(0, len(line)):
            if not is_first:
                out += ' ' * padding

            is_first = False
            out += line[i].ljust(len(table[0][i]))

        is_first_line = False

    return out

def main(argv):
    input = ''

    if args.FILENAME:
        fout  = open(args.FILENAME, 'r')
        input = fout.read()
        fout.close()
    else:
        input = sys.stdin.read()

    if len(input) == 0:
        return 0


    pdata = su_parse(input)
    table = [['Filename', 'Line', 'Column', 'Function', 'Size, bytes', '%', 'Stack type']]
    total = su_count_totals(pdata)

    # table hdr
    for d in pdata:
        if args.FULLPATH:
            table.append(d.to_str_list())
        else:
            table.append(d.to_str_list_short_filename())

        table[-1].insert(-1, format((d.size / total) * 100, '0.2f') + '%')

    if args.CSV:
        is_first_line = True
        for line in table:
            if not is_first_line:
                print()

            is_first_col = True
            for col in line:
                if not is_first_col:
                    print(';', end='')

                print(col, end='')
                is_first_col = False

            is_first_line = False
        print()
    else:
        print(format_table(table))

    print(f'Total: {total}')

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
