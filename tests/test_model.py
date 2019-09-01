from MiScan.model import build_model
import unittest


class TestMiScanModel(unittest.TestCase):
    def test_model_structue(self):
        model = build_model()
        self.assertTupleEqual((None, 2), tuple2=model.output_shape)
