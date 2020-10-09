import discover
import argparse


def parser_init():
    main_parser = argparse.ArgumentParser(add_help=False)
    main_parser.add_argument('--custom-auth', nargs='?', type=str)
    main_parser.add_argument('url')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    discover_parser = subparsers.add_parser('discover', parents=[main_parser])
    discover_parser.add_argument('--common-words', nargs='?', type=str, required=True)
    discover_parser.add_argument('--extensions', nargs='?', type=str, required=False)

    test_parser = subparsers.add_parser('test', parents=[main_parser])
    test_parser.add_argument('--common-words', nargs='?', type=str, required=True)
    test_parser.add_argument('--extensions', nargs='?', type=str, required=False)

    return parser


if __name__ == '__main__':
    parser = parser_init()
    args = parser.parse_args()
    print("Starting fuzzing operations...")
    if args.command == 'discover':
        print("Now discovering: " + args.url)
        discover.discover(args)
    if args.command == 'test':
        print("Now testing: " + args.url)
