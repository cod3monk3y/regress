@SETLOCAL

REM Run a coarse search through the commit history, looking for the most recent success of the regression.
REM Skip every 10 to search more quickly, since it appears (empirically) that this has been broken for a while.
SET KNOWN_FAILURE=126a16a0
python regress.py --commit %KNOWN_FAILURE% -n 10 --skip 10 --repo repos/invoke --command tests\invoke_chain.bat --stop-on-pass

REM Once the first pass was found, back up and scan for the exact commit that succeeds, one commit at a time.
SET KNOWN_FAILURE=75c4d5eb68c9
python regress.py --commit %KNOWN_FAILURE% -n 10 --repo repos/invoke --command tests\invoke_chain.bat --stop-on-pass

REM At this point, 75c4d5eb68c9 fails, and the commit immediately before (96771fd879a7) passes. So
REM 75c4d5eb68c9 (2018-07-08) is the culprit.