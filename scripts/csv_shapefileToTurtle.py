# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:10:58 2018

@author: Joseph
"""

'''
reads a shapefile and converts it to Turtle RDF

This is originally for LGAs but can be adapted

The header should comprise a list of prefixes.
for example:
@prefix pn: <http://linked.data.gov.au/def/placenames#
refers to the Place Names ontology
pn:latitude refers to the latitude predicate

Then the rest of the table; a triple store of the attributes for each subject

'''
import unicodedata
import shapefile

#todays date
from datetime import date
today = str(date.today())

# function to write a python list to a csv file
def write_list_to_file(output, out_filename):
    """Write the list to csv file."""
    with open(out_filename, "w") as outfile:
        for entries in output:
            outfile.write(entries)
            outfile.write("\n")# add a return after each line


# read in the shapefile
myFile = r'\\xxxxxxxxx\LGA\LGA_2018.shp'
# read in the file
r = shapefile.Reader(myFile)

# get the attribute table records (combined with shapes)
shapeRecs = r.shapeRecords()
# firstShape = shapeRecs[0].shape

''' start building output '''
output = list() # python list container for the output

# put name of the file at the top of the turtle file
output.append('# from filename ' + myFile)
output.append('# ' + today)  # add the day the ttl was produced
output.append(' ')  # blank line

# add the prefix to the output (there could be several needed)
# ontology reference
output.append('@prefix lga: <http://madeupLGA.data.gov.au/def/LGAs#> .')
output.append(' ')  # blank line


''' work through attribute table one by one and build triples adding to output list as we go '''
index = 0
for feature in shapeRecs:  # for feature in attribute table
    print(feature.record)
    row = feature.record
    ''' build the output for each row  - most of the setup needs to be done just here below'''

    # triple store subject (= name plus year)
    year = str(row[8])
    index02 = str(row[1]) + '_' + str(row[8])

    # subj = row[2] + year #concatinate to make unigue
    # # clean subject for triple store use
    # subj = subj.replace(' ', '_')
    # subj = subj.replace('(', '')
    # subj = subj.replace(')', '_')
    # subj = subj.replace("'", '_')

    output.append('lga:' + str(index02) + '  ' + 'lga:LGA_code      ' + '"' + row[1] + '"' + ' .')
    output.append('lga:' + str(index02) + '  ' + 'lga:LGA_name      ' +  '"' + row[2] + '"' + ' .')
    output.append('lga:' + str(index02) + '  ' + 'lga:State         ' + '"' + row[4] + '"' + ' .')
    output.append('lga:' + str(index02) + '  ' + 'lga:year          ' + '"' + year + '"' + ' .')
    output.append('lga:' + str(index02) + '  ' + 'lga:area          ' + '"' + str(row[5]) + 'sqkm"' + ' .')

    output.append(' ')
    index += 1


# overwrites previous file unless you rename or move it
write_list_to_file(output, r'\\xxxx\lga02indexed02.ttl')



# for row in output:
#
#    print(row)

print ("finished")
    
    