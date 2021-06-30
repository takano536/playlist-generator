import argparse
import glob
import os
import sys
import itertools
import functools


EXT = [
    'mp3', 'wma', 'oma', 'flac', 'wav',
    'mp4', 'm4a', '3gp', 'aif', 'aiff',
    'afc', 'ogg', 'aifc'
]

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


def natural_sort_cmp(a_substr, b_substr):
    for i in range(min(len(a_substr), len(b_substr))):
        if a_substr[i].isdigit() and b_substr[i].isdigit():
            a_substr[i] = int(a_substr[i])
            b_substr[i] = int(b_substr[i])

        if a_substr[i] != b_substr[i]:
            return 1 if a_substr[i] > b_substr[i] else -1

        if i >= len(a_substr) - 1 or i >= len(b_substr) - 1:
            return 1 if i == len(a_substr) - 1 else -1
    return 0


def filename_natural_sort(a, b):
    a_substr = [''.join(substr) for _, substr in itertools.groupby(os.path.basename(a), str.isdigit)]
    b_substr = [''.join(substr) for _, substr in itertools.groupby(os.path.basename(b), str.isdigit)]
    return natural_sort_cmp(a_substr, b_substr)


def foldername_natural_sort(a, b):
    a_substr = [''.join(substr) for _, substr in itertools.groupby(a, str.isdigit)]
    b_substr = [''.join(substr) for _, substr in itertools.groupby(b, str.isdigit)]
    return natural_sort_cmp(a_substr, b_substr)


def ext_sort(a, b):
    a_ext = os.path.splitext(a)[1][1:]
    b_ext = os.path.splitext(b)[1][1:]
    if a_ext != b_ext:
        return 1 if a_ext > b_ext else -1
    return filename_natural_sort(a, b)


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


def duplicate_rename(filepath):
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

    if args.sort == 'filename-desc':
        files.sort(key=functools.cmp_to_key(filename_natural_sort), reverse=True)
    elif args.sort == 'foldername':
        files.sort(key=functools.cmp_to_key(foldername_natural_sort))
    elif args.sort == 'foldername-desc':
        files.sort(key=functools.cmp_to_key(foldername_natural_sort), reverse=True)
    elif args.sort == 'date' and os.name == 'nt':
        files.sort(key=lambda file_path: os.path.getctime(file_path))
    elif args.sort == 'date-desc' and os.name == 'nt':
        files.sort(key=lambda file_path: os.path.getctime(file_path), reverse=True)
    elif args.sort == 'ext':
        files.sort(key=functools.cmp_to_key(ext_sort))
    elif args.sort == 'ext-desc':
        files.sort(key=functools.cmp_to_key(ext_sort), reverse=True)
    else:
        files.sort(key=functools.cmp_to_key(filename_natural_sort))

    if create_playlist(files) == 0:
        print('Successfully created m3u8 file')
    else:
        print('Failed to create m3u8 file')


if __name__ == '__main__':
    main()
    print('Press enter key to quit...', end='')
    input()
    sys.exit(0)
