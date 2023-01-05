import os


from FmePytonCaller import FmePythonCaller

# Modify the path if FME is installed in another location
os.environ['FME_HOME'] = r"C:\Program Files\FME"
os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = str(1)

import fmebootstrap
import fme

import fmeobjects
from fmeobjects import FMEFeature, FMELine, FMEArea, FMEPoint, FMEMultiPoint, FMEPolygon
from FeatureProcessor import FeatureProcessor
from FeatureProcessorGroup import FeatureProcessorGroup
from FeatureProcessorMacroValue import FeatureProcessorMacroValue

from unittest import main, TestCase


class TestFeatureProcessor(TestCase):
    def setUp(self) -> None:
        pass

    def test_feature_Attribute(self):
        fme.macroValues["foo"] = "bar"
        f = FMEFeature()
        f.setGeometry(fmeobjects.FMELine())
        f.setAttribute('foo', 'bar')
        f.addCoordinate(1, 2)
        out = FmePythonCaller(FeatureProcessor).input(f)

        for i, a in enumerate(out):
            with self.subTest("Has attribute:", item=i):
                self.assertEqual(a.getAttribute('foo'), 'bar')
        self.assertEqual(1, len(out))

    def test_feature_FMELine(self):
        f = FMEFeature()
        f.setGeometry(fmeobjects.FMELine())
        f.setAttribute('foo', 'bar')
        f.addCoordinate(1, 2)
        f.addCoordinate(5, -3)
        f.addCoordinate(15, 13)
        f.addCoordinate(16, 7)
        out = FmePythonCaller(FeatureProcessor).input(f)

        for i,a in enumerate(out):
            with self.subTest("Point:", item=i):
                self.assertEqual(a.getAttribute('foo'), 'bar')
                self.assertIsInstance(a.getGeometry(), fmeobjects.FMEPoint)
        self.assertEqual(4, len(out))

    def test_feature_FMEPolygon(self):
        boundary = fmeobjects.FMELine([(10, 10), (10, 20), (20, 10), (20, 20)])
        f = FMEFeature()
        f.setGeometry(fmeobjects.FMEPolygon(boundary))
        f.setAttribute('foo', 'bar')
        out = FmePythonCaller(FeatureProcessor).input(f)
        for i, a in enumerate(out):
            with self.subTest("Point:", item=i):
                self.assertIsInstance(a.getGeometry(), fmeobjects.FMEPoint)

        self.assertEqual(4, len(out))

    def test_feature_FMEPolygonAndPoint(self):
        boundary = fmeobjects.FMELine([(10, 10), (10, 20), (20, 20)])
        f = FMEFeature()
        f.setGeometry(fmeobjects.FMEPolygon(boundary))

        f2 = FMEFeature()
        f2.setGeometry(fmeobjects.FMEPoint(10, 30))
        out = FmePythonCaller(FeatureProcessor).input(f, f2)

        for i, a in enumerate(out):
            with self.subTest("Point:", item=i):
                self.assertIsInstance(a.getGeometry(), fmeobjects.FMEPoint)
        self.assertEqual(4, len(out))

    def test_feature_GroupBy(self):
        f1 = FMEFeature()

        f1.setAttribute('foo', 'bar')
        f1.setAttribute('foo2', 'bar')
        f1.addCoordinate(1, 2)
        f2 = FMEFeature()
        f2.setAttribute('foo', 'mu')
        f2.setAttribute('foo2', 'mu1')
        f2.addCoordinate(1, 2)
        f3 = FMEFeature()
        f3.setAttribute('foo', 'mu')
        f3.setAttribute('foo2', 'mu')
        f3.addCoordinate(1, 2)
        f4 = FMEFeature()
        f4.setAttribute('foo', 'bar')
        f4.setAttribute('foo2', 'bar')
        f4.addCoordinate(1, 2)

        out = FmePythonCaller(FeatureProcessorGroup).input(f1, f2, f3, f4, groupBy=['foo', 'foo2'])

        self.assertEqual(3, len(out))

    def test_feature_Macro_Values(self):
        features = []
        fme.macroValues["foo"] = "bar"
        for i in range(10):
            features.append(FMEFeature())

        out = FmePythonCaller(FeatureProcessorMacroValue).input(features)
        for i, a in enumerate(out):
            with self.subTest("Should have attribute with value bar:", item=i):
                self.assertEqual(a.getAttribute("foo"), "bar")

        self.assertEqual(10, len(out))








