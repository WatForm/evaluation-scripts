import subprocess

import testrunner as tr
import util

import argparse
from typing import *


# The folder the fortress
def generate_command(opts: tr.OptionDict) -> List[str]:
    return [
        'fortress',  # Invoke java
        '--timeout', opts['timeout'],
        '--scope', opts['scope_info'],
        opts['target_file']
    ]


result_fields = ['sat', 'return_code', 'time_elapsed']


def result_values(opts: tr.OptionDict, result: subprocess.CompletedProcess, time_elapsed: float) -> tr.OptionDict:
    results = {
        'sat': util.satisfiability_of_output(result.stdout),
        'return_code': result.returncode,
        'time_elapsed': time_elapsed
    }
    return results


def timeout_values(opts: tr.OptionDict, result: subprocess.TimeoutExpired) -> tr.OptionDict:
    results = {
        'sat': util.Satisfiablity.UNSURE,
        'return_code': 999,
        'time_elapsed': -1
    }
    return results

methods = tr.CSVOption('methods', 'inputs_int_test.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='ozila int tests',
        description="An evaluation script for various encodings of integers",
    )

    """
    parser.add_argument('-f', '--fortress',
                        required=True,
                        help='The path to the fortress jar file')
        parser.add_argument('-l', '--libs',
                        required=True,
                        help='The path to the folder containing the libraries to run fortress.')
    """
    source_mode = parser.add_mutually_exclusive_group(required=True)
    source_mode.add_argument('--dir', type=str,
                        help='Source is a directory containing .smt2 files for testing')
    source_mode.add_argument('--list', type=str,  # str because we need the filename to read in
                        help='Source is a list to read files from for testing. If not supplied, `dir` is searched recursively.')
    
    parser.add_argument('-t', '--timeout',
                        type=int, default=60,
                        help='Timeout for each problem in seconds')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default=f'test-{util.now_string()}.csv',
                        help='The file to write the csv file out to.')
    parser.add_argument('-v', '--verbose',
                        action='store_true')
    
    parser.add_argument('-i', '--iterations',
                        type=int, default=1,
                        help='The number of iterations to run each set of arguments'
                        )
    parser.add_argument('-s', '--skip',
                        type=int, default=0,
                        help='Number of values to skip')
    parser.add_argument('--force-header', action='store_true',
                        help='forces the header to be written to the output file')
    
    args = parser.parse_args()
    
    # Choose mode based on directory or list
    if args.dir is not None:
        test_file = tr.FilesOption('test_file',
                                args.dir,
                                recursive=True,
                                file_filter=util.valid_smt,
                                folder_filter=util.exclude(['combined', 'qf', 'partial', '.git']),
                                )
    elif args.list is not None:
        test_file = tr.FromFileOption('test_file', args.list)
    
    command = 'fortress --scope {scope_info} --transformers {transformers} --timeout {timeout} {test_file}'
    
        
    timeout = tr.Option('timeout', [args.timeout])
    scope_info = tr.Option('scope_info', [8])

    


    runner = tr.CSVTestRunner(command,
                              test_file, timeout, scope_info, methods,
                              timeout=args.timeout,
                              output_file=args.output,
                              result_fields=result_fields,
                              fields_from_result=result_values,
                              fields_from_timeout=timeout_values,
                              ignore_fields=['timeout', 'transformers'],
                              )
    if args.verbose:
        util.setup_logging_debug()
    else:
        util.setup_logging_default()
        
    runner.run(args.iterations, args.skip)
