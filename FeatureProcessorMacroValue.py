import os

# Modify the path if FME is installed in another location
os.environ['FME_HOME'] = r"C:\Program Files\FME"

os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = str(1)

import fmebootstrap
import fme
import fmeobjects
from fmeobjects import FMEFeature

class FeatureProcessorMacroValue(object):

    def __init__(self):
        self.fooValue = fme.macroValues["foo"]

    def input(self, feature):
        feature.setAttribute("foo", self.fooValue)
        self.pyoutput(feature)

    def close(self):
        pass

    def process_group(self):
        pass

    def has_support_for(self, support_type):
        return False

    def pyoutput(self, feature):
        pass



