import re
import argparse
import mechanicalsoup
import urllib.parse

parser = argparse.ArgumentParser()

# Browser connection to 127.0.0.1
dvwa_addr = 'http://127.0.0.1/'
browser = mechanicalsoup.StatefulBrowser()
response = browser.open(dvwa_addr)
print(response)

