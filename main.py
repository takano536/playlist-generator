import argparse
import glob
import os
import sys
import itertools
import functools
import re


EXT = [
    'mp3', 'wma', 'oma', 'flac', 'wav',
    'mp4', 'm4a', '3gp', 'aif', 'aiff',
    'afc', 'ogg', 'aifc'
]

full_width = ''.join(chr(0xff01 + i) for i in range(94))
half_width = ''.join(chr(0x21 + i) for i in range(94))
full2half = str.maketrans(full_width, half_width)
symbol_regex = '[\\u3000 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'

parser = argparse.ArgumentParser()
parser.add_argument(
    'input',
    nargs='*',
    help='input music path or directory'
)
parser.add_argument(
    '-o', '--outname',
    help='output playlist filename'
)
parser.add_argument(
    '--outfolder',
    help='save the output in a certain folder'
)
parser.add_argument(
    '--sort',
    choices=['filename', 'foldername', 'date', 'ext', 'filename-desc', 'foldername-desc', 'date-desc', 'ext-desc'],
    default='name',
    help='how to sort songs (default=name)'
)
args = parser.parse_args()


def divide_num_char_sym(string: str):
    substr = list()
    string = string.translate(full2half)
    groups = itertools.groupby(string, lambda char: 1 if char.isdigit() else -1 if re.match(symbol_regex, char) else 0)
    for _, group in groups:
        substr.append(''.join(group))
    return substr


def natural_sort_cmp(a_str: str, b_str: str, ext_cmp: bool):
    if ext_cmp and os.path.splitext(a_str)[1] != os.path.splitext(b_str)[1]:
        return 1 if os.path.splitext(a_str)[1] > os.path.splitext(b_str)[1] else -1

    a_str, b_str = divide_num_char_sym(a_str), divide_num_char_sym(b_str)
    rep_cnt = 0
    for (a_substr, b_substr) in zip(a_str, b_str):
        a_swap, b_swap = False, False
        if re.match(symbol_regex, a_substr) and a_str[rep_cnt + 1].isdigit():
            a_str[rep_cnt], a_str[rep_cnt + 1] = a_str[rep_cnt + 1], a_str[rep_cnt]
            a_substr = a_str[rep_cnt]
            a_swap = True
        if re.match(symbol_regex, b_substr) and b_str[rep_cnt + 1].isdigit():
            b_str[rep_cnt], b_str[rep_cnt + 1] = b_str[rep_cnt + 1], b_str[rep_cnt]
            b_substr = b_str[rep_cnt]
            b_swap = True

        if a_substr.isdigit() and b_substr.isdigit():
            a_substr = float(a_substr) - len(a_substr) * 0.1
            b_substr = float(b_substr) - len(b_substr) * 0.1

        if a_substr != b_substr:
            return 1 if a_substr > b_substr else -1

        if a_swap != b_swap:
            return 1 if b_swap else -1

        rep_cnt += 1

    if len(a_str) == len(b_str):
        return 0
    else:
        return 1 if len(a_str) > len(b_str) else -1


def input_files():
    ret = []
    folders = []
    for arg in args.input:
        arg = arg.replace('/', os.sep)
        if not os.path.exists(arg):
            continue
        elif os.path.isfile(arg) and os.path.splitext(arg)[1][1:].lower() in EXT:
            ret.append(arg)
        elif os.path.isdir(arg):
            folders.append(arg)

    for folder in folders:
        for arg in glob.glob(folder + '/*'):
            arg = arg.replace('/', os.sep)
            if not os.path.exists(arg):
                continue
            elif os.path.isfile(arg) and os.path.splitext(arg)[1][1:].lower() in EXT:
                ret.append(arg)
    return ret


def duplicate_rename(filepath: str):
    if not os.path.exists(filepath):
        return os.path.basename(filepath)

    cnt = 1
    while 1:
        filepath_without_ext, file_ext = os.path.splitext(filepath)
        filepath_without_ext += ' (' + str(cnt) + ')'
        if not os.path.exists(filepath_without_ext + file_ext):
            return os.path.basename(filepath_without_ext + file_ext)
        cnt += 1


def search_parent_folder(files):
    files_substr = [os.path.abspath(filepath).split('\\') for filepath in files]
    files_substr.sort(key=len)
    common_substr = set(files_substr[0])
    for file_substr in files_substr:
        common_substr &= set(file_substr)

    parent_folder_path = ''
    for substr in files_substr[-1]:
        if {substr}.issubset(common_substr):
            parent_folder_path += substr + os.sep
    return parent_folder_path


def create_playlist(files):
    if files == []:
        parser.print_help(sys.stderr)
        print('\nPress enter key to quit...', end='')
        input()
        sys.exit(1)

    if args.outname is None:
        out_name = os.path.splitext(os.path.basename(files[0]))[0] + '.m3u8'
    else:
        out_name = args.outname if os.path.splitext(args.outname)[1].lower() == '.m3u8' else args.outname + '.m3u8'

    if args.outfolder is None:
        out_folder = search_parent_folder(files)
    else:
        out_folder = args.outfolder

    out_name = duplicate_rename(os.path.join(out_folder, out_name))

    try:
        f = open(os.path.join(out_folder, out_name), 'x', encoding='UTF-8')
    except Exception as e:
        print(e, file=sys.stderr)
        return -1

    f.write('#EXTM3U\n')
    for filepath in files:
        f.write('#EXTINF:,\n')
        f.write(os.path.relpath(filepath, out_folder).replace(os.sep, '/') + '\n')
    f.close()
    print('"' + out_name + '"', 'was created')
    print('path:', os.path.abspath(os.path.join(out_folder, out_name)))
    return 0


def main():
    files = input_files()

    for file in files:
        divide_num_char_sym(file)

    if args.sort == 'filename-desc':
        files.sort(key=functools.cmp_to_key(lambda a, b: natural_sort_cmp(os.path.basename(a), os.path.basename(b), False)), reverse=True)
    elif args.sort == 'foldername':
        files.sort(key=functools.cmp_to_key(lambda a, b: natural_sort_cmp(a, b, False)))
    elif args.sort == 'foldername-desc':
        files.sort(key=functools.cmp_to_key(lambda a, b: natural_sort_cmp(a, b, False)), reverse=True)
    elif args.sort == 'date' and os.name == 'nt':
        files.sort(key=lambda file_path: os.path.getctime(file_path))
    elif args.sort == 'date-desc' and os.name == 'nt':
        files.sort(key=lambda file_path: os.path.getctime(file_path), reverse=True)
    elif args.sort == 'ext':
        files.sort(key=functools.cmp_to_key(lambda a, b: natural_sort_cmp(os.path.basename(a), os.path.basename(b), True)))
    elif args.sort == 'ext-desc':
        files.sort(key=functools.cmp_to_key(lambda a, b: natural_sort_cmp(os.path.basename(a), os.path.basename(b), True)), reverse=True)
    else:
        files.sort(key=functools.cmp_to_key(lambda a, b: natural_sort_cmp(os.path.basename(a), os.path.basename(b), False)))

    if create_playlist(files) == 0:
        print('Successfully created m3u8 file')
    else:
        print('Failed to create m3u8 file')


if __name__ == '__main__':
    main()
    print('Press enter key to quit...', end='')
    input()
    sys.exit(0)
