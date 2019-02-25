# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:10:58 2018

@author: Joseph
"""

'''
reads a shapefile and converts it to Turtle RDF

It reads from the shapefile attribute table.

ACT DGGS to turtlefile
including SA1 SA2 SA3 DEM LGA

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
myFile = r'\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\ACT_grid\MultiData_DGGS.shp'
# read in the file
r = shapefile.Reader(myFile)

# get the attribute table records (combined with shapes)
shapeRecs = r.shapeRecords()
# firstShape = shapeRecs[0].shape

''' start building output '''
output = list() # python list container for the output

# put name of the file at the top of the turtle file
output.append('# from filename ' + myFile)
output.append('# processed by csv_shapefileToTurtle.py')
output.append('# ' + today)  # add the day the ttl was produced
output.append(' ')  # blank line

# add the prefix to the output (there could be several needed)
# ontology reference
output.append('@prefix dggs: <http://ACT_dggs.data.gov.au/def/LGAs#> .')
output.append(' ')  # blank line


''' work through attribute table one by one and build triples adding to output list as we go '''

for feature in shapeRecs:  # for feature in attribute table
    print(feature.record)
    row = feature.record
    ''' build the output for each row  - most of the setup needs to be done just here below'''

    # subj = row[2] + year #concatinate to make unigue
    # # clean subject for triple store use
    # subj = subj.replace(' ', '_')
    # subj = subj.replace('(', '')
    # subj = subj.replace(')', '_')
    # subj = subj.replace("'", '_')
    dem = str(round(row[3], 2))
    output.append('dggs:' + row[2] + '  ' + 'dggs:hasDGGScode      ' + '"' + row[2] + '"' + ' .')
    output.append('dggs:' + row[2] + '  ' + 'dggs:hasDEM           ' +  '"' + dem + '"' + ' .')
    output.append('dggs:' + row[2] + '  ' + 'dggs:hasSA1code       ' + '"' + row[4] + '"' + ' .')
    output.append('dggs:' + row[2] + '  ' + 'dggs:hasSA2code       ' + '"' + row[5] + '"' + ' .')
    output.append('dggs:' + row[2] + '  ' + 'dggs:hasSA2name       ' + '"' + row[6] +  ' .')

    output.append(' ')



# overwrites previous file unless you rename or move it
write_list_to_file(output, r'\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\data\MultiDataDGGS_ACT.ttl')



# for row in output:
#
#    print(row)

print ("finished")
    
    