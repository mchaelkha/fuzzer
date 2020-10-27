line_sep = '====================\n{}'
line_double_sep = '====================\n{}\n===================='
space_sep = '    {}'

def read_file(filename, arr):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            arr.append(line)

def find_cookies(browser):
    cookies = {}
    for cookie in browser.session.cookies:
        cookies[cookie.name] = cookie.value
    return cookies
