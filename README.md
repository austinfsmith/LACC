# Latin American Collective Collection Project

1. [Introduction](#Introduction)
2. [Holdings Reports](#Combined-Holdings-and-Duplication-Reports)
3. [ILL Reports](#ILL-Reports)

# Introduction

This repository contains scripts and templates created for a project undertaken by Lisa Gardinier, Manuel Ostos, Austin Smith, and Hilary Thompson in 2017-2018.

The purpose of the study was to better understand the Big Ten Academic Alliance's resource sharing needs for Spanish and Portuguese materials published in Latin America and to develop data-informed models for cooperative collection development of these publications. The authors employed multiple technologies to expedite gathering,  reconciling,  and  analyzing  data  from  different  sources,  making  this  project  an  excellent  case study for consortial data analysis. The scripts presented here can be modified to apply the methodology to other consortia, regions, and subject areas.

This project was presented at the IASC21 conference. Slides are available at http://hdl.handle.net/1903/21469 .

# Combined Holdings and Duplication Reports

[Script is available in this repository](https://github.com/austinfsmith/LACC/tree/master/Python%20Scripts)

## What does it do?
This script queries the OCLC API to retrieve lists of records for a given set of parameters.

The parameters include:
* Library (e.g. each member of a consortium)
* Country of Publication
* Library of Congress Class (top-level, e.g. P, F, M)

Additional parameters (e.g. publication year, format) may be used to limit the records queried.

The script uses these holdings lists to determine the degree of duplication of materials within the specified parameters for the specified libraries.

## Prerequisites
* Python 3.6+ : https://www.python.org/
* A WSKey for the WorldCat Search API : https://www.oclc.org/developer/develop/authentication/how-to-request-a-wskey.en.html
* Review the OCLC API Terms of Use : https://www.oclc.org/content/dam/developer-network/PDFs/wcapi-terms-and-conditions-20121204.pdf

## Using the Script
First, add your WSKey (see “Prerequisites”).

Modify the countries, library_symbols, and lc_classes variables to reflect the parameters of your investigation. It’s advisable to keep these lists fairly focused (no more than twenty items per list). Longer lists of parameters will dramatically increase the execution time.

Modify the additional_parameters variable to limit the queries to specific formats, publication years, etc.

Once all parameters have been adjusted, run the script. The script will provide regular progress updates as it runs. Script execution time may be an hour or more - thousands of queries must be generated and executed - but as long as you don’t see any error messages displayed, you can assume that it’s still working.

## Handling Errors
This is a research script, not a finished software project. It does not have sophisticated error-handling routines. If an error is encountered, the script will display an error message and stop running.

There are a number of possible reasons that the script may fail to run to completion:

If the error prevents the script from starting (e.g. you don’t see the “Running Combined Holdings and Duplication Report” message in the Python console), there is a problem with the formatting of your parameters or WSkey. Double-check these, making sure that you’re following the instructions given in the comments.

If the error occurs while the script is querying holdings, the most likely culprit is that the OCLC servers have timed out while executing queries, or that it was interrupted by your computer going to sleep or logging out. You can generally just re-run the script; it will pick up where it left off.

If an error occurs repeatedly at the same point in the script, or occurs while calculating duplication of holdings, send a copy of your modified script, along with the error message you received, to Austin Smith (afsmith@umd).

## Using the Output

### Duplication Reports

One of these reports will be generated for each country included in the script's parameters. Each report contains overall holdings, unique holdings, and degree of duplication for each library and LoC class included in the script's parameters.

### Combined Holdings Report

"Combined Holdings Report.csv" contains a detailed listing of holdings & duplication which can be used as input for several different visualizations. Examples can be found at http://go.umd.edu/IASC21 and http://go.umd.edu/IASC21x . The "Excel Spreadsheets" and "D3 Visualization" filders in this repository contain some templates you can use to generate your own visualizations, using the output of your modified custom holdings report.

If you have any difficulty getting these to work, contact Austin Smith (afsmith@umd)

#### Importing Holdings Data into Excel Spreadsheets

[Templates are available in this repository](https://github.com/austinfsmith/LACC/tree/master/Excel%20Templates)

Examples presented at the IASC21 conference are available at https://go.umd.edu/IASC21x

1. Open “Combined Holdings Report.csv”, and the Excel template file you would like to use (e.g. “Holdings by Country Template.xlsx”).
2. Select all cells in the Combined Holdings Report, and copy them.
3. Select all cells in the Data worksheet of the template file, and paste over them.
4. On the Table worksheet of the template file, right-click anywhere in the pivot table and click “Refresh”.
5. Change the title of the chart on the Chart worksheet, if desired. Save the file under a new filename which reflects its contents.

#### Importing Holdings Data into Interactive Visualizations

[Pages and scripts are available in this repository](https://github.com/austinfsmith/LACC/tree/master/D3%20Visualization)

Examples presented at the IASC21 conference are available at https://go.umd.edu/IASC21

Javascript visualizations must be hosted on a server, as your browser likely will not execute javascript on a local machine.

1. Copy the “D3 Visualization” folder to your web server.
2. Save the output from the Combined Holdings & Duplication script (“Combined Holdings Report.csv” to the \D3 Visualization\data\ . If you change the name of this file, you'll need to change the value of the input_file variable on line 7 of D3InteractiveChart.js.
3. Pointing your browser to D3InteractiveChart.html should now render the interactive chart.

# ILL Reports

## Prerequisites

* Python 3.6+ : https://www.python.org/
* The langdetect library : https://pypi.org/project/langdetect/
* The pymarc library : https://github.com/edsu/pymarc

## Description

Much of the code written for the ILL data analysis portion of the LACC study dealt with parsing or mitigating the idiosyncracies of the data available to the investigators. As this code is neither portable nor easily read, we are sharing two example scripts to demonstrate the tools used for ILL data analysis. A small data set is also included as a demonstration.

The DetectLanguages script accepts as input a CSV file containing a list of requests exported from ILLiad, or another ILL system, and outputs a modified version of the same list, filtered to exclude any requests which appear to be in languages outside of the scope of interest.

The CheckMARCRecords script accepts as input the output of the DetectLanguages script, as well as MARC records for the items listed in that output. It inspects the MARC records to identify the actual country and language of publication, and outputs a report containing this information.

## Using the Output

The output of the CheckMARCRecords script can be used as a starting point for the analysis of ILL requests for materials published in a specific country or language. The analysis and visualizations produced during the course of the LACC study were created from this output with a set of tools including MS Excel and Access, D3.js, and additional Python scripts.
