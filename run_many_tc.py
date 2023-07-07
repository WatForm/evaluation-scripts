import argparse
import subprocess
import shlex
import os
import sys

from typing import *

from tqdm.auto import tqdm

import util
from tcinfo import CLOSURE_ELIMINATION_METHODS


parser = argparse.ArgumentParser()

parser.add_argument('--files', nargs='+')
parser.add_argument('-n', '--num-snapshots', nargs="+", type=int)
parser.add_argument('-t', '--timeout', required=True, type=int, help='timeout in seconds')
parser.add_argument('-o', '--output', default=f'test-{util.now_string()}.csv')
parser.add_argument('-i', '--iterations',
                        type=int, default=1,
                        help='The number of iterations to run each set of arguments'
                        )
parser.add_argument('-m', '--methods', nargs='+', default=CLOSURE_ELIMINATION_METHODS, type=str, help='closure elimination methods')


args = parser.parse_args()

with open(args.output, 'w') as outfile:
    #outfile = sys.stdout
    print('file,method,snapshots,returncode,sat,time_elapsed', file=outfile)

    for method in tqdm(args.methods, 'method', len(args.methods), dynamic_ncols=True, position=0):
        for test_file in tqdm(args.files, 'file', len(args.files), dynamic_ncols=True, leave=False, position=1):
            has_timed_out = False
            for current_num_snapshots in tqdm(args.num_snapshots, 'scope options', len(args.num_snapshots), dynamic_ncols=True, leave=False, position=2):
                for _ in tqdm(range(args.iterations), 'iterations', total=args.iterations, dynamic_ncols=True, leave=False, position=3):
                    if not has_timed_out:
                        command = shlex.split(
                            f'python3 run_one_tc.py {test_file} {current_num_snapshots} {method} {args.timeout}'
                        )
                        result = subprocess.run(command, capture_output=True, text=True, timeout=2*args.timeout)
                    
                    if has_timed_out or 'timeout' in result.stdout:
                        has_timed_out = True
                        result_line = f'{test_file},{method},{current_num_snapshots},2,UNSURE,-1'
                    elif 'portus error' in result.stdout or result.returncode != 0:
                        print(result.stderr)
                        result_line = f'{test_file},{method},{current_num_snapshots},1,UNSURE,-1'
                    else:
                        result_line = f'{test_file},{method},{current_num_snapshots},' + result.stdout.strip()
                    
                    print(result_line, file=outfile)
                    outfile.flush()

print("Done!")