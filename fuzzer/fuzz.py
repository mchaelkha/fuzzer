import argparse
import mechanicalsoup


def parser_init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--custom-auth', required=False)
    parser.add_argument('discover', type=str)
    parser.add_argument('url', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    args = parser_init()

    browser = mechanicalsoup.StatefulBrowser()
    response = browser.open(args.url)
    print(response)
