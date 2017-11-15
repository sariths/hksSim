
from __future__ import print_function
from __future__ import division

import logging
logger = logging.getLogger("__main__")
logging.basicConfig(format='%(asctime)s -%(levelname)s module:%(module)s function:%(funcName)s message--%(message)s')





import sys as sys
import operator as _op
from pts import RoomGrid as _rmgrd
import warnings



class Illarr(object):

    def __init__(self,illarr,roomgrid,vector=[0,0,1]):
        """
            This class is a definition of the illuminance profile of a room/space.
            To be constructed, it needs illvalues and a corresponding points grid.
            Notes to self: Don't create zone inside this...create zone outside..
        """
        self.illarr = self.createIllArr(illarr)
        self.roomgrid = roomgrid




    def createIllArr(self,illarr):
        fileContainsText=False
        try:
            # If a pts file is not provided assume that this is a zone ill file.
            # So read value into an array.
            #Update 7th Sep 2016: Added a functionality where illuminance files containing
            # headers, like the ones produced by rmtxop, can also be read.
            with open(illarr)as illfile:
                illarr = []
                for lines in illfile:
                    lineSplit = lines.strip().split()
                    if lineSplit:
                        try:
                            illarr.append(float(lineSplit[-1]))
                        except ValueError:
                            fileContainsText = True
        except:
            illarr = illarr

        if fileContainsText:
            msg = "\nThe file contains text in addition to numbers. The size of the number" \
                  "array is %s" % (len(illarr))
            warnings.warn(msg)

        return illarr

    def __add__(self, other):
        """
            Operator overloading for addition
            Addition of two illarrays results in the creation of a newillarry with the added illuminance
            Addition shouldn't be allowed to mutate an existing zone.
            So, any addition, subtraction multiplication etc. should return a new Illarr.
        """
        try:

            self.illarr = map(_op.add,self.illarr,other.illarr)

        except:
            print(sys.exc_info())
        return self

    def __sub__(self, other):
        """
            Operator overloading for addition
            Addition of two illarrays results in the creation of a newillarry with the
            added illuminance
        """
        try:
            self.illarr = map(_op.sub,self.illarr,other.illarr)
        except:
            print(sys.exc_info())

        return self

    def __mul__(self, other):
        """
            Operator overloading for multiplication
            Multiply illuminance values with a scalar quantity.
        """
        try:
           self.illarr = map(_op.mul,self.illarr,[other]*len(self.illarr))
        except:
            print(sys.exc_info())

        return self


    @property
    def max_ill(self):
        maxval = max(self.illarr)
        maxpts = [idx for idx,val in enumerate(self.illarr) if val==maxval]
        maxpts = [ self.roomgrid.ptsdict[pt].ptid for pt in maxpts ]
        return {'max_ill':maxval,"points":maxpts}

    @property
    def min_ill(self):
        minval = min(self.illarr)
        minpts = [idx for idx,val in enumerate(self.illarr) if val==minval]
        minpts = [ self.roomgrid.ptsdict[pt].ptid for pt in minpts ]
        return {'min_ill':minval,"points":minpts}

    @property
    def summary(self):
        try:
            ave_val = sum(self.illarr)/len(self.illarr)
            ave_max = ave_val/self.max_ill['max_ill']
            ave_min = ave_val/self.min_ill['min_ill']
            max_min = ave_min/ave_max
            return {"av_ill":round(ave_val,2),"av_ill/max":round(ave_max,2),"av_ill/min":round(ave_min,2),"max/min":round(max_min,2)}
        except ZeroDivisionError:
            return {"av_ill":0,"av_ill/max":None,"av_ill/min":None,"max/min":None}


    def filterill(self,upper=None,lower=None,listpts=False,verbose=True,percent=False):
        """
            If only upper is provided then list all points equal to and above upper
            If only lower is provided then list all points equal to and below lower
            If upper and lower are provided list all points within that range.
            if listpts is True then list all the points for that particular option.
        """
        if not upper and not lower:
            raise  Exception("No upper and lower values were specified for filtering illuminance values")

        if upper and not lower:

            pts = [{'ptid': self.roomgrid.ptsdict[idx].ptid,'illval':illval,'ptobj':self.roomgrid.ptsdict[idx]} for idx,illval in enumerate(self.illarr) if illval>=upper]
            ptsnum = len(pts)
            if verbose:
                if listpts:
                    return {"Number of pts, out of a total {} pts, that are greater than or equal to {}".format(len(self.illarr),upper):ptsnum,"List of points":pts}
                else:
                    return {"Number of pts, out of a total {} pts, that are greater than or equal to {}".format(len(self.illarr),upper):ptsnum}
            elif percent:
                return round(ptsnum/len(self.illarr),3)
            else:
                return ptsnum

        if not upper and lower:

            pts = [{'ptid': self.roomgrid.ptsdict[idx].ptid,'illval':illval,'ptobj':self.roomgrid.ptsdict[idx]} for idx,illval in enumerate(self.illarr) if illval<=lower]
            ptsnum = len(pts)

            if verbose:
                if listpts:
                    return {"Number of pts, out of a total {} pts, that are lower than or equal to {}".format(len(self.illarr),lower):ptsnum,"List of points":pts}
                else:
                    return {"Number of pts, out of a total {} pts, that are lower than or equal to {}".format(len(self.illarr),lower):ptsnum}
            elif percent:
                return round(ptsnum/len(self.illarr),3)
            else:
                return ptsnum

        if upper and lower:

            pts = [{'ptid': self.roomgrid.ptsdict[idx].ptid,'illval':illval,'ptobj':self.roomgrid.ptsdict[idx]} for idx,illval in enumerate(self.illarr) if illval>=lower and illval<=upper]
            ptsnum = len(pts)

            if verbose:
                if listpts:
                    return {"Number of pts, out of a total {} pts, that between {} and {}".format(len(self.illarr),upper,lower):ptsnum,"List of points":pts}
                else:
                    return {"Number of pts, out of a total {} pts, that between {} and {}".format(len(self.illarr),upper,lower):ptsnum}
            elif percent:
                return round(ptsnum/len(self.illarr),3)
            else:
                return ptsnum

class Zoneill(Illarr):
    """This class can be used to read Data from electric zones and also data from
    daylight rtrace results that contain pts info.."""

    def __init__(self,zonefile):
        self.roomgrid = _rmgrd(zonefile)
        Illarr.__init__(self,zonefile,self.roomgrid)



if __name__ ==  '__main__':
    pass
