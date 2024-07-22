# Simple Evaluation Test Harness

We commonly have to run a command at the CLI over a variety of inputs and options.  We have to time the running of this command and tally its results in a CSV file.

This repo contains some simple scripts to run commands at the CLI with options for performance evaluations.  The top-level script is testrunner.py .  Helper functions are found in util.py .

## Usage
1. Git clone this repo so the these scripts are inside a directory called `testrunner`.

2. Create a virtual environment as in:
    `python3 -m venv venv`       -- creates a directory called venv for a virtual python env 
    `source venv/bin/activate`   -- activates virtual environment
    `python -m pip install -r requirements.txt` -- installs python dependencies in venv
    `deactivate`                    -- exit the virtual env

    The virtual environment can be removed at any time using rm -rf venv 
    The eval_portus.py (used below) script operates in the virtual environment using a shebang #!venv/bin/python3

3. The python script that calls these scripts should contain:
   `import testrunner` and `import util` along with configuration and calls the the testrunner class.

4. Two examples of scripts that uses these evaluation scripts can be found in `example-simple.py` and `example-fortress.py`.  Inputs are provided for example-simple.py but example-fortress.py is not runnable.


Documentation on how to use the testrunner.py script can be found in the example.  

It is unlikely that you should have to modify these scripts to run your own evaluation.  But if you do modify these scripts then perhaps, the evaluation-scripts repo should be updated.

## Acknowledgements

These scripts were mainly written by Owen Zila with modifications by Nancy Day.
