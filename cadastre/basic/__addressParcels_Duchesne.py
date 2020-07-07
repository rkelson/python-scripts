# address cleaner for Utah County

import arcpy
from agrc import parse_address

def addressParcels_Duchesne(newParcels):

    print(' ** Getting addresses from Parcels')

    #  CALC PARCEL_ADD & OrigAddress
    def calcAddress():
        print(' ** Calculating PARCEL_ADD & OrigAddress')
        with arcpy.da.UpdateCursor(newParcels, ['PARCEL_ADD', "OrigAddress", 'PROPERTY_A']) as rows:

              for row in rows:

                    row[0] = row[2]     #PARCEL_ADD
                    row[1] = row[2]     #OrigAddress
                    rows.updateRow(row)

    calcAddress()

    # Clean Addresses
    def cleanAddresses():
        print(' * Cleaning Addresses')

        def NullOrEmpty(value):
            if value is None:
                return True

            value = value.strip()
            return len(value) < 1

        def NotNumericAddress(value):
            if not value[0].isdigit():
                return True

        with arcpy.da.UpdateCursor(newParcels,['PARCEL_ADD']) as rows:

            for row in rows:
                if NullOrEmpty(row[0]):
                    continue

                if NotNumericAddress(row[0]):
                    row[0] = ""

                else:
                    address = parse_address.parse(row[0])
                    row[0] = address.normalizedAddressString

                row[0] = row[0].strip().upper().replace("  "," ").replace(".","")

                rows.updateRow(row)
    cleanAddresses()
    #-------------End Clean Addresses-----------
