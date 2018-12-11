"""
hsgconv.py
Provides conversion support from/to England's highways standards local grids to OSGB36 EPSG:27700
author: ccampanile<at>brydenwood.co.uk
date: 2018/12/10
version: 1.0.15
Compatible with Python versions 2.7-3.x
"""

__title__ = 'hsgconv'
__version__ = '1.0.15'

#import statements
import sys
import os


#python 3 compatibility
PYTHON3 = sys.version_info[0] == 3

if PYTHON3:
    xrange = range
    izip = zip
else:
    from itertools import izip


#Begin Module

def GridParams(gridID, mean_z):
    """
    Retrieve conversion params specific to a grid

    :param gridID: string, refer to the list at http://www.standardsforhighways.co.uk/ha/standards/ians/pdfs/ian99.pdf
    :param mean_z: float, mean altitude of the scheme's bounding box

    :returns: Conversion_parameters: tuple, `('gridID, PSF, ESF, CSF, 1/CSF, Eo, No')`
    """
    ESF = __CalculateESF(mean_z)
    (Es,Ns,Eo,No,PSF,bands) = __LocalParams(gridID)
    return (gridID,PSF,ESF,(PSF*ESF), 1/(PSF*ESF) ,Eo,No)


def CreateParamList(gridID, PSF, ESF, Eo, No):
    """
    Create a custom parameters list. **Be careful** of your inputs

    :param gridID: string, refer to the list at http://www.standardsforhighways.co.uk/ha/standards/ians/pdfs/ian99.pdf
    :param PSF: float - Projection Scale Factor
    :param ESF: float - Elevation Scale Factor
    :param Eo: float - delta Easting
    :param No: float - delta Northing
    
    :returns: Custom parameters for coordinate conversion
    """
    CSF = PSF*ESF
    return (gridID, PSF, ESF, CSF, 1/CSF, float(Eo), float(No))


def ConvertToOSBG(myGridParam, x_coord, y_coord):
    """
    Convert local grid's (x,y) to OBSG's (easting, northing)
    
    :param myGridParam: conversion parameter of local grid `('gridID, PSF, ESF, CSF, 1/CSF, Eo, No')`
    :param x_coord: x coordinate in local grid
    :param y_coord: y coordinate in local grid
    
    :returns: OSBG36's Easting and Northing
    """
    OSBG_coord = __ConvertLocalToOBSG(x_coord, y_coord, myGridParam[5], myGridParam[6], myGridParam[3])
    return OSBG_coord


def ConvertToLocalGrid(myGridParam, easting, northing):
    """
    Convert OSBG's (easting, northing) to local grid's (x,y)
    
    :param myGridParam: conversion parameter of local grid as ('gridID, PSF, ESF, CSF, 1/CSF, Eo, No')
    :param easting: easting in OSBG36
    :param northing: northing in OSBG36
    
    :returns: HS local grid's X and Y coordinates
    """
    local_coord = __ConvertOSBGToLocal(easting, northing, myGridParam[5], myGridParam[6], myGridParam[4])
    return local_coord


#non-exposed functions

def __GetBandsData():
    """
    Get Local Grid's elevation parameter

    :param _: todo
    
    :returns: todo
    """
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "data", "LocalGrid_DataBands.csv")
    return open(DATA_PATH)


def __GetGridData():
    """
    Get Local Grid's transformation parameters

    :param _: todo
    
    :returns: todo
    """
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "data", "LocalGrid_DataParams.csv")
    return open(DATA_PATH)


def  __ConvertLocalToOBSG(e_local, n_local, Eo, No, CSF):
    """
    Convert local grid to OSBG coordinates

    :param e_local: x coord in local grid
    :param n_local: y coord in local grid
    :param Eo: delta easting of local grid
    :param No: delta northing of local grid
    :param CSF: grid's associated scale factor
    
    :returns: todo
    """
    #Easting national grid
    easting = e_local*CSF + Eo
    #Northing national grid
    northing = n_local*CSF + No
    #Return a tuple of coordinates
    return (easting, northing)


def  __ConvertOSBGToLocal(easting, northing, Eo, No, one_over_CSF):
    """
    Convert OSBG36 Easting-Northing to local grid coordinates

    :param easting: easting in OSBG36
    :param northing: northing in OSBG36
    :param Eo: delta easting of local grid
    :param No: delta northing of local grid
    :param one_over_CSF: reciprocal CSF (combinated scale factor, = 1/CSF)

    :returns: todo
    """

    #x-coord in local grid
    x_local = (easting - Eo)*(one_over_CSF)
    #y-coord in local grid
    y_local = (northing - No)*(one_over_CSF)
    #return a tuple of coordinates    
    return (x_local, y_local)


def __CalculateESF(myElevation):
    """
    Retrieve the ElevationScaleFactor

    :param _: todo
    
    :returns: todo
    """
    #list out elevation and elevation scale factors
    elevation_list = [0,80,160,240,320,400,480,520,640,720,800]
    ESF_list = [1,0.9999875,0.999975,0.9999625,0.99995,0.9999375,0.999925,0.9999125,0.9999,0.9998875,0.999875]
    
    #find at which elevation band myElevation is
    closestAltitude = min(elevation_list, key=lambda x:abs(x-myElevation))
    #find the index of the elevation
    index = elevation_list.index(closestAltitude)
    ESF = ESF_list[index]

    return float(ESF)


def __LocalParams(localGrid):
    """
    Retrieve the parameters from the shared csv with files inside
    
    :param _: todo
    
    :returns: todo
    """
    #check valuable input
    if  (localGrid == None):
        return None
    
    try:
        f = __GetGridData()
    except:
        print ("I have not found any references for this grid")
        return None
    
    #parameters
    foundRecord = False
    Es = None
    Ns = None
    Eo = None
    No = None
    SF = None
    bands = None
    
    #scan lines
    for line in f:
        currentLine = line.split(',')
        if (currentLine[0] == localGrid):
            foundRecord = True
            print("I have found a record for grid zone " + currentLine[0])
            Es = float(currentLine[1])
            Ns = float(currentLine[2])
            Eo = float(currentLine[3])
            No = float(currentLine[4])
            SF = float(currentLine[5])
            bands = currentLine[6].split('*')
            break
            
    if foundRecord:
        #return a list with values
        return (Es,Ns,Eo,No,SF,bands)
    else:
        print("I haven't found any records for the requested grid zone")
        return None   
