#

import arcpy

def calcBaseAttributes(newParcels, parcelFld, fips, recorder, url, county, coUpdate):

    print(' ** Calculating FIPS, RECORDER, URL, PARCEL_ID, STRUCTURE & CURRENCY')
#                                              0       1           2               3           4           5           6
    with arcpy.da.UpdateCursor(newParcels, ['FIPS', 'RECORDER', 'CoParcel_URL', 'PARCEL_ID', parcelFld, 'STRUCTURE']) as rows:

        for row in rows:

            row[0] = fips
            row[1] = recorder
            row[2] = url

            if not row[0] in ('49001', '49033'):

                row[5] = 'Unknown'

            if not parcelFld in ('parcel_id', 'Parcel_ID', 'PARCEL_ID'):
                row[3] = row[4]

            rows.updateRow(row)

##    print(' *** Calculating STRUCTURE')
##    with arcpy.da.UpdateCursor(newParcels, ['FIPS', 'STRUCTURE']) as rows:
##        for row in rows:
##
##            if row[0] in ('49033'):
##
##                continue
##
##            else:
##                row[5] = 'Unknown'
##
##            rows.updateRow(row)

## CURRENCY Fields
    co = county.title()

    if co == 'Boxelder':
        co = 'Box Elder'

    if co == 'Saltlake':
        co = 'Salt Lake'

    if co == 'Sanjuan':
        co = 'San Juan'

    print(co, 'County ** Calculating Currency Fields')

    exp = "{0} = '{1}'".format('NAME', co)

    with arcpy.da.SearchCursor(coUpdate, ['ParcelsCur', 'ParcelsRec', 'ParcelsPub', 'ParcelYear', 'ParcelNotes'], exp) as srows:
        for srow in srows:

            with arcpy.da.UpdateCursor(newParcels, ['ParcelsCur', 'ParcelsRec', 'ParcelsPub', 'ParcelYear', 'ParcelNotes']) as urows:
                for urow in urows:

                    urow[0] = srow[0]
                    urow[1] = srow[1]
                    urow[2] = srow[2]
                    urow[3] = srow[3]
                    urow[4] = srow[4]
                    urows.updateRow(urow)