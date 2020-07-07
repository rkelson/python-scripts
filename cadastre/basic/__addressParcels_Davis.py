# address aggregator and cleaner for Davis County

import arcpy
from sweeper import address_parser

def addressParcels_Davis(newParcels):

    #  CALC PARCEL_ADD & OrigAddress
    def calcAddress():
        print(' * Calculating Address Field')

        arcpy.AddField_management(newParcels, "Address", "TEXT", "", "", "50")
        #               0               1           2           3               4           5
        fields = ['ParcelSitu', 'ParcelSi_2', 'ParcelSi_3', 'ParcelSi_4', 'OrigAddress', 'Address']

        with arcpy.da.UpdateCursor(newParcels, fields) as rows:

            for row in rows:

                if row[0] == 0:
                    continue

                if row[0] is None: row[0] = ''
                if row[2] is None: row[2] = ''
                if row[3] is None: row[3] = ''

                parts = [str(row[0]), row[1], row[2], row[3]]

                row[4] = " ".join(parts)
                row[5] = " ".join(parts)
                row[5] = row[5].strip().replace("  ", " ").replace("  ", " ").replace("  ", " ")

                rows.updateRow(row)

        with arcpy.da.UpdateCursor(newParcels, ['Address', 'PARCEL_ADD', 'OrigAddress']) as rows:
            for row in rows:
                row[1] = row[0]
                row[2] = row[0]
                rows.updateRow(row)

    calcAddress()

    # Clean Addresses
    def cleanAddresses():
        print(' * Cleaning Addresses')

        def IsProblem(value):
            ex = ['NO.', 'ST. JOSEPH', 'SOUTH WEBER', 'NORTH LISA', 'SOUTH LISA', 'EAST LISA']
            return any(value.find(e) > -1 for e in ex)

        exp = "{0} <> '' AND {0} IS NOT NULL".format('PARCEL_ADD')
        print('Where Clause is', exp)

        with arcpy.da.UpdateCursor(newParcels, ['PARCEL_ADD', 'OrigAddress', 'OID@'], exp) as rows:

            for row in rows:

                if IsProblem(row[1]):

                    row[0] = row[1].replace('NO.', '').replace('ST. JOSEPH', 'ST JOSEPH')\
                        .replace('ROAD','RD').replace('LANE','LN').replace('DRIVE','DR').replace('STREET','ST').replace('CIRCLE', 'CIR')\
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
