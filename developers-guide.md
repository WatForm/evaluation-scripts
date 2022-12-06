# Developer's Guide

The simplest way to use these scripts is to use a `CSVTestRunner` class.
More specific outputs can be made by directly modifying the base `TestRunner` class.

## Commands
The Test Runner will repeatedly run a single command with values substituted from a variety of options.
For a simple example, let's say you want to run a script on a variety of files, with 3 levels of detail.
The command is written as a string with python format string formatting.
For example, `./test {file} --level {level}` can fill in values from options named `file` and `level`.

Commands can also be pre-separated lists of strings as for the `subprocess.run` function, but there is no real benefit to doing this, and it may cause issues, so it is not recommended.

## Options
Options are essentially just lists of values that can be filled into the command.
The `TestRunner` then composes the cross product of all its options' values and runs the command for each of them.
For ease of use, options with a single value are called "static options" while those with multiple values are "dynamic options".
Static options make it easier to configure the command, without cluttering the output.

Options can also provide a dictionary with strings representing option names and values being option values.
This allows you to synchronize options rather than making a cross product.
This can be seen in the `CSVOption` class.



## Using the `CSVTestRunner` Class
This class is designed to be the typical jumping off point

### Initializing
Use a [command](#commands) and [options](#options) as described above.

`output_file` is a file handle (opened for writing or appending) for you to write the csv data to.

`result_fields` are fields you will calculate after each run for recording.

`fields_from_timeout` and `fields_from_result` are functions that will do the calculation of the result_fields. They also allow you to overwrite input fields... but that's probably not a great idea.

`ignore_fields` Maybe you have options you don't want to record. Put them in this list to remove them

`write_header` If `True` a header will be written when you run the evaluation
