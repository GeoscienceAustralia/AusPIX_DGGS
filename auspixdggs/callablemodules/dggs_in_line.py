
from ..auspixengine.dggs import RHEALPixDGGS
#from shapely.geometry import shape, MultiLineString, LineString 

rdggs = RHEALPixDGGS()

'''
def line_to_DGGS(myLineObj, resolution):  # one poly and the attribute record for it
    """
    Takes a line and a resolution and returns a list of DGGS cells objects.
    myLineObj is expected to be a shapely MultiLineString or LineString object.    
    """
    doneDGGScells = [] #to accumlate a list of completed cells
    arrLines = []
    if(isinstance(myLineObj, MultiLineString)):        
        arrLines = list(myLineObj)
    else: #assume this is a LineString object
        arrLines.append(myLineObj)
    #iterate through list of LineStrings    
    for currLine in arrLines:
        for pt in currLine.coords:  # for each point calculate the DGGS by calling on the DGGS engine
            # ask the engine what cell thisPoint is in
            thisDGGS = rdggs.cell_from_point(resolution, pt, plane=False)# plane=false therefore on the ellipsoid curve
            #add cell if not already in there
            if thisDGGS not in doneDGGScells: # == new one
                doneDGGScells.append(thisDGGS) # save as a done cell
    return doneDGGScells
'''

def line_to_DGGS(line_coords, resolution):  # one poly and the attribute record for it
    """
    Takes a list of line coords and a resolution and returns a list of DGGS cells objects.
    """
    doneDGGScells = [] #to accumlate a list of completed cells
    arrLines = []
    for pt in line_coords:  # for each point calculate the DGGS by calling on the DGGS engine
        # ask the engine what cell thisPoint is in
        thisDGGS = rdggs.cell_from_point(resolution, pt, plane=False)# plane=false therefore on the ellipsoid curve
        #add cell if not already in there
        if thisDGGS not in doneDGGScells: # == new one
            doneDGGScells.append(thisDGGS) # save as a done cell
    return doneDGGScells