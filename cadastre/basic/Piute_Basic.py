# Piute County parcels
# Gets addresses from address points and then gets the rest from county parcel data
#
# Comes with PARCEL_ADD field so a code block adds PARCEL_ADD2, calc equal to PARCEL_ADD, and drop PARCEL_ADD field

import os, arcpy, time
from agrc import parse_address
from arcpy import env

from _createGDBreproject import createGDBreproject
from _addFields import addFields
from _calcBaseAttributes import calcBaseAttributes
from _addressSDEpts import addressSDEpts
from ___addressParcels_Generic import addressParcels_Generic
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

county = 'Piute'
fips = '49031'
recorder = '1-435-577-2550'
url = 'http://www.piute.org/Goverment.htm'
# ******
path = r'L:\agrc\users\rkelson\Cadastre\Basic\2020'
coPath = os.path.join(path, county)
# ******
parcels = r'L:\agrc\data\county_obtained\Piute\PiuteCo_20200229.gdb\PiuteCountyParcels2020'
parcelFld = 'Serial__'
parcelAddrFld = 'PARCEL_ADD2' # comes with PARCEL_ADD
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

    # UNIQUE TO PIUTE
    # Move parcel addresses in parcels from PARCEL_ADD field to PARCEL_ADD2
    if arcpy.ListFields(newParcels, 'PARCEL_ADD'):
        print(" Adding PARCEL_ADD2")

        if not arcpy.ListFields(newParcels, 'PARCEL_ADD2'):
            arcpy.AddField_management(newParcels, 'PARCEL_ADD2', 'TEXT', '', '', '60')

        with arcpy.da.UpdateCursor(newParcels, ['PARCEL_ADD2', 'PARCEL_ADD']) as rows:
            for row in rows:
                row[0] = row[1]
                rows.updateRow(row)

        arcpy.DeleteField_management(newParcels, ['PARCEL_ADD'])

    # Add Fields
    addFields(newParcels)

    # Calc Base fields FIPS, PARCEL_ID, RECORDER, URL, STRUCTURE, CURRENCY
    calcBaseAttributes(newParcels, parcelFld, fips, recorder, url, county, coUpdate)

    # Get SDE address point addresses into the parcels
    addressSDEpts(fips, addrPts, parcelFld)

    # Get other addresses that are not in the address points
    addressParcels_Generic(newParcels, parcelFld, parcelAddrFld)

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