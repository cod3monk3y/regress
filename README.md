# Py/Invoke Regression Test and Search

## Setup

1. Clone py-invoke into `repos/invoke`.
1. Install python 3.8

> This script was written to work on Windows, and will need to be modified slightly to work on Linux/OSX.
>
> It also assumes Python 3.8, so may need changes to work with 3.7 and earlier.

## Regression Overview
This regression generates 26 tasks and attempts to invoke them with

    invoke a b c d ... z`

This scenario exacerbates the `invoke` error. In order to detect that the `invoke` command has succeeded, each command logs its name (e.g. 'a') to an output file. For this test to succed, the *last* line in the file should be 'z'.

The test outputs the last line from the file for each run, and a pass '.' or fail 'F' flag. When failing, the output will look like:

    [0] c F
    [1] d F
    [2] q F
    [3] b F
    [4] l F
    Failures: 5/5

When passing, all iterations will end with 'z' and have the pass flag '.'. 

    [0] z .
    [1] z .
    [2] z .
    [3] z .
    [4] z .
    Failures: 0/5
    
## Running the regression test for Invoke

To run the scan in two parts using pre-discovered commits, use the batch file:

    run_regression.bat
    
To run the invoke-chain regression against the currently checked out commit:

    python tests\test_invoke_chain.py
    
## Running generic regression searches (like bisect)

If a test is failing at the most recent commit, and you want to know when it last worked, run the `regress` script
 with `--stop-on-pass`. You can speed up the search by skipping commits, with `--skip N`:

    python regress.py --commit HEAD -n 100 --repo repos/invoke --command test\REGRESSION_TEST.py --skip 10 --stop-on-pass

Once you have a last-known-good (LKG) and a previous failure (PRV), search one at a time between them and stop as soon 
as the test passes. Then, the culprit will be the commit immediately *after* the PASS.

    python regress.py --commit PRV -n 100 --repo repos/invoke --command test\REGRESSION_TEST.py --stop-on-pass

