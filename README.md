# fuzzer
SWEN-331 fuzzer project.

@TA I have received an extension on Part 2 to be due on 2020-10-27 @ 11:59PM.

## Assumptions
* Submitting the file upload form results in an OSError. This was counted as an HTTP response error.
* A page and its state after submitting a possible form are two separate cases of data leakage.
* "refresh" the page after submitting a form in case of redirects or HTML changes

## Installation
* Run `pip install -r requirements`. This is ran in the [GitLab CI](.gitlab-ci.yml) file.

## Running
* GitLab CI - `.gitlab-ci.yml` file is provided for running with a few different options.
* Local - Run the fuzzer on DVWA or fuzzer-tests with provided .txt files. `[]` are optional flags.
	* DVWA:
	```sh
	python3 fuzzer/fuzz.py discover http://localhost/ [--custom-auth=dvwa] --common-words=common-words.txt [--extensions=common-extensions.txt]
	python3 fuzzer/fuzz.py test http://localhost/ [--custom-auth=dvwa] --common-words=common-words.txt [--extensions=common-extensions.txt] --vectors=vectors.txt --sensitive=sensitive.txt [--slow=TIME_MS] [--sanitized-chars=sanitized-chars.txt]
	```
	* /fuzzer-tests:
	```sh
	python3 fuzzer/fuzz.py discover http://127.0.0.1/fuzzer-tests --common-words=common-words.txt [--extensions=common-extensions.txt]
	python3 fuzzer/fuzz.py test http://127.0.0.1/fuzzer-tests --common-words=common-words.txt [--extensions=common-extensions.txt] --vectors=vectors.txt --sensitive=sensitive.txt [--slow=TIME_MS] [--sanitized-chars=sanitized-chars.txt]
	```
