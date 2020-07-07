# Summit Parcels
# Data comes from county with a bunch of relationship tables
# Add field Situs text 60
# Join OWNERSHIP table to parcels on Serial and SERIAL and populate Situs with SITUS

import os, sys, arcpy, time
from sweeper import address_parser
from arcpy import env

from _createGDBreproject import createGDBreproject
from _addFields import addFields
from _calcBaseAttributes import calcBaseAttributes
# from _addressSDEpts import addressSDEpts
from __addressParcels_Summit import addressParcels_Summit
from _repairGeometry import repairGeometry
import _feature2point
from _identity import identity
from _spatialJoin import spatialJoin
from _calcOwnZipsMuni import calcOwnZipsMuni
from _load2SDEtol import load2SDEtol
from _loadFile import loadFile

startTime = time.clock()
env.qualifiedFieldNames = False

sys.exit('populate CoUpdates data')
sys.exit('On last update there was no correct Parcel ID in the address points, so I used the addresses in the parcels')

county = 'Summit'
fips = '49043'
recorder = '1-435-366-3238'
url = 'http://maps.summitcounty.org/flexviewers/countymap/'
# ******
path = r'L:\agrc\users\rkelson\Cadastre\Basic\2020'
coPath = os.path.join(path, county)
# ******
parcels = r'L:\agrc\data\county_obtained\Summit\Summit_20200131.gdb\Parcels'
parcelFld = 'Serial'
# ******
sgid = r'C:\Users\rkelson\AppData\Roaming\ESRI\ArcGISPro\Favorites\SGID_'
sgidfc = sgid + 'Cadastre.sde\\SGID.CADASTRE.Parcels_' + county
addrPts = sgid + 'Location.sde\\SGID.LOCATION.AddressPoints'
landOwn = sgid + 'Cadastre.sde\\SGID.CADASTRE.LandOwnership'
munis = sgid + 'Boundaries.sde\\SGID.BOUNDARIES.Municipalities'
zipCodes = sgid + 'Boundaries.sde\\SGID.BOUNDARIES.ZipCodes'
coUpdate = os.path.join(path, 'BasicParcels_2020.gdb\_County_Parcel_Updates')
schema = os.path.join(path, 'BasicParcels_2020.gdb\_BasicParcel_Schema')
utmprj = arcpy.SpatialReference(r'L:\agrc\users\rkelson\UTM.prj')
# ******
gdb = county + '_Parcels_2020.gdb'
inGDBpath = os.path.join(coPath, gdb)

newParcels = os.path.join(inGDBpath, county + '_Parcels_2020_UTM')
newParcelsFinal = os.path.join(inGDBpath, county + '_Parcels_2020_UTM_Final')
newParcelsFinalSDE = os.path.join(path, 'BasicParcels_2020.gdb', county + '_Parcels_2020')
parcelPts = os.path.join(inGDBpath, county + '_PTS')

owner = parcelPts + '_OWN'
zips = parcelPts + '_OWN_ZIPS'
parcelPtsFinal = parcelPts + '_OWN_ZIPS_MUNI'
# ******

def p1():
    # Create GDB and Reproject
    createGDBreproject(inGDBpath, coPath, gdb, parcels, newParcels, utmprj)

    # Add Fields
    addFields(newParcels)

    # Calc Base fields FIPS, PARCEL_ID, RECORDER, URL, STRUCTURE, CURRENCY
    calcBaseAttributes(newParcels, parcelFld, fips, recorder, url, county, coUpdate)

    # Get SDE address point addresses into the parcels
    # addressSDEpts(fips, addrPts, parcelFld)

    # Use addresses in parcels
    addressParcels_Summit(newParcels, parcelFld)

    # Repairing Geometry 1st time
    repairGeometry(newParcels, startTime)

    # Feature to Point
    _feature2point.feature2point(parcelPts, newParcels)

def p2():
    # Feature to Point 2nd time
    _feature2point.feature2point_2(parcelPts, newParcels)

    # Identity with Munis, Land Ownership, and Zips
    identity(parcelPts, landOwn, owner, zipCodes, zips, munis, parcelPtsFinal, newParcelsFinal)

    # Spatial Join points to new layer
    spatialJoin(newParcels, parcelPtsFinal, newParcelsFinal)

    # Calc PARCEL_OWN, PARCEL_ZIP, PARCEL_MUNI
    calcOwnZipsMuni(newParcelsFinal, county)

    # Load data into new FC with SDE Tols
    load2SDEtol(newParcelsFinalSDE, path, county, schema, newParcelsFinal, startTime)

    # Write lines to CountyName_LOAD.txt to Copy features into SDE
    loadFile(coPath, county, sgid, sgidfc, newParcelsFinalSDE)

p1()
p2()