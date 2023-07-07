import shlex
import subprocess
import sys
import os

from time import monotonic as monotonic_timer
from time import time as time_timer

from testrunner import kill_child_processes
import util

DEBUG = False

TEST_FILE_NAME = 'test.als'
PORTUS_JAR = 'alloy_portus_final.jar'

model_file_path = sys.argv[1]
num_snapshots = int(sys.argv[2])
closure_transformer = sys.argv[3]
timeout = int(sys.argv[4])

test_file_path = os.path.join(os.path.dirname(model_file_path), TEST_FILE_NAME)

#=========================
# Alter scope in test file
#=========================
with open(model_file_path) as model_file, open(test_file_path, 'w') as test_file:
    for line in model_file:
        # Take for command apart
        if not line.startswith('for exactly '):
            test_file.write(line)
        else:
            # trim off the start
            data_start = line.find('DshSnapshot')
            trimmed_line = line[data_start:]
            fixed_line = "for exactly " + str(num_snapshots) + " " + trimmed_line
            test_file.write(fixed_line)

#=========================
# Call portus to translate
#=========================
# b automatically scales integers up for Liu et. al.'s method
portus_command = f'java -cp {PORTUS_JAR} ca.uwaterloo.watform.portus.cli.PortusCLI -smtlib-tc -b {test_file_path}'
# portus_command = f'java -cp alloy_portus_sorts.jar ca.uwaterloo.watform.portus.cli.PortusCLI -h'
portus_command = shlex.split(portus_command)

try:
    result = subprocess.run(portus_command, capture_output=True, text=True, timeout=timeout)

    if result.returncode != 0:
        print("portus error")
        if DEBUG:
            print(result.stdout)
            print('-------------------------')
            print(result.stderr)
            kill_child_processes()
            exit(1)
except subprocess.TimeoutExpired as timeout_error:
    print("portus error")
    kill_child_processes()
    exit(1)


# Get result path
OUTPUT_LINE_HEAD = 'Done. Output to '

smttc_path = ''
for line in result.stdout.splitlines():
    if OUTPUT_LINE_HEAD in line:
        smttc_path = line.split()[-1]
        smttc_path = smttc_path.strip()
        break
if smttc_path == '':
    print(result.stdout)
    print('---------------')
    print(result.stderr)
    exit(1)


# Make fortress load sorts with -i
#fortress_command = f'fortress -t {timeout} -T typecheck nnf {closure_transformer} oaf skolemize symmetrybreaking quantifierexpansion rangeformula simplify datatype  -i {smttc_path}'
fortress_command = f'fortress -t {timeout} -T typecheck enumelimination {closure_transformer} ceeijck oaf symmetry rangeformula simplify datatype -i {smttc_path}'

if DEBUG:
    print(f'{smttc_path=}')
    print(f'{fortress_command=}')


fortress_command = shlex.split(fortress_command)

try:
    start = monotonic_timer()
    result = subprocess.run(fortress_command, capture_output=True, text=True, timeout=timeout)
    end = monotonic_timer()
    
    time_elapsed = end - start
    if DEBUG:
        print(result.stdout)
        print('---------------')
        print(result.stderr)
    sat = util.satisfiability_of_output(result.stdout).value
    return_code = result.returncode
    results = ','.join(map(str, [return_code, sat, time_elapsed]))
    print(results)
    if DEBUG:
        print(results)
    exit(0)
except subprocess.TimeoutExpired as timeout_error:
    print('timeout')
    kill_child_processes()
    exit(2)
    
