''' this script DGGS enables a csv point file
written by Joseph Bell October 2019'''
import csv # import csv reader
from dggs import RHEALPixDGGS  # import the DGGS
rdggs = RHEALPixDGGS()  # make an instance of dggs

# point to the CSV file
myFile = r'C:\Users\u82871\PycharmProjects\doc_scripts\AusPIX_DGGS\test_data\PointFile_example.csv'

def write_list_to_file(myList, filename):
    ''' function to write a CSV from a python list
    requires the list and the filename to save it to the as inputs'''
    with open(filename, "w") as outfile:  # Write the list to csv file
        for entries in myList:
            #cleanup for csv output
            thisRow = str(entries)  #convert to string
            thisRow = thisRow.replace('[', '')
            thisRow = thisRow.replace(']', '')
            thisRow = thisRow.replace("'", "")
            outfile.write(thisRow) # write
            outfile.write("\n") # add a new line

# variables declarations
output = [] # to hold data output to CSV
resolution = 10  # # define resolution ’

# open the data file
with open(myFile) as csvDataFile:
    csvReader = csv.reader(csvDataFile) # read the data in
    headerOutput = next(csvReader)  # skip the header - or save it for output header
    headerOutput.insert(0, 'ausPIXdggs')  # add column header for DGGS
    output.append(headerOutput)  # add the header to output

    for row in csvReader: # iterate through the rows one by one
        thisRow = []

        # needs to be modified to point to the lat and long columns in the csv file - first column == 0
        # get the latitude and longitude for on the row - points need to be longitude first
        thisPoint = [float(row[2]), float(row[1])]   # converting string to float as well

        # ask the engine what cell thisPoint is in
        thisDGGS = rdggs.cell_from_point(resolution, thisPoint, plane=False)
        # plane=false therefore on the ellipsoid curve

        row.insert(0, str(thisDGGS))  #insert dggs at front of row
        output.append(row)  # add this row to output

# send output to file by calling function 'write_list_to_file'
write_list_to_file(output, r'C:\Users\u82871\PycharmProjects\doc_scripts\AusPIX_DGGS\test_data\PointFile_dggs.csv')
