import csv
import os
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET

### DO NOT CHANGE ANYTHING ABOVE THIS LINE #####################################

# WS key - obtain one from OCLC and paste it here. Be sure to single-quote it.
wsKey = 'add your wskey here'

# Country codes and names to include in queries.
# Observe the formatting: 'code':'name',
# For full list of codes, see https://www.loc.gov/marc/countries/countries_code.html
countries = {
'ag':'Argentina',
'bo':'Bolivia',
'bl':'Brazil',
'cl':'Chile',
'ck':'Colombia',
'cr':'Costa Rica',
'cu':'Cuba',
'dr':'Dominican Republic',
'ec':'Ecuador',
'es':'El Salvador',
'gt':'Guatemala',
'ho':'Honduras',
'mx':'Mexico',
'nq':'Nicaragua',
'pn':'Panama',
'py':'Paraguay',
'pe':'Peru',
'pr':'Puerto Rico',
'uy':'Uruguay',
've':'Venezuela'
}

# Library names and symbols.
# Multiple symbols for the same library (or university) will be grouped together in the results.
# Observe the formatting: 'name':['symbol1','symbol2'],
# Consult the OCLC Policies Directory, or your local ILL department, for symbols.
# OCLC Policies Directory: https://illpolicies.oclc.org/
library_symbols = {
'Indiana':['IUL'],
'Michigan':['EEM'],
'Northwestern':['INU'],
'Ohio':['OSU'],
'Penn State':['UPM'],
'Purdue':['IPL'],
'Rutgers':['NJR'],
'Chicago':['CGU'],
'Illinois':['UIU'],
'Iowa':['NUI'],
'Maryland':['UMC'],
'Michigan State':['EYM'],
'Minnesota':['MNU'],
'Nebraska':['LDL'],
'Wisconsin':['GZM']
}

# List of the LoC Classes to query.
# Observe the formatting: Single-quoted, comma-separated, and enclosed by brackets.
# Single-letter, top-level holdings only -
#   anything else will be stripped from the list prior to execution.
lc_classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'Z']

# Any additional search parameters should be added here.
# Must be single-quoted and comma-separated, as shown.
# list of acceptable parameters at:
# https://www.oclc.org/developer/develop/web-services/worldcat-search-api/bibliographic-resource.en.html
additional_parameters = ['srw.dt="bks"', 'srw.yr=2006-2016']

### DO NOT CHANGE ANYTHING BELOW THIS LINE #####################################

base_url = 'http://worldcat.org/webservices/catalog/search/worldcat/opensearch?q='

query_final_clause = '&count=100&servicelevel=full&wskey=' + wsKey

country_codes = list(countries.keys())
library_names = list(library_symbols.keys())
lc_class_parameters = {
                        'A':['a1','a2','a3','a4','a5','a6','a7','a8','a9','ac','ae','ag','ai','am','an','ap','as','ay','az'],
                        'B':['b1','b2','b3','b4','b5','b6','b7','b8','b9','bc','bd','bf','bh','bj','bl','bm','bp','bq','br','bs','bt','bv','bx'],
                        'C':['c1','c2','c3','c4','c5','c6','c7','c8','c9','cb','cc','cd','ce','cj','cn','cr','cs','ct'],
                        'D':['d1','d2','d3','d4','d5','d6','d7','d8','d9','da','daw','db','dc','dd','de','df','dg','dh','dj','djk','dk','dl','dp','dq','dr','ds','dt','du','dx'],
                        'E':['e1','e2','e3','e4','e5','e6','e7','e8','e9'],
                        'F':['f1','f2','f3','f4','f5','f6','f7','f8','f9'],
                        'G':['g1','g2','g3','g4','g5','g6','g7','g8','g9','ga','gb','gc','ge','gf','gn','gr','gt','gv'],
                        'H':['h1','h2','h3','h4','h5','h6','h7','h8','h9','ha','hb','hc','hd','he','hf','hg','hj','hm','hn','hq','hs','ht','hv','hx'],
                        'J':['j1','j2','j3','j4','j5','j6','j7','j8','j9','ja','jc','jf','jj','jk','jl','jn','jq','js','jv','jx','jz'],
                        'K':['k1','k2','k3','k4','k5','k6','k7','k8','k9','kb','kbm','kbp','kbr','kbs','kbt','kbu','kd','kdk','kdz','ke','kf','kg','kh','ku','kuq','kz'],
                        'L':['l1','l2','l3','l4','l5','l6','l7','l8','l9','la','lb','lc','ld','le','lf','lg','lh','lj','lt'],
                        'M':['m1','m2','m3','m4','m5','m6','m7','m8','m9','ml','mt'],
                        'N':['n1','n2','n3','n4','n5','n6','n7','n8','n9','na','nb','nc','nd','ne','nk','nx'],
                        'P':['p1','p2','p3','p4','p5','p6','p7','p8','p9','pa','ph','pc','pd','pe','pf','pg','ph','pj','pk','pl','pm','pn','pq','pr','ps','pt','pz'],
                        'Q':['q1','q2','q3','q4','q5','q6','q7','q8','q9','qa','qb','qc','qd','qe','qh','qk','ql','qm','qp','qr'],
                        'R':['r1','r2','r3','r4','r5','r6','r7','r8','r9','ra','rb','rc','rd','re','rf','rg','rj','rk','rl','rm','rs','rt','rv','rx','rz'],
                        'S':['s1','s2','s3','s4','s5','s6','s7','s8','s9','sb','sd','sf','sh','sk'],
                        'T':['t1','t2','t3','t4','t5','t6','t7','t8','t9','ta','tc','td','te','tf','tg','th','tj','tk','tl','tn','tp','tr','ts','tt','tx'],
                        'U':['u1','u2','u3','u4','u5','u6','u7','u8','u9','ua','ub','uc','ud','ue','uf','ug','uh'],
                        'V':['v1','v2','v3','v4','v5','v6','v7','v8','v9','va','vb','vc','vd','ve','vf','vg','vk','vm'],
                        'Z':['z1','z2','z3','z4','z5','z6','z7','z8','z9','za']
}

