import re
import argparse
import mechanicalsoup
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('discover', action='store_const',
                    help='discover a URL address argument')
parser.add_argument('--custom-auth=dvwa', action='store_const',
                    help='use custom authentication')
args = parser.parse_args()
print(args)

# Browser connection to 127.0.0.1
dvwa_addr = 'http://127.0.0.1/'
dvwa_test = dvwa_addr + 'fuzzer-tests'
browser = mechanicalsoup.StatefulBrowser()
response = browser.open(dvwa_addr)
print(response)

response = browser.open(dvwa_test)
print(response)

