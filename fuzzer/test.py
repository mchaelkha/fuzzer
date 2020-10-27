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


def check_sanitization(browser, form_inputs, chars):
    phrase = "foo{}bar"
    unsanitized_count = 0
    for page in form_inputs.keys():
        if not form_inputs[page]:
            continue
        browser.open(page)
        soup = browser.get_current_page()
        form_elements = soup.find_all('form')
        was_found = False

        for char in chars:
            for form in form_elements:
                current_form = browser.select_form(form)
                inputs = form.find_all('input')
                test_phrase = phrase.format(char)
                for input in inputs:
                    current_form.set(input.attrs['name'], test_phrase)
                submit = form.find('input', {'type': 'submit'})
                current_form.choose_submit(submit)
                resp = browser.submit_selected()
                soup = browser.get_current_page()
                was_found = False
                for tag in soup.contents:
                    if test_phrase in str(tag.__dict__):
                        was_found = True
                        break
                if was_found:
                    break
            if was_found:
                unsanitized_count += 1
                break
    return unsanitized_count

# res = browser.open(page)
# print(res.elapsed)

def print_formatted_output(unsanitized_count):
    print(line_double_sep.format(space_sep.format('TEST RESULTS')))
    print('Number of unsanitized inputs: {}'.format(unsanitized_count))


def test(browser, args, form_inputs):
    vectors, sensitive_data, sanitized_chars, slow = read_args(args)
    # print(form_inputs)
    # space_sep = '    {}'
    # for page in form_inputs.keys():
    #     print(page)
    #     for input in form_inputs[page]:
    #         print(space_sep.format(input))
    unsanitized_count = check_sanitization(browser, form_inputs, sanitized_chars)
    print_formatted_output(unsanitized_count)
