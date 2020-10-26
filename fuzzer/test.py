from util import read_file


def test(browser, args):
    # Populate extensions from file or with default values
    vectors = []
    if args.vectors:
        read_file(args.vectors, vectors)
    else:
        print('Using default file extensions...')
        exts.append('.php')
        exts.append('')

    # Populate paths from common_words file
    sensitive_data = []
    if args.sensitive:
        read_file(args.sensitive, sensitive_data)
    else:
        print('Missing required sensitive argument...')
        exit(1)
