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

f = r'\\xxxxxxxxx\PlacesToRDF_fromQuery.csv'
output = list()

# name of the file at the top
output.append('# filename ' + f)
output.append(' ' )

# add the prefix to the output (there could be several needed)
output.append('@prefix pn: <http://linked.data.gov.au/def/placenames#> .')
output.append(' ' )

import csv
import unicodedata


# function to write a list to a csv file
# requires the list and the filename to save it too	
def write_list_to_file(myList, filename):
    """Write the list to csv file."""

    with open(filename, "w") as outfile:
        for entries in myList:
            outfile.write(entries)
			# add a return after each line
            outfile.write("\n")
            
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def convert_to_normal(s):
    return unicodedata.normalize('NFKD', s).encode('ascii','ignore')
    


# check everthing is ASCCI
## open the data file 
#with open(f) as csvDataFile:
#    csvReader = csv.reader(csvDataFile)
#
#    next(csvReader)  # skip the header
#    for row in csvReader:
#         # remove any " from the name string
#        row[1]=row[1].replace('"', '')
#
#        #check for characters of another language
#        if not is_ascii(row[1]):
#            print ('Not_ASCCI', row[0], row[1])



# open the data file 
with open(f) as csvDataFile:
    csvReader = csv.reader(csvDataFile)

    next(csvReader)  # skip the header
    for row in csvReader:
         # remove any " from the name string
        row[1]=row[1].replace('"', '')

        # #check for characters of another language
        # if not is_ascii(row[1]):
        #
        #     row[1] = convert_to_normal(row[1])
        #     # if not ascii assume some French characters = @fr
        #     output.append('pn:' + row[0] + '  ' + 'pn:hasPlaceName              "' + row[1] +'"@fr .')
        #
        # else:
        #     output.append('pn:' + row[0] + '  ' + 'pn:hasPlaceName              "' + row[1] +'" .')
        #
   
        
        output.append('pn:' + row[0] + '  ' + 'pn:hasPlaceName              "' + row[1] +'" .')
        # amend to suit classification list
        #row[2] = row[2].replace('Airfields', 'Airfield')
        output.append('pn:' + row[0] + '  ' + 'pn:FeatureClassification     "' + row[2] +'" .')  
        output.append('pn:' + row[0] + '  ' + 'pn:latitude                  "' + row[3] +'" .')  
        output.append('pn:' + row[0] + '  ' + 'pn:longitude                 "' + row[4] +'" .') 
        output.append('pn:' + row[0] + '  ' + 'pn:State                     "' + row[5] +'" .')
         
            
        output.append(' ')    
        



# Build the ttl
# write the file
#filename = 
# overwrites previous file unless you rename or move it
write_list_to_file(output, r"\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\Workspace\Joseph\PlaceNamesTest.ttl")


#
#for row in output:
#
#    print(row)
#    
print ("finished")
    
    