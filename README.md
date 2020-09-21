# fuzzer
SWEN-331 fuzzer project.

## Installation
* Run `pip install -r requirements`. This is ran in the [GitLab CI](.gitlab-ci.yml) file.

## Running
* DVWA: `python3 fuzzer/fuzz.py discover http://localhost/ --custom-auth=dvwa`
* Other: `python3 fuzzer/fuzz.py discover http://127.0.0.1/fuzzer-tests`
