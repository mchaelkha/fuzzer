import argparse
import discover


def parser_init():
    main_parser = argparse.ArgumentParser(add_help=False)
    main_parser.add_argument('--custom-auth', nargs='?', type=str)
    main_parser.add_argument('url')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    discover_parser = subparsers.add_parser('discover', parents=[main_parser])
    discover_parser.add_argument('--common-words', nargs='?', type=str, required=True)
    discover_parser.add_argument('--extensions', nargs='?', type=str)

    test_parser = subparsers.add_parser('test', parents=[main_parser])
    test_parser.add_argument('--common-words', nargs='?', type=str, required=True)
    test_parser.add_argument('--extensions', nargs='?', type=str)
    test_parser.add_argument('--vectors', nargs='?', type=str, required=True)
    test_parser.add_argument('--sanitized-chars', nargs='?', type=str)
    test_parser.add_argument('--sensitive', nargs='?', type=str, required=True)
    test_parser.add_argument('--slow', nargs='?', type=int, default=500)

    return parser


if __name__ == '__main__':
    parser = parser_init()
    args = parser.parse_args()
    print("Starting fuzzing operations...")
    # Make sure url ends with /
    if args.url[-1] != '/':
        args.url += '/'
    if args.command == 'discover':
        print("Now discovering: " + args.url)
        discover.discover(args)
    if args.command == 'test':
        print("Now testing: " + args.url)
