# Simple Test Harness

This test harness is a simple series of scripts meant to make building
evaluations easier and faster.

## Usage
1. Get the .zip module. In the future it may simply be in releases on the git repo, but for now it is simple to
build it oneself. 
   1. Clone the repo, then navigate inside it.
   2. Run `./distribute.sh` If you are on Windows you can instead run `py -m zipfile -c evaluationscripts.zip testrunner.py utils.py`
2. Put the .zip wherever you want.
3. Make it accessible to your evaluation script
   Either:
      - Add the .zip to your PYTHON_PATH
      - Add the following to your script
   ```python 
   import sys
   sys.path.insert(0, 'testharness/evaluationscripts.zip')  # Replace with the proper path
   ```
   You can then `import testrunner` or `import util`.
   