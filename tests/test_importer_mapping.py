from src.data.importer import DataImporter, REQUIRED_FIELDS
import pandas as pd


def test_normalize_header():
    imp = DataImporter()
    assert imp.normalize_header(" Sample_ID ") == "sampleid"
    assert imp.normalize_header("Depth-From") == "depthfrom"
    assert imp.normalize_header("Lab/Name") == "labname"


def test_suggest_mapping_exact_and_fuzzy():
    headers = [
        "SampleID",
        "TYPE",
        "Value",  # synonym for result
        "Hole Id",
        "From",
        "To",
    ]
    imp = DataImporter()
    suggestions = imp.suggest_mapping(headers, threshold=0.8)

    # Required fields should have matches
    for req in REQUIRED_FIELDS:
        matched, score = suggestions[req]
        assert matched is not None
        assert score >= 0.8

    # Optional example
    assert suggestions["hole_id"][0] == "Hole Id"


def test_validate_required_missing():
    imp = DataImporter()
    mapping = {"sample_id": "SampleID", "result": "Value"}  # missing sample_type
    missing = imp.validate_required(mapping)
    assert missing == ["sample_type"]


def test_apply_mapping_renames_columns():
    imp = DataImporter()
    df = pd.DataFrame({"SampleID": ["A1"], "Value": [1.2]})
    out = imp.apply_mapping(df, {"SampleID": "sample_id", "Value": "result"})
    assert list(out.columns) == ["sample_id", "result"]
