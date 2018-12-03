# LACC
Latin American Collective Collection project scripts &amp; documentation

# Introduction

# Combined Holdings and Duplication Reports.py

## What does it do?
This script queries the OCLC API to retrieve lists of records for a given set of parameters.

The parameters include:
* Library (e.g. each member of a consortium)
* Country of Publication
* Library of Congress Class (top-level, e.g. P, F, M)

Additional parameters (e.g. publication year, format) may be used to limit the records queried.

The script uses these holdings list to determine the degree of duplication of materials within the specified parameters for the specified libraries.

## Pre-requisites
* Python 3.6+ : https://www.python.org/
* A WSKey for the WorldCat Search API : https://www.oclc.org/developer/develop/authentication/how-to-request-a-wskey.en.html
* Review the OCLC API Terms of Use : https://www.oclc.org/content/dam/developer-network/PDFs/wcapi-terms-and-conditions-20121204.pdf

## Using the Script
First, add your WSKey (see “Pre-requisites”).

Modify the countries, library_symbols, and lc_classes variables to reflect the parameters of your investigation. It’s advisable to keep these lists fairly focused (no more than twenty items per list). Longer lists of parameters will dramatically increase the execution time.

Modify the additional_parameters variable to limit the queries to specific formats, publication years, etc.

Once all parameters have been adjusted, run the script. The script will provide regular progress updates as it runs. Script execution time may be an hour or more - thousands of queries must be generated and executed - but as long as you don’t see any error messages displayed, you can assume that it’s still working.

## Handling Errors
This is a research script, not a finished software project. It does not have sophisticated error-handling routines. If an error is encountered, the script will display an error message and stop running.

There are a number of possible reasons that the script may fail to run to completion:

If the error prevents the script from starting (e.g. you don’t see the “Running Combined Holdings and Duplication Report”), there is a problem with the formatting of your parameters or WSkey. Double-check these, making sure that you’re following the instructions given in the comments.

If the error occurs while the script is querying holdings, the most likely culprit is that the OCLC servers have timed out while executing queries, or that it was interrupted by your computer going to sleep or logging out. You can generally just re-run the script; it will pick up where it left off.

If an error occurs repeatedly at the same point in the script, or occurs while calculating duplication of holdings, send a copy of your modified script, along with the error message you received, to Austin Smith (afsmith at umd dot edu).
