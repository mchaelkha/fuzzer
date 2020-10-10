import mechanicalsoup
import urllib.parse


def dvwa_auth(url):
    browser = mechanicalsoup.StatefulBrowser()
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


def read_common_words(filename, words):
    with open(filename) as wf:
        for line in wf:
            line = line.strip()
            words.append(line)


def discover(args):
    if args.custom_auth == "dvwa":
        dvwa_auth(args.url)

    # Populate extensions from file or with default values
    exts = []
    if args.extensions:
        read_extensions(args.extensions, exts)
    else:
        print("Using default file extensions...")
        exts.append('.php')
        exts.append('')

    # Populate filenames from common_words file
    filenames = []
    if args.common_words:
        read_common_words(args.common_words, filenames)
    else:
        print("Missing required common-words argument...")
        exit(1)
