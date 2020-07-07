# asterisk explained -> http://gis.stackexchange.com/questions/57380/possible-to-add-multiple-fields-in-single-arcpy-statement

import arcpy


def addFields(newParcels):
    print(' *** Adding Fields')

    fields = [
        ('FIPS', 'DOUBLE'),
        ('PARCEL_ID', 'TEXT', '', '', '50'),
        ('ACCOUNT_NUM', 'TEXT', '', '', '50'),  # Unique to Kane
        ('PARCEL_ADD', 'TEXT', '', '', '60'),
        ('PARCEL_CITY', 'TEXT', '', '', '30'),
        ('PARCEL_ZIP', 'TEXT', '', '', '10'),
        ('OWN_TYPE', 'TEXT', '', '', '50'),
        ('OWNERNAME', 'TEXT', '', '', '100'),   # Unique to Utah
        ('RECORDER', 'TEXT', '', '', '50'),
        ('STRUCTURE', 'TEXT', '', '', '20'),
        ('OrigAddress', 'TEXT', '', '', '60'),
        ('PT_ADDRESS', 'TEXT', '', '', '60'),
        ('ParcelsCur', 'DATE', '', '', '', 'Parcels Current As Of'),
        ('ZONING', 'TEXT', '', '', '20'),       # Unique to Kane
        ('ParcelsRec', 'DATE', '', '', '', 'Parcels Received'),
        ('ParcelsPub', 'DATE', '', '', '', 'Parcels Published'),
        ('ParcelYear', 'TEXT', '', '', '5', 'Parcel Year'),
        ('ParcelNotes', 'TEXT', '', '', '50', 'Parcel Notes'),
        ('CoParcel_URL', 'TEXT', '', '', '100', 'County Parcel Website')
    ]

    arcpy.MakeFeatureLayer_management(newParcels, 'parFl')

    if arcpy.ListFields('parFl', 'OWNER'):
        arcpy.DeleteField_management('parFl', ['OWNER'])

    for field in fields:
        if not arcpy.ListFields('parFl', field[0]):
            arcpy.AddField_management(*('parFl',) + field)