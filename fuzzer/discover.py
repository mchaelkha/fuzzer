import mechanicalsoup
import urllib.parse


def discover(args):
    if args.custom_auth == "dvwa":
        browser = mechanicalsoup.StatefulBrowser()
        # Go to setup page and reset the database
        browser.open(urllib.parse.urljoin(args.url, '/setup.php'))
        browser.select_form('form[action="#"]')
        browser.submit_selected()

        # Go to login page and login as admin
        browser.open(args.url)
        browser.select_form('form[action="login.php"]')
        browser['username'] = 'admin'
        browser['password'] = 'password'
        browser.submit_selected()

        # Change security level to low
        browser.open(urllib.parse.urljoin(args.url, '/security.php'))
        browser.select_form('form[action="#"]')
        browser['security'] = 'high'
        browser.submit_selected()
