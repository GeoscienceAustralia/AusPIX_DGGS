# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:10:58 2018

@author: Joseph Bell Geoscience Australia
"""

'''
reads a csv file and converts it to Turtle RDF

This is originally for placeNames but can be adapted

The header should comprise a list of prefixes.
for example:
@prefix pn: <http://linked.data.gov.au/def/placenames#
refers to the Place Names ontology
pn:latitude refers to the latitude predicate

Then the rest of the table; a triple store of the attributes for each subject

'''

f = r'\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\ACT_grid\RiverGauge\Riverlea1960_2018.csv'
output = list()

# name of the file at the top
output.append('# filename ' + f)
output.append(' ' )

# add the prefix to the output (there could be several needed)
output.append('PREFIX rg: <http://linked.data.gov.au/def/riverData#> .')
output.append('#processed by: csvToTurtle.py')
output.append('#subject is indexed by river gauge number and date')
output.append(' ')

import csv

# function to write a list to a csv file
# requires the list and the filename to save it too	
def write_list_to_file(myList, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in myList:
            outfile.write(entries)
			# add a return after each line
            outfile.write("\n")
            
count = 0


# open the data file only to read header data
with open(f) as csvDataFile:
    # read in the header data
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if '#' in row[0]:
            # grab the header information
            if "Long Name" in row[0]:
                name = row[1]

            elif "Station Number" in row[0]:
                number = row[1]

            elif "Latitude" in row[0]:
                lat = row[1]

            elif "Long" in row[0]:
                long = row[1]

            elif "OWNER" in row[0]:
                owner = row[1]

# open the data file again
with open(f) as csvDataFile:
    # now process the data
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if '#' not in row[0]:
            # readDate
            thisDate = row[0][:-19]
            thisIndex = number + '_' + thisDate
            output.append('rg:' + thisIndex + '  ' + 'rg:hasname       "' + name + '" .')
            output.append('rg:' + thisIndex + '  ' + 'rg:hasnumber     "' + number + '" .')
            output.append('rg:' + thisIndex + '  ' + 'rg:haslat        "' + lat + '" .')
            output.append('rg:' + thisIndex + '  ' + 'rg:haslong       "' + long + '" .')
            output.append('rg:' + thisIndex + '  ' + 'rg:hasowner      "' + owner + '" .')
            output.append('rg:' + thisIndex + '  ' + 'rg:hasDate       "' + row[0][:-19] + '" .')  # removed time zone of date
            output.append('rg:' + thisIndex + '  ' + 'rg:hasRiverLevel "' + row[1] + '" .')

            output.append(' ') # space


            count += 1

# Build the ttl
# write the file
#filename = 
# overwrites previous file unless you rename or move it
write_list_to_file(output, r"\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\Workspace\Joseph\RiverGauge.ttl")


#
#for row in output:
#
#    print(row)
#    
print ("finished")
    
    