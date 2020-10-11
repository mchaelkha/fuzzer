# fuzzer
SWEN-331 fuzzer project.

## Installation
* Run `pip install -r requirements`. This is ran in the [GitLab CI](.gitlab-ci.yml) file.

## Running
* GitLab CI - `.gitlab-ci.yml` file is provided for running with a few different options.
* Local - Run the fuzzer on DVWA or fuzzer-tests with provided .txt files. `[]` are optional flags.
	* DVWA:
	```sh
	python3 fuzzer/fuzz.py discover http://localhost/ [--custom-auth=dvwa] --common-words="common-words.txt" [--extensions="common-extensions.txt"]
	```
	* /fuzzer-tests:
	```sh
<<<<<<< HEAD
	python3 fuzzer/fuzz.py discover http://127.0.0.1/fuzzer-tests --common-words="common-words.txt" [--extensions="common-extensions.txt"]
=======
	python3 fuzzer/fuzz.py discover http://127.0.0.1/fuzzer-tests --common-words="common-words.txt" --[extensions="common-extensions.txt"]
>>>>>>> c2beac80a55405d7762b6cbce7a66735e1125360
	```
