# load feature into a feature class with SDE tolerances

import arcpy, time

def load2SDEtol(newParcelsFinalSDE, path, county, schema, newParcelsFinal, startTime):
    print('Creating FC with SDE tols and Load data')

    if arcpy.Exists(newParcelsFinalSDE):
        print(' Exists - Deleting', newParcelsFinalSDE)
        arcpy.Delete_management(newParcelsFinalSDE)

    print('Creating', newParcelsFinalSDE)
    arcpy.CreateFeatureclass_management(path + '\\BasicParcels_2020.gdb', county + '_Parcels_2020', "POLYGON", schema, "DISABLED", "DISABLED", schema)

    print('Appending to', newParcelsFinalSDE)
    arcpy.Append_management(newParcelsFinal, newParcelsFinalSDE, "NO_TEST",)
    count = int(arcpy.GetCount_management(newParcelsFinalSDE).getOutput(0)); print(str(count), 'features appended')

    # Repair Geometry - SDE Tol data
    print('Repairing Geometry -',newParcelsFinalSDE, 'with SDE Tolerance data')
    arcpy.RepairGeometry_management(newParcelsFinalSDE, "DELETE_NULL")

    stopTime3 = time.clock(); elapsedTime = stopTime3 - startTime; elapsedTime = elapsedTime / 60
    print('Time for operation:', str(round(elapsedTime, 1)), 'minutes')
