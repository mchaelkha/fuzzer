import re
import argparse
import mechanicalsoup
import urllib.parse

parser = argparse.ArgumentParser()

# Browser connection to 127.0.0.1
browser = mechanicalsoup.StatefulBrowser()
response = browser.open("127.0.0.1/")
print(response)