# Make sure we don't try to query nonexistent LC classes!
lc_classes = [lc_class for lc_class in lc_classes if lc_class in lc_class_parameters.keys()]

holdings_data_directory = "Holdings Data"
duplication_report_directory = "Duplication Reports"

# Retrieve a list of holdings for the set of parameters provided.
# Also returns the number of queries executed, for tracking.
def query_holdings(country_code, oclc_symbol, lc_class):
    # Construct the query from the parameters    
    cp = 'srw.cp=' + country_code
    li = 'srw.li=' + oclc_symbol
    lc = '(srw.lc=' + '*+or+srw.lc='.join(lc_class_parameters[lc_class]) + '*)'
    args = cp, li, lc, *additional_parameters
    
    query = base_url + '+and+'.join(filter(None,args)) + query_final_clause
    
    oclc_numbers = set()
    query_count = 0
    while query:

        # Execute the query.
        response = urllib.request.urlopen(query)
        root = ET.fromstring(response.read())

        query_count += 1
        for item in root:
            if item.tag == '{http://www.w3.org/2005/Atom}entry':
                for field in item:
                    if field.tag == "{http://purl.org/oclc/terms/}recordIdentifier":
                        oclc_numbers.add(field.text)
        query = None
        for item in root:
            if (item.tag == '{http://www.w3.org/2005/Atom}link') and (item.attrib['rel'] == 'next'):
                query = item.attrib['href'] + '&servicelevel=full'

    return oclc_numbers, query_count

# Download lists of OCLC numbers for each combination of parameters.
# Writes lists to files as follows:
#   filename = CountryCode_LibraryName_LCClass
#   contents = one OCLC number per line
# Returns the number of queries executed & the number of files written.
def compile_holdings():

    try:
        if not os.path.exists(holdings_data_directory):
            os.makedirs(holdings_data_directory)
        if not os.path.exists(duplication_report_directory):
            os.makedirs(duplication_report_directory)
       
    except OSError:
        print('Unable to create holdings directory.')
        print('Either your hard drive is full, or you do not have write permissions on this disk')
        sys.exit()

    query_counter, file_counter = 0, 0

    for country_code in country_codes:
        print('Querying holdings for ' + countries[country_code]+':\n\t',end='')
        for lc_class in lc_classes:
            print(lc_class+' ',end='')
            for library_name in library_names:


                # If we already have data for this set of parameters, continue.
                filename = holdings_data_directory + os.sep + '_'.join([country_code,library_name,lc_class])
                if os.path.isfile(filename):
                    continue

                # Get holdings for each symbol for this library.
                oclc_numbers = set()
                for oclc_symbol in library_symbols[library_name]:
                    symbol_holdings, queries = query_holdings(country_code, oclc_symbol, lc_class)
                    query_counter += queries
                    oclc_numbers.update(symbol_holdings)

                # Write data for this set of parameters.
                with open(filename, 'w') as outfile:
                    for oclc_number in oclc_numbers:
                        outfile.write(oclc_number+'\n')
                file_counter += 1
        print('')
    return query_counter, file_counter

# Loads lists of holdings from the text files generated by compile_holdings().
# Returns a data structure containing holdings information in the format:
#   holdings_data[country][lc_class][library]
def load_holdings_data():
    # Create data structure
    holdings_data = { country_code:
                     { lc_class:
                       { library_name : [] for library_name in library_names }
                       for lc_class in lc_classes }
                    for country_code in country_codes }

    # Load data from each file
    for country_code in country_codes:
        for lc_class in lc_classes:
            for library_name in library_names:
                filename = holdings_data_directory + os.sep + '_'.join([country_code,library_name,lc_class])
                with open(filename) as f:
                    holdings_data[country_code][lc_class][library_name] = f.read().splitlines()
    return holdings_data    

