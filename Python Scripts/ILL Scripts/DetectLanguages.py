## DetectLanguages.py
#
# This script uses the langdetect library to attempt to identify ILL requests
# for materials in a specific language or set of languages.
# Input must be a CSV file. Required columns are:
#   title
#   oclc_number
# Output will contain the same columns as input, in the same order,
#  with an additional 'detected_language' column added.
#

import csv
import langdetect

# Input file must be in CSV format, with labeled columns.
input_filename = 'test_input.csv'
output_filename = 'lang_detect_output.csv'

# List of ISO 639-1 language codes.
# Only requests whose titles appear to be in these languages will be kept;
#  other languages will be ignored.
language_codes = ['es','pt']

input_file =  open(input_filename, 'r')
request_reader = csv.DictReader(input_file)
output_rows = []

for request in request_reader:
    detected_language = langdetect.detect(request['title'])
    if detected_language in language_codes:
        request['detected_language'] = detected_language
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
