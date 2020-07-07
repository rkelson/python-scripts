# address cleaner for Beaver County

import arcpy
from sweeper import address_parser

def addressParcels_Beaver(newParcels, parcelAddrFld):

    print(' ** Getting addresses from Parcels')

    #  CALC PARCEL_ADD & OrigAddress
    def calcAddress():
        print(' ** Calculating OrigAddress')
        with arcpy.da.UpdateCursor(newParcels, ['OrigAddress', parcelAddrFld]) as rows:

            for row in rows:

                if row[1] != None and row[1][0].isdigit():

                    row[0] = row[1].upper().strip().replace('  ',' ')     #OrigAddress

                rows.updateRow(row)
    calcAddress()

    # Clean Addresses
    def cleanAddresses():
        print(' * Cleaning Addresses')

        def SkipName(value):
            skipNameList = ['NORTH CREEK']
            return any(value.find(e) > -1 for e in skipNameList)

        exp = "{0} <> '' AND {0} IS NOT NULL".format('OrigAddress')
        print('Where Clause is', exp)

        with arcpy.da.UpdateCursor(newParcels, ['PARCEL_ADD', 'OrigAddress', 'OID@'], exp) as rows:

            for row in rows:

                if SkipName(row[1]):

                    row[0] = row[1].replace("ROAD","RD").replace("LANE","LN").replace("DRIVE","DR").replace("STREET","ST").replace("CIRCLE", "CIR")\
                        .strip().upper().replace("  "," ")

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
