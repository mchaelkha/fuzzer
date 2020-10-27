import argparse
import mechanicalsoup
from discover import discover, print_discover_output
from test import test, print_test_output
from util import find_cookies


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


def discover_command(browser, args):
    print("Now discovering: " + args.url)
    formatted_pages, guesses, form_inputs, pages_without_forms = discover(browser, args)
    cookies = find_cookies(browser)
    print_discover_output(formatted_pages, guesses, form_inputs, cookies)


def test_command(browser, args):
    print("Now testing: " + args.url)
    formatted_pages, guesses, form_inputs, pages_without_forms = discover(browser, args)
    # print_discover_output(formatted_pages, guesses, form_inputs, cookies)
    unsanitized_count, leak_count, response_count, slow_count = test(browser, args, formatted_pages, pages_without_forms, form_inputs)
    cookies = find_cookies(browser)
    print_discover_output(formatted_pages, guesses, form_inputs, cookies)
    print_test_output(unsanitized_count, leak_count, response_count, slow_count)


if __name__ == '__main__':
    parser = parser_init()
    args = parser.parse_args()
    print("Starting fuzzing operations...")
    browser = mechanicalsoup.StatefulBrowser()
    # Make sure url ends with /
    if args.url[-1] != '/':
        args.url += '/'
    if args.command == 'discover':
        discover_command(browser, args)
    elif args.command == 'test':
        test_command(browser, args)
