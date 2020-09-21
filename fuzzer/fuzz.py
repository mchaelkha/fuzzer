import discover
import argparse


def parser_init():
    parser = argparse.ArgumentParser()
    parser.add_argument('discover', type=str)
    parser.add_argument('url', type=str)
    parser.add_argument('--custom-auth', required=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = parser_init()
    if args.custom_auth == 'dvwa':
        discover.discover(args)
