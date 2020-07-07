# Download from http://www.utahcounty.gov/OnlineServices/maps/DataLayers.asp OR use what Michael Foulger pulls down
# This code uses the addresses that come with the parcels because the address points do not have a Parcel ID
# Utah also has a unique Schema
# Code also populates OWNERNAME

import os, sys, arcpy, time
from sweeper import address_parser
from arcpy import env

from __downloadUtahCo import downloadUtahCo
from _createGDBreproject import createGDBreproject
from _addFields import addFields
from _calcBaseAttributes import calcBaseAttributes
from __addressParcels_Utah import addressParcels_Utah
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

county = 'Utah'
fips = '49049'
recorder = '1-801-851-8179'
url = 'https://maps.utahcounty.gov/ParcelMap/ParcelMap.html'
# ******
path = r'L:\agrc\users\rkelson\Cadastre\Basic\2020'
coPath = os.path.join(path, county)
# ******
parcels = r'L:\agrc\data\county_obtained\Utah\UtahCo_20200630.gdb\TaxParcel'
# parcels = r'L:\agrc\users\rkelson\Cadastre\Basic\2020\Utah\TaxParcels.gdb\TaxParcel'
parcelFld = 'PARCELID'
parcelAddrFld = 'SITE_FULLADDRESS'
# ******
sgid = r'C:\Users\rkelson\AppData\Roaming\ESRI\ArcGISPro\Favorites\SGID_'
sgidfc = sgid + 'Cadastre.sde\\SGID.CADASTRE.Parcels_' + county
addrPts = sgid + 'Location.sde\\SGID.LOCATION.AddressPoints'
landOwn = sgid + 'Cadastre.sde\\SGID.CADASTRE.LandOwnership'
munis = sgid + 'Boundaries.sde\\SGID.BOUNDARIES.Municipalities'
zipCodes = sgid + 'Boundaries.sde\\SGID.BOUNDARIES.ZipCodes'
coUpdate = os.path.join(path, 'BasicParcels_2020.gdb\_County_Parcel_Updates')
schema = sgid + 'Cadastre.sde\\SGID.CADASTRE.Parcels_Utah' # **** ! UNIQUE SCHEMA - OWNERNAME ***
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

    # Get a copy of the data
    # downloadUtahCo()

    # Create GDB and Reproject
    createGDBreproject(inGDBpath, coPath, gdb, parcels, newParcels, utmprj)

    # Add Fields
    addFields(newParcels)

    # Calc Base fields FIPS, PARCEL_ID, RECORDER, URL, STRUCTURE, CURRENCY
    calcBaseAttributes(newParcels, parcelFld, fips, recorder, url, county, coUpdate)

    # Use addresses in parcels
    addressParcels_Utah(newParcels, parcelAddrFld)

    # CALC OWNERNAME - Unique to Utah County
    def Ownername():
        print(' * Calculating Ownername')

        with arcpy.da.UpdateCursor(newParcels, ['OWNERNAME']) as rows:
            for row in rows:
                if row[0] != None:
                    if row[0].find(',') > -1:
                        row[0] = ''
                rows.updateRow(row)
    Ownername()

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