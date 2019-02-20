# -*- coding: utf-8 -*-

'''
Compare 2012 ans 2018 files to detect differences
compare the 2012 and 2018 place_names data sets
1) find missing data
2) find new data
3) find data that has been shifted
4) use dggs if possible



'''

placeNames2012 = r'\\xxxxxxx\Places_fromQuery_2012_DGGS.csv'

placeNames2018 = r'\\xxxxxx\PlacesNames2018with_12_DGGS.csv'

import csv
import math


output = list()

# function to output write a list to a csv file
# requires the list and the filename to save it too
def write_list_to_file(myList, filename):
    """Write the list to csv file."""
    with open(filename, "w") as outfile:
        for entries in myList:
            outfile.write(entries)
            # add a return after each line
            outfile.write("\n")


def cleanPosition(pos):
    pos = pos.replace('(', '')
    pos = pos.replace(')', '')
    pos = pos.replace(',', ' ')
    return pos

# # find based on name and dggs
# def findIn2018XX(name, dggs):
#     with open(placeNames2018) as thisFile:
#         myPN2018 = csv.reader(thisFile)
#         header = next(myPN2018)  # skip the header
#         # search for the name  (only rinds the first
#         for row in myPN2018:
#             if row[2] == name:
#                 # check dggs
#                 if dggs == row[10]:
#                     print('foundit ', row[0])
#                     return row[0]   # return index

# find based on name and dggs
def findIn2018(name12, dggs, ID12):
    # print ('fn', name12, dggs)
    for item in PN_2018.keys():
        # print (item)
        this18Row = PN_2018.get(item)
        name2018 = this18Row[2].title()
        if name2018 == name12 and this18Row[10] == dggs:
            return ('found ' + item + ' ' + name2018 + ' ' + this18Row[10] + ' matched 2012 ' + ID12 + ' ' + name12 +  dggs)








#make empty dictionary for PlaceNames 2018
PN_2018 = {}
PN_2018nameDGGS = {}

# build a 2018 as dictionary - this is the most recent file which will be compared with 2018
# 2018 has about 100,000 less places than the older 2012
with open(placeNames2018) as thisFile:
    myPN2018 = csv.reader(thisFile)
    header = next(myPN2018)       # skip the header
    #fill the dictionary with the key on column 0
    for row in myPN2018:
        temp = row[0]  # grab the data in the first column in this row
        temp = temp.replace('SA_', '')  # fix up - SA_SA in data to match with 2012
        temp = temp.replace('ACT__', '')  # fix up - ACT_ACT in data to match with 2012
        ID = temp.replace('_', '')   # get rid of underscore - to match with 2012
        PN_2018[ID] = row   # make the dictionary entry


print (PN_2018['AAD1182'])


# go through the 2012 file, checking against 2018 version
counted = 0
notfound = 0
my2012_count = 0
output = list()

my2012 = open(placeNames2012)
csv_2012_data = csv.reader(my2012)
print ('building . . . .')


for row12 in csv_2012_data:
    # initialise variables
    # ID_match = False
    name_match = False
    location_match = False
    note = '' # initialise 'note'
    note2 = ''
    my2012_count += 1  # count the rows
    ID = row12[0]   # grab the Record_ID for this 2012 row

    # see if this ID is a key in the 2018 dataset
    if ID in PN_2018:  # then ID is dictionary match
        ID_match = True  # found ID in 2018

        # now check name against ID
        row18 = PN_2018[ID]   # get the data for this row
        #print ('2018row = ', row18)

        # check name match
        name2012 = row12[1]  # name is in row12[1]?
        name2012 = name2012.replace(' Of ', ' of ')
        name2012 = name2012.replace(' And ', ' and ')

        #convert both to title case
        name2018 = row18[2]
        name2018 = name2018.title()
        name2012 = name2012.title()


        if name2018 == name2012:
            name_match = True

            note = ('ID and name matched with 2018')        #+ row18[2] + ' with ' + row12[1])
        else:
            name_match = False
            note = (ID + ' didnt match on 2018name ' + row18[2])


        #found
        counted += 1
        # note = ('found in 2018 - same ID and name = ' +  row12[1])   # make a note of it

    # sometimes the ID has changed
    # if ID dosn't match look for a name and location
    else:
        ID_match = False
        # try to find different ID but matching name and dggs location in 2018
        # search 2012 for
        note = findIn2018(row12[1], row12[6], row12[0])


    # build output
    pushout = (str(row12[0]) + ',' + str(row12[1]) + ',' + str(row12[2]) + ',' + str(row12[3]) +
               ',' + str(row12[4]) + ',' + str(row12[5]) + ',' + str(row12[6]) + ',' + str(note))

    #append output
    output.append(pushout)


print ('counted', str(counted))
#print ('notfound', str(notfound))
print ('my2012 count = ', str(my2012_count))



# # overwrites previous file unless you rename or move it
# write_list_to_file(output, r"\\xxxxx\DGGS_py\PlacesNames2018withDGGS.csv")
#
write_list_to_file(output, r'\\xxxxxx\Compare_2012_18\didnt_find.csv')




print('finished')

# # Build another 2018 dictionary on name location combo for key
# with open(placeNames2018) as thisFile:
#     myPN2018 = csv.reader(thisFile)
#     header = next(myPN2018)       # skip the header
#     #fill the dictionary with the key on columns 1 and 6
#     for row in myPN2018:
#         ID2 = (row[1]+[6])
#         PN_2018nameDGGS[ID2] = row


# for key in PN_2018.keys():
#     print (key)
#
#     this18Row = PN_2018.get(key)
#
#     print (this18Row)
#
#
#     name2018 = this18Row[2].title()  #and convert 2018 name to Title Case
#
#
#     #print(name2018)
#     if name12.title() == name2018:   # including convert 2012 to Title Case
#         # yes name matched
#         print('function print', dggs, this18Row)
#         # now check if dggs similar - ie in same area
#         if dggs == this18Row[10]:  # location the same
#             print('foundit ', this18Row[0])
#             return (this18Row[0] + ' in 2018')  # return index
#         else:
#             # try with a shortened less precise dggs
#             short_dggs = dggs[:6]  # cut back to 5 numbers
#             this18dggs = this18Row[0]
#             short_2018 = this18dggs[:6]
#             if short_dggs == short_2018:
#                 print('foundit in short DGGS', this18Row[0])
#                 return this18Row[0]  # return index
#             else:
#                  return 'no name with spatial match in 2018'
#     else:
#         # no matching name
#         return 'no match on 2018 ID or all names'


