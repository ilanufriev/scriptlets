#!/bin/python3

import os
import sys
import argparse

parser = argparse.ArgumentParser(prog='notrail',
                                 description='Helps you remove trailing ' +
                                             'whitespace from files')

parser.add_argument('-R', '--recursive', action='store_true', dest='RECURSE',
                    help='Go through directory recursively and remove ' +
                         'whitespace from all files along the way')

parser.add_argument('FILE',
                    help='File from which the whitespace will be ' +
                         'removed. When -R flag is enabled, a directory can be given',
                    nargs='+')

parser.add_argument('-s', '--save-originals', action='store_true', dest='SAVE_ORIGINALS',
                    help='Save original files into <filename>.<extension>.notrail_original')

parser.add_argument('--overwrite', action='store_true', dest='OVERWRITE',
                    help='If an original file with name <filename>.<extension>.notrail_original already exists, overwrite it')

parser.add_argument('-p', '--preview', action='store_true', dest='PREVIEW',
                    help='Display files with visible whitespaces')

parser.add_argument('-c', '--check', action='store_true', dest='CHECK',
                    help='Check and tell if the file has trailing whitespaces. ' +
                         'Returns 0 if the file contains no trailing ws, and 1 otherwise')

parser.add_argument('--show-where', action='store_true', dest='SHOW_WHERE',
                    help='Show where check found a trailing whitespace')

args = parser.parse_args()

def get_preview_contents(lines: list[str], wschar: str) -> str:
    processed_lines = []

    for line in lines:
        pline = ''
        for c in line:
            if c == ' ':
                pline += wschar
            else:
                pline += c

        processed_lines.append(pline)

    return '\n'.join(processed_lines)

def get_removed_ws_contents(lines: list[str]) -> str:
    processed_lines = []
    for line in lines:
        processed_lines.append(line.rstrip(' '))

    return '\n'.join(processed_lines)

def check(path: str, lines: list[str]):
    result = False
    for i in range(0, len(lines)):
        if len(lines[i]) == 0:
            continue

        if lines[i][-1] == ' ':
            if args.SHOW_WHERE:
                print(f'Found newline in file {path}:{i + 1}: {get_preview_contents([lines[i]], "`")}')
            result = True

    return result 

def rstrip_newlines(s: str):
    return s.rstrip('\n')

def run(path: str): 
    file = open(path, 'r')

    try:
        lines = file.readlines()
    except UnicodeDecodeError:
        print(f'File {path} is binary and is skipped')
        file.close()
        return

    file.close()

    if args.SAVE_ORIGINALS:
        mode = 'x'
        if args.OVERWRITE:
            mode = 'w'

        original = open(path + '.notrail_original', mode)
        original.write(''.join(lines))
        original.close()

    lines = list(map(rstrip_newlines, lines))

    if args.PREVIEW:
        print(get_preview_contents(lines, '`'))
        return

    if args.CHECK:
        if check(path, lines) == True:
            print(f'{path}: 1')
        else:
            print(f'{path}: 0')
        return

    file = open(path, 'w') # we want to overwrite the file completely
    file.write(get_removed_ws_contents(lines))
    file.close()
    return

def get_recursive_path_list(root: str):
    path_list = []
    scan = os.scandir(root)
    for e in scan:
        if e.is_dir():
            path_list.extend(get_recursive_path_list(e.path))
        else:
            path_list.append(e.path)

    return path_list

def main(argv):
    if args.FILE is not None:
        for path in args.FILE:
            if args.RECURSE:
                if not os.path.isfile(path):
                    path_list = get_recursive_path_list(path)    
                    for path in path_list:
                        if os.path.isfile(path):
                            run(path)
            else:
                run(path)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
