# -*- coding: utf-8 -*-
''' this code grabs a CSV and converts it to a shapefile
It looks for longi and lati in the columns and uses this to make point shapefiles
you need to match the longi and lati names with the code below
'''



# import libraries
import shapefile, csv

# # funtion to generate a .prj file
# def getWKT_PRJ (epsg_code):
#     import urllib
#     wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
#     remove_spaces = wkt.read().replace(" ","")
#     output = remove_spaces.replace("\n", "")
#     return output

# create a point shapefile
out_File = shapefile.Writer(shapefile.POINT)

# for every record there must be a corresponding geometry.
out_File.autoBalance = 1

# create the shapefile field names and data type for each column.
out_File.field("ID", "C")
out_File.field("AuthID", "C")
out_File.field("Name", "C")
out_File.field("Feature", "C")
out_File.field("Category", "C")
out_File.field("Group", "C")
out_File.field("Latitude", "C")
out_File.field("Longitude", "C")
out_File.field("Auth", "C")
out_File.field("SupDate", "C")
out_File.field("DGGSrHealPix", "C")
out_File.field("Cell_width", "C")
out_File.field("DGGS_level", "C")
'''  NOTES:
C is ASCII characters
N is a double precision integer limited to around 18 characters in length
D is for dates in the YYYYMMDD format, with no spaces or hyphens between the sections.
F is for floating point numbers with the same length limits as N
L is for logical data which is stored in the shapefile's attribute table as a short integer as a 1 (true) or a 0 (false). The values it can receive are 1, 0, y, n, Y, N, T, F or the python builtins True and False
'''
# count the features
counter = 1

# access the CSV file
in_csvFile = r'\\xxxxxx8\ACT_PlacesNames2018withDGGS.csv'
# read through the csv and make attribute table
with open(in_csvFile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    # skip the header
    next(reader, None)

    # read each row of CSV and save into variables so they can go into shapefile attribute table
    for row in reader:
        Id = row[0]
        AuthID = row[1]
        Name = row[2]
        Feature = row[3]
        Category = row[4]
        Group = row[5]
        Latitude = row[6]
        Longitude = row[7]
        Authority = row[8]
        Sup_Date = row[9]
        DGGSrheal = row[10]
        cell_width = row[11]
        DGGS_Level = row[12]


        # create the point geometry for shapefile
        out_File.point(float(Longitude),float(Latitude))

        # add attribute data
        out_File.record(Id, AuthID, Name, Feature,Category, Group, Latitude, Longitude, Authority, Sup_Date, DGGSrheal, cell_width, DGGS_Level)

        print("Feature " + str(counter) + " added to Shapefile.")
        counter = counter + 1

# save the Shapefile
to_save = 'test\ACT_PlaceNames08'
out_File.save(to_save)

# create a projection file

# writing the projection file into WGS84
prj = open("%s.prj" % to_save, "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()







'''
alternative script that wouldn't work for Oi
'''
# import pandas as pd
# from geopandas import GeoDataFrame
# from shapely.geometry import Point
#
# # read the file
# # file with the source data - MUST BE CSV with Lat Long
# # latitude must be called lati, longitude must be called longi
# f = r'\\xxxxxwithDGGS.csv'
#
# # read in the csv file using pandas
# df = pd.read_csv(f)  # read the file in using pandas
#
# geometry = [Point(xy) for xy in zip(df.longi, df.lati)]
# df['geometry'] = geometry
# # print(df.longi)
# print(list(df.columns.values)) # print a list of column headers
# # print(df.head()) # print a summary of the file
# print(df)  # print all the data
# crs = {'init': 'epsg:4326'} # = WGS84
#
# # convert to geopandas including telling it which field is the Point geometry (and the crs)
# geo_df = GeoDataFrame(df, crs=crs, geometry=geometry)
#
# # output filename
# thisFile = 'test\ACT_PlaceNames.shp'    # adjust the file name to where you want it
# projFile = thisFile.replace('.shp', '')
# # convert to shapefile
# geo_df.to_file(driver='ESRI Shapefile', filename= thisFile)  # adjust the file name to where you want it
#
# # writing the projection file
# prj = open("%s.prj" % projFile, "w")
# epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
# prj.write(epsg)
# prj.close()





print('finished')


