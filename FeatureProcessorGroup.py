import os

# Modify the path if FME is installed in another location
os.environ['FME_HOME'] = r"C:\Program Files\FME"

os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = str(1)

import fmebootstrap
import fme
import fmeobjects
from fmeobjects import FMEFeature



class FeatureProcessorGroup(object):

    def __init__(self):
        self.features = []

    def input(self, feature):
        self.features.append(feature)

    def close(self):
        pass

    def process_group(self):
        feature = fmeobjects.FMEFeature()
        feature.setAttribute("count", len(self.features))
        self.pyoutput(feature)
        self.features = []

    def has_support_for(self, support_type):
        return False

    def pyoutput(self, feature):
        pass



