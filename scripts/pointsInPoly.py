# -*- coding: utf-8 -*-



import shapefile
from shapely.geometry import shape, Point


'''
using shapely to dig information out of shapefiles
example

'''

# read your shapefile
#thisShape = r'\\xxxxxxxxxxACT_grid\ACTgrid01.shp'
file_poly = r'\\xxxxx\ACT_grid\ACT_SA3'  # don't include .shp

def check(lon, lat):
    # build a shapely point from your geopoint
    point = Point(lon, lat)

    # function does exactly what you want
    return polygon.contains(point)


r = shapefile.Reader(file_poly)


# get the shapes
shapes = r.shapes()

print(r.records())
print('number of records', len(shapes))

print('type =', shapes[3].shapeType)

fields = r.fields
print('fields = ', fields)

records = r.records()
print(len(records))

for item in records:
    print(item[2])  # prints the name field 0 1 2


for item in shapes:
    print()
    # build a shapely polygon from your shape
    #polygon = shape(shapes[item])
    polygon = shape(item)
    print(polygon.bounds)
    # Get the bounding box of the 4th shape.
    # Round coordinates to 3 decimal places
    bbox = item.bbox
    print('bbox', ['%.3f' % coord for coord in bbox])

    print('representitive point', polygon.representative_point())
    print('number of points', len(item.points))
    print('parts', item.parts)
    print('Is_Valid =', polygon.is_valid)

    if check(148.961, -35.469):
        print('found', item)





print('finished')

# from osgeo import ogr
# file = ogr.Open("my_shapefile.shp")
# shape = file.GetLayer(0)
# #first feature of the shapefile
# feature = shape.GetFeature(0)
# first = feature.ExportToJson()
# print first # (GeoJSON format)
# {"geometry": {"type": "LineString", "coordinates": [[0.0, 0.0], [25.0, 10.0], [50.0, 50.0]]}, "type": "Feature", "properties": {"FID": 0.0}, "id": 0}

''' 
Output example
[['80104', '80104', 'Gungahlin', '8', 'Australian Capital Territory', 91.8565], ['80103', '80103', 'Canberra East', '8', 'Australian Capital Territory', 211.9214], ['80111', '80111', 'Urriarra - Namadgi', '8', 'Australian Capital Territory', 1619.5054], ['80110', '80110', 'Molonglo', '8', 'Australian Capital Territory', 27.1506], ['80105', '80105', 'North Canberra', '8', 'Australian Capital Territory', 44.7227], ['80107', '80107', 'Tuggeranong', '8', 'Australian Capital Territory', 159.7084], ['80109', '80109', 'Woden Valley', '8', 'Australian Capital Territory', 28.6004], ['80106', '80106', 'South Canberra', '8', 'Australian Capital Territory', 44.4112], ['80101', '80101', 'Belconnen', '8', 'Australian Capital Territory', 112.1467], ['80108', '80108', 'Weston Creek', '8', 'Australian Capital Territory', 18.1487]]
number of records 10
type = 5
fields =  [('DeletionFlag', 'C', 1, 0), ['SA3_CODE', 'C', 5, 0], ['SA3_CODE16', 'C', 5, 0], ['SA3_NAME', 'C', 50, 0], ['STATE_CODE', 'C', 1, 0], ['STATE_NAME', 'C', 50, 0], ['AREA_SQKM', 'F', 19, 11]]
10
Gungahlin
Canberra East
Urriarra - Namadgi
Molonglo
North Canberra
Tuggeranong
Woden Valley
South Canberra
Belconnen
Weston Creek

(149.04619299400008, -35.23139136899994, 149.20071556100004, -35.12441600599993)
bbox ['149.046', '-35.231', '149.201', '-35.124']
representitive point POINT (149.1274850768994 -35.17807550649997)
number of points 203
parts [0]
Is_Valid = True

(149.118535446, -35.410674997999934, 149.39928720500006, -35.20556536899994)
bbox ['149.119', '-35.411', '149.399', '-35.206']
representitive point POINT (149.2676579561013 -35.30813083949994)
number of points 670
parts [0]
Is_Valid = True

(148.76278998500004, -35.92076221499997, 149.1111300340001, -35.21846708399994)
bbox ['148.763', '-35.921', '149.111', '-35.218']
representitive point POINT (148.9422306946992 -35.56947910899996)
number of points 1630
parts [0]
Is_Valid = True
found <shapefile._Shape object at 0x00000000033726D8>

(149.00877998300007, -35.32740100299998, 149.08787201500002, -35.26588700499997)
bbox ['149.009', '-35.327', '149.088', '-35.266']
representitive point POINT (149.041671544968 -35.29663500399997)
number of points 159
parts [0]
Is_Valid = True

(149.07017999100003, -35.30617299399995, 149.17768913500004, -35.22248441399995)
bbox ['149.070', '-35.306', '149.178', '-35.222']
representitive point POINT (149.1205186649136 -35.26412911699995)
number of points 693
parts [0]
Is_Valid = True

(149.00785576600003, -35.592783003999955, 149.15509501400004, -35.35896407599995)
bbox ['149.008', '-35.593', '149.155', '-35.359']
representitive point POINT (149.1028130277402 -35.47581381249998)
number of points 690
parts [0]
Is_Valid = True

(149.06294072700007, -35.38426136399994, 149.12736417600001, -35.31231162699993)
bbox ['149.063', '-35.384', '149.127', '-35.312']
representitive point POINT (149.0971901247547 -35.34844289449995)
number of points 119
parts [0]
Is_Valid = True

(149.07112307800003, -35.34791900199997, 149.1927160020001, -35.28401143699995)
bbox ['149.071', '-35.348', '149.193', '-35.284']
representitive point POINT (149.1336875870768 -35.31602099699995)
number of points 652
parts [0]
Is_Valid = True

(148.96134451000012, -35.28063000699996, 149.12511968100011, -35.168722007999975)
bbox ['148.961', '-35.281', '149.125', '-35.169']
representitive point POINT (149.0435712946654 -35.22444929899996)
number of points 327
parts [0]
Is_Valid = True

(149.02243671400004, -35.36688584999996, 149.08298419100004, -35.299602755999956)
bbox ['149.022', '-35.367', '149.083', '-35.300']
representitive point POINT (149.0436135775917 -35.33385887249997)
number of points 166
parts [0]
Is_Valid = True
finished


'''