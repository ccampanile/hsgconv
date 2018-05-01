"""
hs_gridconv.py
Provides conversion support from/to England's highways standards local grids to OSGB36 EPSG:27700
author: ccampanile<at>brydenwood.co.uk
date: 2018/04/30
version: 1.0.0
Compatible with Python versions 2.7-3.x
"""

__version__ = "1.0.0"



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



#Begin Library

def GridParams(gridID, mean_z):
    """
    Retrieve conversion params specific to a grid
    Input:
        gridID: string, refer to the list at http://www.standardsforhighways.co.uk/ha/standards/ians/pdfs/ian99.pdf
        mean_z: float, mean altitude of the scheme's bounding box
    Returns:
        Conversion_parameters: tuple, ('gridID, PSF, ESF, CSF, 1/CSF, Eo, No')
            
    """
    ESF = __CalculateESF(mean_z)
    (Es,Ns,Eo,No,PSF,bands) = __LocalParams(gridID)
    return (gridID,PSF,ESF,(PSF*ESF), 1/(PSF*ESF) ,Eo,No)


def CreateParamList(gridID, PSF, ESF, Eo, No):
    """
    Create a custom parameters list
    Input:
        todo
    Returns:
        todo
    """
    CSF = PSF*ESF
    return (gridID, PSF, ESF, CSF, 1/CSF, float(Eo), float(No))


def ConvertToOSBG(myGridParam, x_coord, y_coord):
    """
    Convert local grid's (x,y) to OBSG's (easting, northing)
    Input:
        myGridParam: conversion parameter of local grid as ('gridID, PSF, ESF, CSF, 1/CSF, Eo, No')
        x_coord: x coordinate in local grid
        y_coord: y coordinate in local grid
    Returns:
        todo
    """
    OSBG_coord = __ConvertLocalToOBSG(x_coord, y_coord, myGridParam[5], myGridParam[6], myGridParam[3])
    
    return OSBG_coord


def ConvertToLocalGrid(myGridParam, easting, northing):
    """
    Convert OSBG's (easting, northing) to local grid's (x,y)
    Input:
        myGridParam: conversion parameter of local grid as ('gridID, PSF, ESF, CSF, 1/CSF, Eo, No')
        easting: easting in OSBG36
        northing: northing in OSBG36
    Returns:
        todo
    """
    local_coord = __ConvertOSBGToLocal(easting, northing, myGridParam[5], myGridParam[6], myGridParam[4])
    
    return local_coord


#non-exposed functions

def __GetBandsData():
    #localpath
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "docs", "LocalGrid_DataBands.csv")
    return open(DATA_PATH)


def __GetGridData():
    #localpath
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "docs", "LocalGrid_DataParams.csv")
    return open(DATA_PATH)


def  __ConvertLocalToOBSG(e_local, n_local, Eo, No, CSF):
    """
    Convert local grid to OSBG coordinates
    Input:
        e_local: x coord in local grid
        n_local: y coord in local grid
        Eo: delta easting of local grid
        No: delta northing of local grid
        CSF: grid's associated scale factor
    Returns:
        todo
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
    Inputs:
        easting: easting in OSBG36
        northing: northing in OSBG36
        Eo: delta easting of local grid
        No: delta northing of local grid
        one_over_CSF: reciprocal CSF (combinated scale factor, = 1/CSF)
    Returns:
        todo
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
    Input:
        todo
    Returns:
        todo
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
    Input:
        todo
    Returns:
        todo
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
