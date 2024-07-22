"""
    This is an example of how to use the testrunner evaluation script to call
    the 'fortress' command with multiple values for the options iterating through filenames
    listed in an input file.
    Output is tallied to a CSV file.

    The steps are:
    1) Set a bunch of options, including how to interpret regular and timeout outputs
    2) Create a CSVTestRunner and execute its .run method.
"""

import logging
import subprocess
import psutil

from testrunner import testrunner as tr
from testrunner import util


# Timeout in seconds
TIMEOUT: int = 20 * 60  # 20 mins

# The command to run
# You may want a java command to set memory appropriately
# I chose a large timeout so the test harness checks the timeout, not Fortress
# the options that will be filled in with values are {compiler} and {model}
COMMAND = 'fortress -t 999999 --compiler {compiler} {model}'

# Values to fill in for the {compiler} option
compiler: tr.Option = tr.Option('compiler', [
    "Standard",
    "StandardSICompiler",
])

# Values to fill in for the {model} option
# In this case, we will read the option values from a file
# Each filename of a model should be on one line
model: tr.Option = tr.FromFileOption('model', "models.txt")

# The file to write output to
OUTPUT_FILE_NAME: str = f'test-{util.now_string()}.csv'

# how many times do we want to run each command?
ITERATIONS = 1

# To resume in the middle of an execution
SKIP = 0  # number of iterations to skip

FORCE_HEADER = False # rewrite the csv header

# Level of debug
util.setup_logging_debug()
# or:
#util.setup_logging_default()

# These are the string names of the fields that we want to determine the values
# of from the results of the command
# not needed?
# result_fields = ['return_code', 'time_elapsed', 'satisfiability']

# Fill in result fields when the process completes
# opts are the options we outlined above
# result is what the subprocess sends back
# time_elapsed comes from the timer
# returns a dictionary with values for results_fields above
def result_values(opts: tr.OptionDict, result: subprocess.CompletedProcess, time_elapsed: float) -> tr.OptionDict:
    # when the result has an error, put something special in the logging output
    if result.returncode != 0:
        logging.error('------OUTPUT------\n' + result.stdout + '------STDERR-----\n' + result.stderr +"------------")

    # interpret the satisfiability output
    # this is standard stuff so it's in a util function
    satisfiability: str = util.satisfiability_of_output(result.stdout)
    
    results: tr.OptionDict = {
        # dictionary keys must match result_fields above?
        'return_code': result.returncode,
        'time_elapsed': time_elapsed,
        'satisfiability': satisfiability
    }

    # Ensure no active z3 processes
    kill_z3()
    return results

# Fill in result fields when the process times out
# same arguments as above except for timeout
# returns a dictionary with values for results_fields above
def timeout_values(opts: tr.OptionDict, result: subprocess.TimeoutExpired) -> tr.OptionDict:
    logging.info('Timed out.')
    results: tr.OptionDict = {
        'return_code': 999,
        'time_elapsed': -1,  # the actual value for the timeout limit was an option input
        'satisfiability': 'UNKNOWN',
    }
    # Ensure no active child processes; Z3 does not always quit when
    # parent process timeouts
    util.kill_child_processes()
    return results

# This is the call to the CSVTestRunner to execute the runs
with open(OUTPUT_FILE_NAME, 'w') as output_file:
    runner = tr.CSVTestRunner(
        COMMAND,  # command string with blanks to fill in
        compiler, # option
        model, # option
        timeout=TIMEOUT,
        output_file=output_file,
        fields_from_result=result_values, # how to interpret results of run
        fields_from_timeout=timeout_values,   # how to interpret timeouts
    )  
runner.run(ITERATIONS, SKIP, FORCE_HEADER)