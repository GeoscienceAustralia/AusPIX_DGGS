# -*- coding: utf-8 -*-
"""
Created on March 2019
@author: Joseph Bell Geoscience Australia
"""

''' Build a DGGS triple store using multi processors :)
1. select the area
2 calculate dggs cells over the area

3. Convert into ttl file
centroids, area, top left , bottom right

'''
import time
import numpy as np
import point_DGGSvalue as d
from multiprocessing import Pool

#todays date
from datetime import date
today = str(date.today())

#start the clock
start = time.time()

resolution = 14
dggsList = list()

# function to write a python list to a csv file
def write_list_to_file(output, out_filename):
    """Write the list to csv file."""
    with open(out_filename, "w") as outfile:
        for entries in output:
            outfile.write(str(entries))
            outfile.write("\n")# add a return after each line





def multi_calc(allCoords):  # split into chucks for multi processor

    chunks = [allCoords[x:x + 100000] for x in range(0, len(allCoords), 100000)]
    print('number of chunks', len(chunks))

    pool = Pool(processes=7)

    result = pool.map_async(calc_DGGS, chunks)

    while not result.ready():
        print("Running...")
        time.sleep(0.5)

    return result.get()

def calc_DGGS(coordsList):
    global resolution
    global dggsList
    output = list()
    already = 0
    for coord in coordsList:
        coordinates = (coord[0], coord[1])
        #print(coordinates)
        dggs = d.latlong_to_DGGS(coordinates, resolution)
        # dggs variable contains the cell name, centroid, area and width - this has been caclulated on the plane but should be elipsoid


        if dggs[0] not in dggsList:

            #print('answer', dggs[0], dggs[1], dggs[2], dggs[3], dggs[4], dggs[5])
            dggsList.append(dggs[0]) # to keep track of duplicates

            longi = dggs[1][0]  # data prep
            longi = round(longi, 8)
            lati = dggs[1][1]
            lati = round(lati, 8)
            thisArea = int(dggs[2])
            thisWidth = int(dggs[3])

            # output to file
            output.append('dggs:' + dggs[0] + '    ' + 'dggs:cellResolution   ' + '"' + str(resolution) + '"' + ' .')
            output.append('dggs:' + dggs[0] + '    ' + 'dggs:centroidLong     ' + '"' + str(longi) + '"' + ' .')
            output.append('dggs:' + dggs[0] + '    ' + 'dggs:centroidLat      ' + '"' + str(lati) + '"' + ' .')
            output.append('dggs:' + dggs[0] + '    ' + 'dggs:area_m2          ' + '"' + str(thisArea) + '"' + ' .')
            output.append('dggs:' + dggs[0] + '    ' + 'dggs:planarWidth_m    ' + '"' + str(thisWidth) + '"' + ' .')
            output.append('dggs:' + dggs[0] + '    ' + 'dggs:upperLeft        ' + '"' + str(dggs[4]) + '"' + ' .')
            output.append('dggs:' + dggs[0] + '    ' + 'dggs:bottomRight      ' + '"' + str(dggs[5]) + '"' + ' .')
            # output.append('dggs:' + dggs[0] + '    ' + 'dggs:coords           ' + '"' + str(coordinates) + '"' + ' .')

            output.append(' ')

        else:
            # print('copy', dggs)
            already += 1
        #print(coordinates, dggs, resolution)
    print('already =', already)
    return output



if __name__ == '__main__':
    # main
    longStart = 148.75
    longEnd = 149.4
    latStart = -35.93
    latEnd = -35.12

    step = 0.00005  # need to step small enough to catch every DGGS cell
    # should be some doubled up - but filtered out in the program



    #print(np.arange(longStart, longEnd, step))
    print()
    #print(np.arange(latStart, latEnd, step))
    longList = np.arange(longStart, (longEnd + step), step)
    latList = np.arange(latStart, latEnd, step)

    # make a list of long lat sets
    allCoords = list()
    for long in longList:
        for lat in latList:
            thisCoord = list()
            thisCoord.append(long)
            thisCoord.append(lat)
            allCoords.append(thisCoord)




    print('len of all coords', len(allCoords))

    results = multi_calc(allCoords) # call the multi processor


    output = list()  # set up the output file
    # put name of the file at the top of the turtle file
    output.append(
        '# from long ' + str(longStart) + ' to ' + str(longEnd) + ' and Lat ' + str(latStart) + ' to ' + str(latEnd))
    output.append('# processed by buildDGGStroples.py')
    output.append('# ' + today)  # add the day the ttl was produced
    output.append('@prefix dggs: <http://ACT_dggs.data.gov.au/def/LGAs#> .')
    output.append(' ')  # blank line

    print('SETTING UP OUPUT . . . ')
    for thing in results:
        for item in thing:
            output.append(item)




#     # overwrites previous file unless you rename or move it
    write_list_to_file(output, r'\\prod.lan\active\ops\nlib\NLI Reform Project\Place Names Linked Data Project\data\ACT_DGGStriples_Multi.ttl')
#
#
#
    print('len of all coords', len(allCoords))


    print('finished')

    end = time.time()
    print('time taken = ', end - start, ' seconds or ', (end - start)/60, 'mins')