"""
	A very simple example of how to use
	the testrunner class
"""

from testrunner.testrunner import *

# cmd should run with cross product of these three options

# an option named 'op' with one value 'echo'
op = Option('op', ['echo'])
# an option named 'number' with 5 numbers as its values
numbers = Option('number', list(range(5)))
# an option called 'text' with values read from each line of the file inputstrings.txt
text = FromFileOption('text', 'inputstrings.txt')

# look in test.csv and create a combo map option for the elements in the row
# first line is option labels
# there is a way to provide this info if it's not in the file
# e.g., if the column labels in test.csv are Name, Age
csv_opt = CSVOption('csv_opt', 'test.csv')

# template for string of command to run
command = '{op} {number} {text} something else {Name} -command {Age}'

# choose the logging level to be recorded in a default file name (log-date.txt)
setup_logging_debug()

#TestRunner takes a command, plus a unlimited list of options, and a timeout
# if opts is a lit of options, can do TestRunner(command, *opts, timeout=2000)
testRunner = TestRunner(command, op, numbers, text, csv_opt, timeout=2000)

# iterates commands on option values and spews unprocessed output to the screen
testRunner.run()
