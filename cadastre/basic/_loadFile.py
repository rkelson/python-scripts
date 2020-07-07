# Write lines to Copy features into SDE

import os

def loadFile(coPath, county, sgid, sgidfc, newParcelsFinalSDE):

    loadFile = coPath + '\\' + county.title() + '_LOAD.txt'

    with open(loadFile, 'w') as file:

        file.write('       *** ! UPDATE ! *** \n')
        file.write('\n')
        file.write('     * ArcCatalog Metadata \n')
        file.write('     * SGID Changelog \n')
        file.write('     * Webpage \n')
        file.write('\n')
        file.write('------------------- Python 3 ------------------- \n')
        file.write('\n')
        file.write('import arcpy \n')
        file.write('''arcpy.TruncateTable_management(r"''' + sgidfc + '''")''' + '\n')
        file.write('''arcpy.Append_management(r"''' + newParcelsFinalSDE + '''",r''' + '''"''' + sgidfc + '''",''' + '''"NO_TEST")''' + '\n')
        file.write('''arcpy.GetCount_management(r"''' + sgidfc + '''")''' + '\n')
        file.write('\n')
        file.write('\n')
        file.write(r'*** Run Geometry Fixer from: (arcgispro-py3) L:\agrc\users\rkelson\Cadastre>' +'\n')
        file.write('\n')
        file.write(r'python fix_corrupt_geometry_Py3.py ' + sgid + 'Cadastre.sde\SGID.CADASTRE.Parcels_' + county.title() + '''''' + '\n')
        file.write('\n')
        file.write('*** If problems are found delete the OIDs *** \n')
        file.write('\n')
        file.write('\n')
        file.write(r'*** Run Sweeper from: (arcgispro-py3) L:\agrc\users\rkelson\Cadastre>' +'\n')
        file.write('\n')
        file.write('activate sweeper \n')
        file.write(r'python -m sweeper sweep --workspace=' + sgid + 'Cadastre.sde --try-fix --save-report=C:\\Temp --table-name=CADASTRE.Parcels_' + county.title() + '''''' + '\n')
        file.write('deactivate sweeper \n')

##        file.write(r'     * Update Drive: python zip_loader.py "Database Connections\\SGID.sde" --feature "SGID.CADASTRE.Parcels_' + county.title() + '''"''' + '\n')
##        file.write('\n')

    os.startfile(loadFile)

    print('   *************** Success  ******************* ')