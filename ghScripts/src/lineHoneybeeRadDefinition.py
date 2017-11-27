"""
Return Radiance Material definition based on an inputMaterial name

    Args:
        _matName: Name of the material. This name should already exist in the
            Honeybee Radiance Material Library.
    Returns:
        matInHB: Lists all the materials available in the Honeybee database.
        radDef: The Radiance definition for the specified material name.
"""
ghenv.Component.Name = "LINE_Honeybee_Rad Definition"
ghenv.Component.NickName = 'lineHoneybeeRadDefinition'
ghenv.Component.Message = 'VER 0.0.01\nNOV_27_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "MISC"
ghenv.Component.SubCategory = "LINE"
#compatibleHBVersion = VER 0.0.56\nDEC_21_2015
#compatibleLBVersion = VER 0.0.59\nFEB_01_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import scriptcontext as sc
import Grasshopper.Kernel as gh



def main(_matName):
    if not sc.sticky.has_key('honeybee_release'):
        print "You should first let Honeybee fly..."
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, "You should first let Honeybee fly...")
        raise Exception("You should first let Honeybee fly...")

    matDict = dict(sc.sticky['honeybee_RADMaterialLib'])

    try:
        material = matDict[_matName]
    except:
         msg = "'%s' was not found in the list of defined materials."%_matName
         msg+="\nCheck the 'matInHB' output to see the list of available materials"
         w = gh.GH_RuntimeMessageLevel.Warning
         ghenv.Component.AddRuntimeMessage(w, msg)
         return None
    return material


if __name__ =="__main__" and _matName:
    matDict = dict(sc.sticky['honeybee_RADMaterialLib'])
    matInHB="\n".join(sorted(matDict.keys()))
    radDef = main(_matName)