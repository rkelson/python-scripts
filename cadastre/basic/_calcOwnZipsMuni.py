#

import arcpy


def calcOwnZipsMuni(newParcelsFinal, county):

    print('Calculating Own_Type, Zip & Mini')

    cityField = 'NAME_1'

    if county in ('Duchesne', 'Summit'):
        cityField = 'NAME_12_13'

    if county == ('Juab'):
        cityField = 'NAME_12_13_14_15'

    with arcpy.da.UpdateCursor(newParcelsFinal, ['OWN_TYPE', 'PARCEL_ZIP', 'PARCEL_CITY', 'OWNER', 'ZIP5', cityField]) as rows:

        for row in rows:

            row[0] = row[3]
            row[1] = row[4]
            row[2] = row[5]

            rows.updateRow(row)