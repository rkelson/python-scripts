
import arcpy, os, shutil, time, urllib.request

# new paths using Share
url = r'http://maps.utahcounty.gov/data4export/TaxParcels_FileGeo.zip'
filename = 'TaxParcels_FileGeo.zip'
share = r'L:\agrc\users\rkelson\Cadastre\Basic\2020\Utah\TaxParcels_FileGeo.zip'
gdb = r'L:\agrc\users\rkelson\Cadastre\Basic\2020\Utah\TaxParcels.gdb'
outDir = gdb[:-15]

def downloadUtahCo():

    if not os.path.exists(r'L:\agrc\users\rkelson\Cadastre\Basic\2020\Utah'):
        os.mkdir(r'L:\agrc\users\rkelson\Cadastre\Basic\2020\Utah')

    if os.path.exists(share):
        print('Exists share, Deleting')
        os.remove(share)

    print('* Downloading file')
    with urllib.request.urlopen(url) as response, open(share, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    time.sleep(35)

    print('** Unzipping file')
    if arcpy.Exists(gdb):
        shutil.rmtree(gdb)

    os.chdir(outDir)
    os.system('7z x ' + share)

    print('*** Finished copying file ***')



# Old local paths
##url = r'http://maps.utahcounty.gov/data4export/TaxParcels_FileGeo.zip'
##filename = 'TaxParcels_FileGeo.zip'
##local = r'E:\Cadastral\Basic\2020\Utah\TaxParcels_FileGeo.zip'
##gdb = r'E:\Cadastral\Basic\2020\Utah\TaxParcels.gdb'
##outDir = gdb[:-15]