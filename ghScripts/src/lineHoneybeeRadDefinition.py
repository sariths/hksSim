"""
Return Radiance Material definition based on an inputMaterial name

    Args:
        _matName: Name of the material. This name should already exist in the
            Honeybee Radiance Material Library.
    Returns:
        radDef: The Radiance definition for the specified material name.
"""
ghenv.Component.Name = "LINE_Honeybee_Rad Definition"
ghenv.Component.NickName = 'lineHoneybeeRadDefinition'
ghenv.Component.Message = 'VER 0.0.01\nNOV_27_2017'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "MISC"
ghenv.Component.SubCategory = "LINE"

try:
    ghenv.Component.AdditionalHelpFromDocStrings = "1"
except:
    pass

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
        msg = "'%s' was not found in the list of defined materials" % _matName
        raise Exception(msg)
    return material


if __name__ == "__main__" and _matName:
    radDef = main(_matName)