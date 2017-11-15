"""Contains a function that will consolidate geometry files from a honeybee project."""


import os
import logging
import shutil
import glob


logger = logging.getLogger("__main__")
logger.setLevel(logging.DEBUG)
logging.basicConfig(format="%(asctime)s|%(message)s")

def consolidateGeometry(projectDirectory,destinationDirectory,runDaylightDir='unnamed',mainMaterialFile='material_unnamed.rad',
                        mainGeometryFile='unnamed.rad',overWrite=False,copyPointsFiles=True,splitMainGeometryFile=True):
    """
    Consolidate a Honeybee daylighting simulation with breps, meshes etc into a single directory.

    :param projectDirectory: Directory containing the honeybee project.
    :param destinationDirectory: Directory, preferably empty, to which the files should be consolidated to.
    :param runDaylightDir: This is the subdirectory within the "projectDirectory" which contains brep geometry, points files
        etc. Defaults to 'unnamed'..specify a different value if the folder isn't called unnamed.
    :param mainMaterialFile:
    :param mainGeometryFile:
    :param overWrite:
    :return:
    """

    assert projectDirectory !=destinationDirectory,\
        'Project directory(%s) and Destination directory (%s) cannot be same.'%(projectDirectory,destinationDirectory)


    if os.listdir(destinationDirectory) and not overWrite:
        raise Exception("The destination directory %s is not empty. Set the variable 'overWrite' to True to transfer files"
                        " into this directory nevertheless."%destinationDirectory)

    #This will likely be gridBasedSimulation, imageBasedSimulation or something similar.
    simDirectory = os.listdir(os.path.join(projectDirectory,runDaylightDir))[0]

    logging.warning("The simulation is %s\n"%(simDirectory))

    mainGeometryFileFullpath = os.path.join(projectDirectory,runDaylightDir,simDirectory,mainGeometryFile)
    mainMaterialFileFullPath= os.path.join(projectDirectory,runDaylightDir,simDirectory,mainMaterialFile)

    assert os.path.exists(mainGeometryFileFullpath),'The geometry file %s was not found.'%mainGeometryFileFullpath
    assert os.path.exists(mainMaterialFileFullPath),'The materials file %s was not found.'%mainMaterialFileFullPath

    projectDirs = os.listdir(projectDirectory)

    #sanity check
    assert runDaylightDir in projectDirs,\
        'The directory %s was not found %s'%(runDaylightDir,projectDirectory)

    materialsList = []
    geometryList = []

    for dr in projectDirs:
        fullPath=os.path.join(projectDirectory,dr)
        if os.path.isdir(fullPath) and dr != runDaylightDir:
            if 'MSH2RADFiles' in os.listdir(fullPath):
                logging.warning("Processing mesh-object %s"%dr)

                try:
                    matList = glob.glob(os.path.join(fullPath, 'MSH2RADFiles', "material*.rad"))
                    geoList  = glob.glob(os.path.join(fullPath, 'MSH2RADFiles', "%s*.rad" % dr))
                    assert matList and len(matList)==1
                    assert geoList and len(geoList)==1
                    materialsList.append(matList[0])
                    geometryList.append(geoList[0])
                except AssertionError:
                    logging.warning("Error occured in %s"%fullPath)
            else:
                logging.warning("MSH2RAD directory was not found in %s"%fullPath)




    mainGeomDict={}

    # for files in materialsList:
    #     with open(files) as someFile:
    #         print(" ".join(someFile.read().split()))


if __name__ == "__main__":
    consolidateGeometry(r'C:\Users\ssubramaniam\Projects\SFO\09202017',r'C:\Users\ssubramaniam\Projects\SFO\a')