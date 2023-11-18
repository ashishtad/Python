Program to create an HTML diff of  log files.
Motivation:
Working as software developer I need to deal with log files almost everyday.
Sometimes i need to see the diff of files to check the flow between a passing case log and a failure log.
A major usecase to use this is when we have few testcases where for each test case we have two log files :
    - Baseline log file : Which is generated from a baseline build/image
    - Modified log file : Which is generated with a cutom build/image [ having code changes].
In this case after the whole test suite is run,
instead of comparing manually the baseline code flow with the changed one, we can run this script which will generate diff file of baseline and modified log file for each of the test cases.
This is the reason this program is created which basically creates a html diff of two log files.

Folder Structure:

1. LogDiffCreate.py : Program source code
2. LogFiles         : Contains the input log files
3. config.json      : config file in which the input log files and the output diff file needs to be mentioned