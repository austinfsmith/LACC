## CheckMARCRecords.py
#
# This script uses the PyMARC library to determine the publication language
# and country of materials provisionally identified by the DetectLanguages
# script as being in a language of interest.
# Input is the output of the DetectLanguages script,
#  plus a directory containing MARC records for each item listed in it.
# Output will be a CSV with the same column headings as the input,
#  with additional "marc_language" and "marc_country" columns added.

import csv
import os
import pymarc

input_filename = 'lang_detect_output.csv'
output_filename = 'marc_record_output.csv'
marc_folder = 'MARC Records'


input_file =  open(input_filename, 'r')
request_reader = csv.DictReader(input_file)

output_rows = []

for request in request_reader:
    filename = marc_folder + os.sep + request['oclc_number']

    # Load the MARC record and extract the country & language codes
    marc_record = pymarc.parse_xml_to_array(filename)[0]
    country_code = marc_record.get_fields('008')[0].value()[15:17]
    language_code = marc_record.get_fields('008')[0].value()[35:38]

    # Add the country & language codes to the request data
    request['marc_language'] = language_code
    request['marc_country'] = country_code
    output_rows.append(request)

if output_rows:
    output_file = open(output_filename,'w',newline='')
    request_writer = csv.DictWriter(output_file, output_rows[0].keys())
    request_writer.writeheader()
    request_writer.writerows(output_rows)
else:
    print("No rows to output. Please check your filenames and language codes")

input_file.close()
output_file.close()
