# gRAND County
# After getting addresses from the address points in SDE get additional addresses from the county parcels

# SITEADDRESS IS BACKWARDS SO cleanAddresses() DOES NOT GET CALLED and I don't look for .isdigit

import arcpy
from agrc import parse_address

def addressParcels_Grand(newParcels, parcelFld):

    print(' ** Getting other addresses from Parcels that are not in the address points')

    exp = "{0} IS NULL AND {1} <> '' AND {1} IS NOT NULL".format('PARCEL_ADD', 'SITEADDRESS')
    print ('Where Clause is', exp)

    arcpy.MakeFeatureLayer_management(newParcels, 'newParcelsFl', exp)
    print(arcpy.GetCount_management('newParcelsFl'),' records with Parcel addresses and no Address Point')

    #  CALC PARCEL_ADD & OrigAddress
    def calcAddress():

        print(' ** Calculating PARCEL_ADD & OrigAddress for parcels that do not have address points')

        with arcpy.da.UpdateCursor('newParcelsFl', ['PARCEL_ADD', 'OrigAddress', 'SITEADDRESS']) as rows:

            for row in rows:

                if row[2] != None:

                    row[0] = row[2].strip().replace('  ',' ')     #PARCEL_ADD
                    row[1] = row[2]     #OrigAddress

                    rows.updateRow(row)
    calcAddress()

    arcpy.Delete_management('newParcelsFl')

##    # Clean Addresses
##    def cleanAddresses():
##
##        print(' * Cleaning Addresses')
##
##        exp = "{0} IS NOT NULL AND {1} IS NULL".format('PARCEL_ADD', 'PT_ADDRESS')
##        print ('NEW Where Clause is', exp)
##
##        arcpy.MakeFeatureLayer_management(newParcels, 'newParcelsFl', exp)
##        print(arcpy.GetCount_management('newParcelsFl'),' records with Addresses from Parcels') # should be 2360 on 1/22/20
##
##        def NullOrEmpty(value):
##            if value is None:
##                return True
##
##            value = value.strip()
##            return len(value) < 1
##
##        def NotNumericAddress(value):
##            if not value[0].isdigit():
##                return True
##
##        def DirWType(value):
##            ex = ['NORTH CIR', 'SOUTH CIR', 'EAST CIR', 'WEST CIR','NORTH ST', 'SOUTH ST', 'EAST ST', 'WEST ST']
##            return any(value.find(e) > -1 for e in ex)
##
##        def IsApartment(value):
##            ex = ['#', '&', '-', 'UNIT', 'BLDG', '/', 'TRLR']
##            return any(value.find(e) > -1 for e in ex)
##
##        def IsHWY(value):
##            ex = ['HWY', 'HIGHWAY', ' CR ', 'COUNTY ROAD', ' SR ', 'STATE ROAD', 'STATE ROUTE', 'US HIGHWAY', 'U.S. HIGHWAY', 'UTAH STATE HIGHWAY', 'STATE HIGHWAY']
##            return any(value.find(e) > -1 for e in ex)
##
##        def HasAliasStreet(value):
##            return value.find('(') > -1
##
##        def SkipName(value):
##            skipNameList = ['TRUNKJUNK'] # JUNK
##            return any(value.find(e) > -1 for e in skipNameList)
##
##        with arcpy.da.UpdateCursor('newParcelsFl',['PARCEL_ADD', 'OrigAddress', 'OID@']) as rows:
##
##            for row in rows:
##
##                if NullOrEmpty(row[1]):
##                    continue
##
####                if NotNumericAddress(row[1]):
####                    row[0] = ""
##
##                if DirWType(row[1]):
##                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")
##
##                if IsApartment(row[1]):
##                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")
##                    row[0] = row[1].replace(" NORTH"," N").replace(" SOUTH"," S").replace(" EAST"," E").replace(" WEST"," W")
##                    row[0] = row[1].replace(" WY "," WAY ").replace(" AV "," AVE ").replace(" CI "," CIR ").replace(" COVE "," CV ").replace(" LA "," LN ").replace(" TRAIL ", " TRL ").replace(" CRT ", " CT ")
##
##                if IsHWY(row[1]):
##                    row[0] = row[1].replace(" COUNTY ROAD ", " CR ")
##                    row[0] = row[1].replace(" STATE ROAD ", " SR ")
##                    row[0] = row[1].replace(" STATE ROUTE ", " SR ")
##                    row[0] = row[1].replace(" US HIGHWAY ", " HWY ")
##                    row[0] = row[1].replace(" U.S. HIGHWAY ", " HWY ")
##                    row[0] = row[1].replace(" UTAH STATE HIGHWAY ", " HWY ")
##                    row[0] = row[1].replace(" STATE HIGHWAY ", " HWY ")
##                    row[0] = row[1].replace(" HIGHWAY ", " HWY ")
##                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")
##                    row[0] = row[1].strip().upper().replace("  "," ")
##
##                if HasAliasStreet(row[1]):
##                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")
##                    row[0] = row[1].replace("ROAD","RD").replace("LANE","LN").replace("DRIVE","DR").replace("STREET","ST")
##                    row[0] = row[1].strip().upper().replace("  "," ")
##
##                if SkipName(row[1]):
##                    row[0] = row[1].replace("ROAD","RD").replace("LANE","LN").replace("DRIVE","DR").replace("STREET","ST").replace("CIRCLE", "CIR")
##                    row[0] = row[1].strip().upper().replace("  "," ")
##
####                if not (NullOrEmpty(row[1]) or NotNumericAddress(row[1]) or DirWType(row[1]) or IsApartment(row[1]) or IsHWY(row[1]) or HasAliasStreet(row[1]) or SkipName(row[1])):
##                if not (NullOrEmpty(row[1]) or DirWType(row[1]) or IsApartment(row[1]) or IsHWY(row[1]) or HasAliasStreet(row[1]) or SkipName(row[1])):
##                    address = parse_address.parse(row[1])
##                    row[0] = address.normalizedAddressString
##
####                row[0] = row[0].strip().upper().replace("  "," ").replace(".","").replace(",","").replace(" RD RD"," RD")
##                rows.updateRow(row)
##    cleanAddresses()
##
##    arcpy.Delete_management('newParcelsFl')

    #-------------End Clean Addresses-----------
