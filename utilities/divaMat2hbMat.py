# coding=utf-8
import os

def makeHBmatFromDivaMat(divaFile, hbMatFileName='HoneybeeRadMaterials.mat'):
    """
    Take a DIVA material file and write a Honeybee-friendly material database. The written file needs to be placed
    inside the Ladybug root folder...Usually c:\ladybug.
    :param divaFile: File path for the diva material file.
    :param hbMatFileName: File path to which the Honeybee-friendly radiance materials should be written to.
    :return:
    """
    assert os.path.exists(divaFile),'The Diva materials file (%s) was not found.'%divaFile

    hbStr = ""
    commentCount=0
    with open(divaFile) as divaData:
        for lines in divaData:
            lines=lines.strip()
            if lines:
                if lines.startswith("#"):
                    commentCount+=1
                else:
                    if commentCount>0:
                        hbStr+='\n'
                        commentCount=0
                    hbStr+="%s\n"%lines

    with open(hbMatFileName,'w') as writeMatData:
        writeMatData.write(hbStr)

if __name__ == "__main__":
    makeHBmatFromDivaMat(r'C:\Users\ssubramaniam\Documents\My Received Files\HoneybeeRadMaterials.mat')