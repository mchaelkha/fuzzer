from collections import defaultdict
from util import *


def read_args(args):
    vectors = []
    if args.vectors:
        read_file(args.vectors, vectors)

    sensitive_data = []
    if args.sensitive:
        read_file(args.sensitive, sensitive_data)

    sanitized_chars = []
    if args.sanitized_chars:
        read_file(args.sanitized_chars, sanitized_chars)
    else:
        sanitized_chars = ["<", ">"]

    slow = 500
    if args.slow:
        slow = args.slow

    return vectors, sensitive_data, sanitized_chars, slow


def check_pages(browser, pages, sensitive_data, slow):
    leak_count = 0
    response_count = 0
    slow_count = 0
    for page in pages:
        if 'logout' in page:
            continue
        resp = browser.open(page)
        for leak in sensitive_data:
            if leak in resp.text:
                leak_count += 1
        if resp.elapsed.total_seconds() >= slow / 1000:
            slow_count += 1
        if resp.status_code != 200:
            response_count += 1
    return leak_count, response_count, slow_count


def check_sanitization(browser, form_inputs, sensitive_data, chars, slow):
    phrase = "foo{}bar"
    unsanitized_count = 0
    leak_count = 0
    response_count = 0
    slow_count = 0
    for page in form_inputs.keys():
        if 'logout' in page:
            continue
        if not form_inputs[page]:
            continue
        resp = browser.open(page)
        soup = browser.get_current_page()
        form_elements = soup.find_all('form')
        for char in chars:
            browser.open(page)
            for form in form_elements:
                current_form = browser.select_form(form)
                inputs = form.find_all('input')
                test_phrase = phrase.format(char)
                try:
                    for input in inputs:
                        if 'name' in input.attrs and input.attrs['type'] != 'submit':
                            current_form.set(input.attrs['name'], test_phrase)
                    submit = form.find('input', {'type': 'submit'})
                    current_form.choose_submit(submit)
                    resp = browser.submit_selected()
                    if resp.status_code != 200:
                        response_count += 1
                    if resp.elapsed.total_seconds() >= slow / 1000:
                        slow_count += 1
                    for leak in sensitive_data:
                        if leak in resp.text:
                            leak_count += 1
                    if test_phrase in resp.text:
                        unsanitized_count += 1
                except OSError as e:
                    response_count += 1
                    continue
    return unsanitized_count, leak_count, response_count, slow_count


def print_test_output(unsanitized_count, leak_count, response_count, slow_count):
    print(line_double_sep.format(space_sep.format('TEST RESULTS')))
    print('Number of unsanitized inputs: {}'.format(unsanitized_count))
    print('Number of possible data leaks: {}'.format(leak_count))
    print('Number of HTTP/Response Code Errors: {}'.format(response_count))
    print('Number of slow responses: {}'.format(slow_count))


def test(browser, args, formatted_pages, pages, query_param_pages, form_inputs):
    vectors, sensitive_data, sanitized_chars, slow = read_args(args)

    total_leak_count = 0
    total_response_count = 0
    total_slow_count = 0

    leak_count, response_count, slow_count = check_pages(browser, pages, sensitive_data, slow)
    total_leak_count += leak_count
    total_response_count += response_count
    total_slow_count += slow_count

    unsanitized_count, leak_count, response_count, slow_count = check_sanitization(browser, form_inputs, sensitive_data, sanitized_chars, slow)
    total_leak_count += leak_count
    total_response_count += response_count
    total_slow_count += slow_count
    return unsanitized_count, total_leak_count, total_response_count, total_slow_count