# Calculated degrees of duplication from holdings data.
# Returns a data structure containing duplication data in the format:
#   duplication_data[country][lc_class][library][held by 1,2,3...]
def calculate_duplication(holdings_data):
    duplication_data = { country_code:
                     { lc_class:
                       { library_name : [0]*len(library_names) for library_name in library_names }
                       for lc_class in lc_classes }
                    for country_code in country_codes }

    for country_code in country_codes:
        for library_name in library_names:
            for lc_class in lc_classes:
                for oclc_number in holdings_data[country_code][lc_class][library_name]:
                    count = 0
                    for holdings_lib in library_names:
                        if oclc_number in holdings_data[country_code][lc_class][holdings_lib]:
                            count += 1
                    duplication_data[country_code][lc_class][library_name][count-1] += 1
    return duplication_data
                    
def generate_combined_holdings_report(duplication_data):
    heading = ['Country','Library','LC Class'] + ['Held by '+str(x) for x in range(1, len(library_names)+1)]
    output_rows = [heading]
    for country_code in country_codes:
        for library_name in library_names:
            for lc_class in lc_classes:
                new_row = [countries[country_code], library_name, lc_class] + [duplication_data[country_code][lc_class][library_name][x] for x in range(0, len(library_names))]
                output_rows.append(new_row)
    with open('Combined Holdings Report.csv','w',encoding='utf-8',newline='') as output_file:
        cwriter = csv.writer(output_file, delimiter=',', quotechar='"')
        cwriter.writerows(output_rows)

def generate_duplication_reports(duplication_data):
    for country_code in country_codes:
        report_rows = []
        
        # Overall Holdings
        heading = ['Overall','Total'] + lc_classes
        report_rows.append(heading)
        for library_name in library_names:
            new_row = [library_name,0]
            total = 0
            for lc_class in lc_classes:
                count = len(holdings_data[country_code][lc_class][library_name])
                total += count
                new_row.append(count)
            new_row[1] = total
            report_rows.append(new_row)
        report_rows.append([])

        # Unique Holdings
        heading = ['Unique','Total'] + lc_classes
        report_rows.append(heading)
        for library_name in library_names:
            new_row = [library_name,0]
            total = 0
            for lc_class in lc_classes:
                count = duplication_data[country_code][lc_class][library_name][0]
                total += count
                new_row.append(count)
            new_row[1] = total
            report_rows.append(new_row)
        report_rows.append([])

        # Duplication
        heading = ["Duplication","All"] + lc_classes
        report_rows.append(heading)
        new_row = ["Held by Any:",0]
        total = 0
        for lc_class in lc_classes:
            class_total_holdings = set()
            for library_name in library_names:
                class_total_holdings.update(set(holdings_data[country_code][lc_class][library_name]))
            total += len(class_total_holdings)
            new_row.append(len(class_total_holdings))
        new_row[1] = total
        report_rows.append(new_row)

        for held_by in range(1,len(library_names)+1):
            new_row = ["Held by " + str(held_by) + ":",0]
            total = 0
            for lc_class in lc_classes:
                class_held_by = 0
                for library_name in library_names:
                    class_held_by += duplication_data[country_code][lc_class][library_name][held_by-1]
                total += int( round( class_held_by / held_by ))
                new_row.append( int( round( class_held_by / held_by )))
            new_row[1] = total
            report_rows.append(new_row)

        filename = duplication_report_directory + os.sep + countries[country_code] + ' Duplication Report.csv'
        with open(filename,'w',encoding='utf-8',newline='') as output_file:
            cwriter = csv.writer(output_file, delimiter=',', quotechar='"')
            cwriter.writerows(report_rows)

### MAIN #######################################################################
print('Running Combined Holdings and Duplication Report.')

try:
    query_counter, file_counter = compile_holdings()
    print('{} queries executed, {} files written.'.format(query_counter, file_counter))
except KeyboardInterrupt:
    print('Execution halted by user.')
    sys.exit()
except Exception as e:
    print('\n An error occurred while retrieving holdings information: ', str(sys.exc_info()[0]))
    print('\n You may wish to try running the script again.')
    print('If the error recurs, please send this message and a copy of the script to afsmith@umd.edu')
    sys.exit()

try:
    print('\nCalculating Duplication of Holdings')                        
    holdings_data = load_holdings_data()
    duplication_data = calculate_duplication(holdings_data)

    generate_combined_holdings_report(duplication_data)
    print('Combined Holdings Report generated.')

    generate_duplication_reports(duplication_data)
    print('Duplication Reports generated.')

except Exception as e:
    print('\n An error occurred while compiling duplication data: ', str(sys.exc_info()[0]))
    print('\n You may wish to try running the script again.')
    print('If the error recurs, please send this message and a copy of the script to afsmith@umd.edu')
    sys.exit()

print('Reports generated. Deleting holdings lists...')
if os.path.isdir(holdings_data_directory):
    shutil.rmtree(holdings_data_directory)
print('Finished.')


