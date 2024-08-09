from unittest import TestCase

from ddt import data
from ddt import ddt

from quantmsio.core.feature_in_memory import FeatureInMemory
from quantmsio.core.feature import FeatureHandler
from quantmsio.tests.common import datafile


@ddt
class TestFeatureHandler(TestCase):
    global test_datas
    test_datas = [
        (
            "DDA-plex/MSV000079033.mzTab",
            "DDA-plex/MSV000079033_msstats_in.csv",
            "DDA-plex/MSV000079033-Blood-Plasma-iTRAQ.sdrf.tsv",
            "ITRAQ4",
        ),
    ]

    @data(*test_datas)
    def test_convert_mztab_msstats_to_feature(self, test_data):
        mztab_file = datafile(test_data[0])
        msstats_file = datafile(test_data[1])
        sdrf_file = datafile(test_data[2])
        expertment_type = test_data[3]
        f = FeatureHandler()
        feature_manager = FeatureInMemory(expertment_type, f.schema)
        for _ in feature_manager.merge_mztab_and_sdrf_to_msstats_in(
            mztab_path=mztab_file, msstats_path=msstats_file, sdrf_path=sdrf_file
        ):
            print("ok")
