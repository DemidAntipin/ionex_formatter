import pytest
import json
import os

from ionex_formatter.ionex_format import (
    IonexHeader_V_1_1,
    FormatDescriptionLabelMissing
)

class TestIoneHeaderFormat:

    def test_init(self):
        header_format = IonexHeader_V_1_1()
        header_format2 = IonexHeader_V_1_1()
        auto_labels = [
            "PGM / RUN BY / DATE",
            "DESCRIPTION",
            "COMMENT",
            "INTERVAL",
            "# OF MAPS IN FILE",
            "MAPPING FUNCTION",
            "ELEVATION CUTOFF",
            "OBSERVABLES USED",
            "# OF STATIONS",
            "# OF SATELLITES",
            "SYS / # STA / # SAT",
            "BASE RADIUS",
            "MAP DIMENSION",
            "HGT1 / HGT2 / DHGT",
            "LAT1 / LAT2 / DLAT",
            "LON1 / LON2 / DLON",
            "EXPONENT",
            "START OF AUX DATA",
            "END OF AUX DATA",
            "START OF TEC MAP",
            "LAT/LON1/LON2/DLON/H",
            "END OF TEC MAP",
            "START OF RMS MAP",
            "END OF RMS MAP",
            "START OF HEIGHT MAP",
            "END OF HEIGHT MAP",
        ]
        auto_labels.sort()
        header_format._update()
        header_format.line_tokens("EXPONENT")
        assert auto_labels == header_format.AUTO_FORMATTED_LABELS

    def test_label_description_is_missing(self, tmp_path):
        with open("ionex_formatter/header_line_descriptions.json", "r") as f:
            corrupted_descrition = json.load(f)
        del corrupted_descrition["COMMENT"]
        corrupted_descrition_path = tmp_path / "corrupted_descriptions.json"
        with open(corrupted_descrition_path, "w") as f:
            corrupted_descrition = json.dump(corrupted_descrition, f)
        header = IonexHeader_V_1_1()
        with pytest.raises(FormatDescriptionLabelMissing):
            header.init_fields(corrupted_descrition_path)
        with pytest.raises(FileNotFoundError):
            header.init_fields('./data_samples/ionex_header.txt')

    def test_label_worng_value_type(self, tmp_path):
        with open("ionex_formatter/header_line_descriptions.json", "r") as f:
            corrupted_descrition = json.load(f)
        with open("ionex_formatter/corrupt.json", "r") as f:
            corrupted_descrition2 = json.load(f)
        corrupted_descrition["COMMENT"] = 123
        corrupted_descrition_path = tmp_path / "corrupted_descriptions.json"
        corrupted_descrition_path2 = tmp_path / "corrupted_descriptions2.json"
        with open(corrupted_descrition_path, "w") as f:
            corrupted_descrition = json.dump(corrupted_descrition, f)
        with open(corrupted_descrition_path2, "w") as f:
            corrupted_descrition2 = json.dump(corrupted_descrition2, f)
        header = IonexHeader_V_1_1()
        header2 = IonexHeader_V_1_1()
        with pytest.raises(TypeError):
            header.load_descriptions(corrupted_descrition_path)
        with pytest.raises(TypeError):
            header.load_descriptions(corrupted_descrition_path2)
