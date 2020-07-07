# address cleaner for Utah County

import arcpy
from agrc import parse_address

def addressParcels_Iron(newParcels):

    print(' ** Getting addresses from Parcels')

    #  CALC PARCEL_ADD & OrigAddress
    def calcAddress():
        print(' ** Calculating PARCEL_ADD & OrigAddress')
        with arcpy.da.UpdateCursor(newParcels, ['PARCEL_ADD', "OrigAddress", 'SITUS']) as rows:
            for row in rows:

                if row[2] != None:
                    if row[2].find(';;;') > -1: #True
                        row[0] = row[2].split(';;;')[0].strip().replace('   ', ' ').replace('  ', ' ') #PARCEL_ADD
                        row[1] = row[2].split(';;;')[0].strip().replace('   ', ' ').replace('  ', ' ') #OrigAddress

                    else:
                        row[0] = row[2].strip().replace('   ', ' ').replace('  ', ' ')    #PARCEL_ADD
                        row[1] = row[2].strip().replace('   ', ' ').replace('  ', ' ')    #OrigAddress

                rows.updateRow(row)
    calcAddress()

    # Clean Addresses
    def cleanAddresses():
        print(' * Cleaning Addresses')
        # might need some additions
        def NullOrEmpty(value):
            if value is None:
                return True

            value = value.strip()
            return len(value) < 1

        def NotNumericAddress(value):
            if not value[0].isdigit():
                return True

        def DirWType(value):
            ex1 = ['NORTH CIR', 'SOUTH CIR', 'EAST CIR', 'WEST CIR']
            return any(value.find(e) > -1 for e in ex1)

        def IsApartment(value):
            ex2 = ['#', '&', '-', 'UNIT', 'BLDG', '/', 'TRLR']
            return any(value.find(e) > -1 for e in ex2)

        def IsHWY(value):
            ex3 = ['HWY', 'HIGHWAY', ' CR ', 'COUNTY ROAD', ' SR ', 'STATE ROAD', 'STATE ROUTE', 'US HIGHWAY', 'U.S. HIGHWAY', 'UTAH STATE HIGHWAY', 'STATE HIGHWAY']
            return any(value.find(e) > -1 for e in ex3)

        def HasAliasStreet(value):
            return value.find('(') > -1

        def SkipName(value):
            skipNameList = skipNameList = ['E BLUE SKY DR N', 'N BLUE SKY DR E', 'E BLUE SKY DR S',
            'N CLARK PKWY N', 'W CLARK PKWY N', 'S COVE DR', 'CEDAR KNOLLS WEST', 'CEDAR KNOLLS SOUTH',
            'NORTH CEDAR', 'SOUTH ARTIFACT', 'CENTER'] # Iron HAS ';;;' in many addrsses
            return any(value.find(e) > -1 for e in skipNameList)

        with arcpy.da.UpdateCursor(newParcels,['PARCEL_ADD', 'OrigAddress']) as rows:

            for row in rows:
                if NullOrEmpty(row[1]):
                    continue

                if NotNumericAddress(row[1]):
                    row[0] = ""

                if DirWType(row[1]):
                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")

                if IsApartment(row[1]):
                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")
                    row[0] = row[1].replace(" NORTH"," N").replace(" SOUTH"," S").replace(" EAST"," E").replace(" WEST"," W")
                    row[0] = row[1].replace(" WY "," WAY ").replace(" BOULEVARD "," BLVD ").replace(" AV "," AVE ").replace(" CI "," CIR ").replace(" COVE "," CV ").replace(" LA "," LN ")

                if IsHWY(row[1]):
                    row[0] = row[1].replace(" COUNTY ROAD ", " CR ")
                    row[0] = row[1].replace(" STATE ROAD ", " SR ")
                    row[0] = row[1].replace(" STATE ROUTE ", " HWY ")
                    row[0] = row[1].replace(" US HIGHWAY ", " HWY ")
                    row[0] = row[1].replace(" U.S. HIGHWAY ", " HWY ")
                    row[0] = row[1].replace(" UTAH STATE HIGHWAY ", " HWY ")
                    row[0] = row[1].replace(" STATE HIGHWAY ", " HWY ")
                    row[0] = row[1].replace(" HIGHWAY ", " HWY ")
                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")
                    row[0] = row[1].strip().upper().replace("  "," ")

                if HasAliasStreet(row[1]):
                    row[0] = row[1].replace(" NORTH "," N ").replace(" SOUTH "," S ").replace(" EAST "," E ").replace(" WEST "," W ")
                    row[0] = row[1].replace("ROAD","RD").replace("LANE","LN").replace("DRIVE","DR").replace("STREET","ST")
                    row[0] = row[1].strip().upper().replace("  "," ")

                if SkipName(row[1]):
                    row[0] = row[1].replace(" WEST CEDAR KNOLLS SOUTH"," W CEDAR KNOLLS SOUTH").replace(" SOUTH CEDAR KNOLLS WEST"," S CEDAR KNOLLS WEST")
                    row[0] = row[1].replace(" EAST CENTER", " E CENTER").replace(" WEST CENTER", " W CENTER").replace(" NORTH CENTER", " N CENTER").replace(" SOUTH CENTER", " S CENTER")
                    row[0] = row[1].replace("ROAD","RD").replace("LANE","LN").replace("DRIVE","DR").replace("STREET","ST")
                    row[0] = row[1].strip().upper().replace("  "," ")

                if not (NullOrEmpty(row[1]) or NotNumericAddress(row[1]) or DirWType(row[1]) or IsApartment(row[1]) or IsHWY(row[1]) or HasAliasStreet(row[1]) or SkipName(row[1])):
                    address = parse_address.parse(row[1])
                    row[0] = address.normalizedAddressString

                else:
                    row[0] = row[0].upper()

                row[0] = row[0].strip().upper().replace("  "," ").replace(".","").replace(",","").replace(" RD RD"," RD")
                rows.updateRow(row)

    cleanAddresses()
    #-------------End Clean Addresses-----------
