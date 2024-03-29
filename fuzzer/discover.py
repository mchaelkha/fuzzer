from collections import defaultdict
import urllib.parse
from util import *


def read_args(args):
    # Populate extensions from file or with default values
    exts = []
    if args.extensions:
        read_file(args.extensions, exts)
    else:
        print('Using default file extensions...')
        exts.append('.php')
        exts.append('')

    # Populate paths from common_words file
    paths = []
    if args.common_words:
        read_file(args.common_words, paths)
    return exts, paths


def dvwa_auth(browser):
    url = 'http://localhost/'
    # Go to setup page and reset the database
    browser.open(urllib.parse.urljoin(url, '/setup.php'))
    browser.select_form('form[action="#"]')
    browser.submit_selected()

    # Go to login page and login as admin
    browser.open(urllib.parse.urljoin(url, '/login.php'))
    browser.select_form('form[action="login.php"]')
    browser['username'] = 'admin'
    browser['password'] = 'password'
    browser.submit_selected()

    # Change security level to low
    browser.open(urllib.parse.urljoin(url, '/security.php'))
    browser.select_form('form[action="#"]')
    browser['security'] = 'low'
    browser.submit_selected()


def page_guessing(browser, url, paths, exts, pages):
    if browser.open(url).status_code == 200:
        pages.add(url)
    for path in paths:
        for ext in exts:
            page = urllib.parse.urljoin(url, path + ext)
            # Do not go to logout.php
            if 'logout.php' in page:
                continue
            resp = browser.open(page)
            if resp.status_code == 200:
                pages.add(page)
    return pages


def page_crawling(browser, url, pages):
    crawl_pages = set()
    crawl_pages.update(pages)
    visited_pages = set()
    # Begin crawl search
    while len(crawl_pages) > 0:
        page = crawl_pages.pop()
        visited_pages.add(page)
        if 'logout' in page:
            continue
        resp = browser.open(page)
        if resp.soup is None or resp.status_code != 200:
            pages.remove(page)
            continue
        links = browser.links()
        for link in links:
            href = ''
            link_href = link.get('href')
            if link_href.startswith('?'):
                href = urllib.parse.urljoin(page, link_href)
            else:
                href = urllib.parse.urljoin(url, link_href)
            if url in href and href not in visited_pages:
                pages.add(href)
                crawl_pages.add(href)


def input_crawling(browser, pages):
    form_inputs = defaultdict(set)
    query_param_pages = set()
    for page in pages:
        if 'logout' in page:
            continue
        browser.open(page)
        soup = browser.get_current_page()
        form_elements = soup.find_all('form')
        # Keep pages with different query parameters the same
        page_title = page.split('?')[0]
        if not form_elements:
            form_inputs[page_title] = set()
            if '?' in page:
                query_param_pages.add(page)
            continue
        for form in form_elements:
            inputs = form.find_all('input')
            for input in inputs:
                # Prefer to use 'name' over 'value' if possible
                if 'name' in input.attrs:
                    form_inputs[page_title].add(input.attrs['name'])
                elif 'value' in input.attrs:
                    form_inputs[page_title].add(input.attrs['value'])
    return form_inputs, query_param_pages


def print_discover_output(formatted_pages, guesses, form_inputs, cookies):
    # Print out the links guessed and discovered
    print(line_double_sep.format('LINKS FOUND ON PAGE:'))
    for page in formatted_pages.keys():
        query_params = formatted_pages[page]
        # If there exists a query parameter
        if len(query_params) > 0:
            print("{}, 'query_parameters(?=)': {}".format(page, query_params))
        else:
            print(page)

    print(line_sep.format(''))

    print(line_sep.format('LINKS SUCCESSFULLY GUESSED:'))
    for guess in guesses:
        print(guess)
    print(line_sep.format(''))

    # Print inputs discovered on each page
    print(line_double_sep.format('INPUT FORMS ON PAGES:'))
    for page in form_inputs.keys():
        print(page)
        for input in form_inputs[page]:
            print(space_sep.format(input))

    if cookies:
        print(line_sep.format('COOKIES'))
        for cookie in cookies.keys():
            print(space_sep.format(cookie + ': ' + cookies[cookie]))
        print(line_sep.format(''))


def discover(browser, args):
    url = args.url
    if args.custom_auth == 'dvwa':
        dvwa_auth(browser)

    exts, paths = read_args(args)

    # First guess the pages
    pages = set()
    page_guessing(browser, url, paths, exts, pages)
    guesses = set()
    guesses.update(pages)

    # Now discover other pages from pages guessed by crawling
    page_crawling(browser, url, pages)

    # Reformat links found and query parameters to a list
    formatted_pages = defaultdict(list)
    for page in pages:
        if '?' in page:
            parts = page.split('?', 2)
            formatted_pages[parts[0]].append(parts[1])
        elif not formatted_pages[page]:
            formatted_pages[page] = []

    # Now discover inputs on each page
    form_inputs, query_param_pages = input_crawling(browser, pages)

    return formatted_pages, guesses, form_inputs, pages, query_param_pages
