# Any County that neeeds a generic address clean job
# After getting addresses from the address points in SDE
# get additional addresses from the county parcels

import arcpy
from sweeper import address_parser

def addressParcels_Generic(newParcels, parcelFld, parcelAddrFld):

    print(' ** Getting other addresses from Parcels that are not in the address points')

    exp = "{0} IS NULL AND {1} <> '' AND {1} IS NOT NULL".format('PARCEL_ADD', parcelAddrFld)
    print ('Where Clause is', exp)

    arcpy.MakeFeatureLayer_management(newParcels, 'newParcelsFl', exp)
    print(arcpy.GetCount_management('newParcelsFl'),' records with Parcel addresses and no Address Point')

    #  CALC PARCEL_ADD & OrigAddress
    def calcAddress():

        print(' ** Calculating PARCEL_ADD & OrigAddress for parcels that do not have address points')

        with arcpy.da.UpdateCursor('newParcelsFl', ['PARCEL_ADD', 'OrigAddress', parcelAddrFld]) as rows:

            for row in rows:

                if row[2] != None and row[2].split(' ')[0].isdigit():

                    row[0] = row[2] #.strip().replace('  ',' ')     #PARCEL_ADD
                    row[1] = row[2]     #OrigAddress

                rows.updateRow(row)

    calcAddress()

    arcpy.Delete_management('newParcelsFl')

    # Clean Addresses
    def cleanAddresses():

        print(' * Cleaning Addresses')

        def SkipName(value):
            skipNameList = ['1940 E 5625 S', '430 E 1525 N', '530 E 3625 N', '890 E 2675 N', '930 E 2675 N']
            return any(value.find(e) > -1 for e in skipNameList)

        exp = "{0} IS NOT NULL AND {1} IS NULL".format('PARCEL_ADD', 'PT_ADDRESS')
        print ('NEW Where Clause is', exp)

        with arcpy.da.UpdateCursor(newParcels, ['PARCEL_ADD', 'OrigAddress', 'OID@'], exp) as rows:

            for row in rows:

                if SkipName(row[1]):
                    row[0] = row[1].replace("ROAD","RD").replace("LANE","LN").replace("DRIVE","DR").replace("STREET","ST").replace("CIRCLE", "CIR")\
                        .strip().upper().replace('  ', ' ')

                else:

                    try:
                        address = address_parser.Address(row[1])
                        row[0] = address.normalized

                    except:
                        print(' * Problem with ObjectID:', row[2], '| Original Address:', row[1])

                        row[0] = row[1].replace('ROAD', 'RD').replace('LANE', 'LN').replace('DRIVE', 'DR').replace('STREET', 'ST').replace('CIRCLE', 'CIR')\
                            .replace('NORTH', 'N').replace('SOUTH', 'S').replace('EAST', 'E').replace('WEST', 'W')\
                            .strip().upper().replace('  ', ' ').replace('.','').replace(',','').replace(' RD RD',' RD')

                rows.updateRow(row)
    cleanAddresses()

    #-------------End Clean Addresses-----------
