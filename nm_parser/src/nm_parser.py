#!/bin/python3

import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(
            description="nm output parser for nm --size-sort --print-size"
        )
parser.add_argument('--csv', action='store_true', help='output data in the .csv format')
parser.add_argument('--run-nm', type=str, help='run nm --size-sort --print-size <FILE> and parse output', dest="FILENAME")
args = parser.parse_args()

g_nm_tags = {
    "A": "Absolute symbol. Not affected by relocation. Typically used for constants.",
    "B": "Symbol in the uninitialized data section (BSS) with global scope.",
    "b": "Symbol in the uninitialized data section (BSS) with local (static) scope.",
    "C": "Common symbol. Uninitialized variable (often with common linkage).",
    "D": "Symbol in the initialized data section with global scope.",
    "d": "Symbol in the initialized data section with local (static) scope.",
    "G": "Symbol in the initialized data section for small objects with global scope.",
    "g": "Symbol in the initialized data section for small objects with local (static) scope.",
    "I": "Indirect symbol, pointing to another symbol.",
    "N": "Debugging symbol.",
    "R": "Symbol in the read-only data section with global scope.",
    "r": "Symbol in the read-only data section with local (static) scope.",
    "S": "Symbol in the uninitialized data section for small objects with global scope.",
    "s": "Symbol in the uninitialized data section for small objects with local (static) scope.",
    "T": "Symbol in the text (code) section with global scope (often functions).",
    "t": "Symbol in the text (code) section with local (static) scope.",
    "U": "Undefined symbol, referenced but not defined in the object file.",
    "W": "Weak symbol with global scope.",
    "w": "Weak symbol with local (static) scope.",
    "V": "Weak object symbol in the COMDAT group with global scope.",
    "v": "Weak object symbol in the COMDAT group with local (static) scope.",
    "?": "Unknown or unidentified symbol type."
}

class NMSymbolData:
    offset: int
    size:   int
    name:   str
    type:   str

    def __init__(self, sym_offset: int, sym_size: int,
                       sym_type: str,   sym_name: str):
        self.offset = sym_offset
        self.size   = sym_size
        self.name   = sym_name
        self.type   = sym_type

    def __str__(self):
        return f'NMSymbolData[ Name: {self.name} Type: {self.type} ' + \
               f'Offset: {self.offset} (hex: {hex(self.offset)}) '   + \
               f'Size: {self.size} (hex: {hex(self.size)}) ]'

def nm_parse(input: str) -> list[NMSymbolData]:
    input_lines = input.strip().split('\n')
    tokens: list[list[str]] = []
    data = []

    for line in input_lines:
        tokens.append(line.strip().split(' '))

    for line_tokens in tokens:
        data.append(NMSymbolData(sym_offset = int(line_tokens[0], 16),
                                 sym_size   = int(line_tokens[1], 16),
                                 sym_type   = line_tokens[2],
                                 sym_name   = line_tokens[3]))
    return data

def nm_get_total_size_per_type(data: list[NMSymbolData]) -> dict[str, int]:
    totals: dict[str, int] = {}

    for d in data:
        if not d.type in totals.keys():
            totals[d.type] = d.size
            continue

        totals[d.type] += d.size

    return totals

def nm_get_percentage_per_type(totals: dict[str, int]) -> dict[str, float]:
    grand_total = 0
    percentages: dict[str, float] = {}

    grand_total = sum(totals.values())

    for type in totals.keys():
        percentages[type] = totals[type] / grand_total

    return percentages

def format_table(table:list[list], padding = 4):
    out = ''
    is_first_line = True
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

def cmd_to_str(cmd: list[str]):
    return ' '.join(map(str, cmd))

def main(argv):
    input: str

    if args.FILENAME:
        cmd = ['nm', '--size-sort', '--print-size', args.FILENAME]

        print(f'Running command: {cmd_to_str(cmd)}')
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f'Failed to run command {cmd}. Error:\n{result.stderr}')

        input = result.stdout
    else:
        print(f'Reading from stdin')
        input = sys.stdin.read()
        if len(input) == 0:
            return 0

    data = nm_parse(input)
    totals = nm_get_total_size_per_type(data)
    percentages = nm_get_percentage_per_type(totals)
    sep = '\t'
    table: list[list[str]] = [['Type', 'Total size, Bytes', 'Total size (hex), bytes', 'Percentage', 'Type Description']]

    for type in totals.keys():
        table.append([type, str(totals[type]),
                      str(hex(totals[type])),
                      f'{percentages[type] * 100:.02f}%',
                      g_nm_tags[type]])

    if args.csv:
        sep = ';'
        for line in table:
            is_first = True
            for item in line:
                if not is_first:
                    print(sep, end='')

                is_first = False
                print(item, end='')

            print()
        return 0

    print('\nResult:')
    print(format_table(table))
    print(f'Total: {sum(totals.values())} bytes')

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))