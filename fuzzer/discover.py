import mechanicalsoup
import urllib.parse
from collections import defaultdict

line_sep = '====================\n{}'
line_double_sep = '====================\n{}\n===================='
space_sep = '    {}'

def dvwa_auth(browser, url):
    # Go to setup page and reset the database
    browser.open(urllib.parse.urljoin(url, '/setup.php'))
    browser.select_form('form[action="#"]')
    browser.submit_selected()

    # Go to login page and login as admin
    browser.open(url)
    browser.select_form('form[action="login.php"]')
    browser['username'] = 'admin'
    browser['password'] = 'password'
    browser.submit_selected()

    # Change security level to low
    browser.open(urllib.parse.urljoin(url, '/security.php'))
    browser.select_form('form[action="#"]')
    browser['security'] = 'low'
    browser.submit_selected()


def read_extensions(filename, exts):
    with open(filename) as ef:
        for line in ef:
            line = line.strip()
            exts.append(line)


def read_common_words(filename, paths):
    with open(filename) as wf:
        for line in wf:
            line = line.strip()
            paths.append(line)


def find_cookies(browser):
    print(line_sep.format('COOKIES'))
    for cookie in browser.session.cookies:
        print(space_sep.format(cookie))
    print(line_sep.format(''))


def page_guessing(browser, url, paths, exts, pages):
    if browser.open(url).status_code == 200:
        pages.add(url)
    for path in paths:
        for ext in exts:
            page = url + path + ext
            resp = browser.open(page)
            if resp.status_code == 200:
                pages.add(page)
    return pages


def page_crawling(browser, pages):
    pass


def parse_pages(browser, pages):
    forms = defaultdict(list)
    for page in pages:
        """
            1. get html
            2. find input form fields
            3. append to forms dict
        """
        pass
    # Print inputs discovered on each page
    print(line_double_sep.format("INPUT FORMS ON PAGES:"))
    for page in forms.keys():
        print(page)
        for form in forms[page]:
            print(space_sep.format(form))
    return forms


def discover(args):
    browser = mechanicalsoup.StatefulBrowser()
    url = args.url
    if args.custom_auth == 'dvwa':
        dvwa_auth(browser, url)

    # Populate extensions from file or with default values
    exts = []
    if args.extensions:
        read_extensions(args.extensions, exts)
    else:
        print('Using default file extensions...')
        exts.append('.php')
        exts.append('')

    # Populate paths from common_words file
    paths = []
    if args.common_words:
        read_common_words(args.common_words, paths)
    else:
        print('Missing required common-words argument...')
        exit(1)

    # First guess the pages
    pages = set()
    page_guessing(browser, url, paths, exts, pages)

    # Now discover other pages from pages guessed by crawling
    page_crawling(browser, pages)


    print(line_double_sep.format('LINKS FOUND ON PAGE:'))
    for page in pages:
        print(page)

    find_cookies(browser)
