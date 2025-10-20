from pathlib import Path
import pandas as pd
from src.data.importer import DataImporter


def test_import_csv_tmp(tmp_path: Path) -> None:
    tmp_csv = tmp_path / "data.csv"
    df_in = pd.DataFrame({"SampleID": ["A1", "A2"], "Result": [1.0, 2.5]})
    df_in.to_csv(tmp_csv, index=False)

    importer = DataImporter()
    df_out = importer.read_table(tmp_csv)

    assert list(df_out.columns) == ["SampleID", "Result"]
    assert len(df_out) == 2


def test_sample_type_normalization():
    imp = DataImporter()
    df = pd.DataFrame({
        "sample_type": ["CRM", "std", "BLK", "Field Blank", "dup", "Check", "Other"]
    })
    out = imp.normalize_sample_type(df)
    assert list(out["sample_type"]) == [
        "STANDARD",
        "STANDARD",
        "BLANK",
        "BLANK",
        "DUPLICATE",
        "DUPLICATE",
        "OTHER",
    ]
