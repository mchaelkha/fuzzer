from util import read_file


def read_args(args):
    vectors = []
    if args.vectors:
        read_file(args.vectors, vectors)

    sensitive_data = []
    if args.sensitive:
        read_file(args.sensitive, sensitive_data)

    sanitized_chars = []
    if args.sanitized_chars:
        read_file(args.sanitized_chars, sanitized_chars)
    else:
        sanitized_chars = ["<", ">"]

    slow = 500
    if args.slow:
        slow = args.slow

    return vectors, sensitive_data, sanitized_chars, slow


def test(browser, args):
    vectors, sensitive_data, sanitized_chars, slow = read_args(args)
