from src.data.importer import DataImporter
import pandas as pd


def test_parse_result_with_qualifier_basic():
    imp = DataImporter()

    # Plain number
    v, q, dl = imp.parse_result_with_qualifier("1.23")
    assert v == 1.23 and q is None and dl is None

    # Less-than number
    v, q, dl = imp.parse_result_with_qualifier("<0.01")
    assert v is None and q == "<" and dl == 0.01

    # Greater-than number
    v, q, dl = imp.parse_result_with_qualifier(">10")
    assert v is None and q == ">" and dl == 10.0

    # Tokens
    v, q, dl = imp.parse_result_with_qualifier("ND", default_dl=0.005)
    assert v is None and q == "<" and dl == 0.005

    v, q, dl = imp.parse_result_with_qualifier(">DL", default_dl=0.1)
    assert v is None and q == ">" and dl == 0.1

    # Negative numeric (below detection)
    v, q, dl = imp.parse_result_with_qualifier("-0.02")
    assert v is None and q == "<" and dl == 0.02


def test_normalize_results_creates_qualifier_and_dl_columns():
    imp = DataImporter()
    df = pd.DataFrame({"result": ["<0.02", "1.5", ">DL", "ND", "  ", "-0.02"]})

    out = imp.normalize_results(df, result_col="result", qualifier_col="qual", dl_col="dl", default_dl=0.01)

    # Row-wise expectations
    assert pd.isna(out.loc[0, "result"]) and out.loc[0, "qual"] == "<" and out.loc[0, "dl"] == 0.02
    assert out.loc[1, "result"] == 1.5 and pd.isna(out.loc[1, "qual"]) and pd.isna(out.loc[1, "dl"])
    assert pd.isna(out.loc[2, "result"]) and out.loc[2, "qual"] == ">" and out.loc[2, "dl"] == 0.01
    assert pd.isna(out.loc[3, "result"]) and out.loc[3, "qual"] == "<" and out.loc[3, "dl"] == 0.01
    assert pd.isna(out.loc[4, "result"]) and pd.isna(out.loc[4, "qual"]) and out.loc[4, "dl"] == 0.01
    assert pd.isna(out.loc[5, "result"]) and out.loc[5, "qual"] == "<" and out.loc[5, "dl"] == 0.02


def test_normalize_uses_row_detection_limit_when_present():
    imp = DataImporter()
    df = pd.DataFrame({
        "result": ["<DL", ">DL", "ND", "1.0", "<0.005"],
        "detection_limit": [0.01, 0.02, 0.03, 0.04, 0.001],
    })

    out = imp.normalize_results(df, result_col="result", qualifier_col="qual", dl_col="detection_limit", default_dl=0.99)

    # For <DL/>DL/ND, should use per-row detection_limit, not default
    assert pd.isna(out.loc[0, "result"]) and out.loc[0, "qual"] == "<" and out.loc[0, "detection_limit"] == 0.01
    assert pd.isna(out.loc[1, "result"]) and out.loc[1, "qual"] == ">" and out.loc[1, "detection_limit"] == 0.02
    assert pd.isna(out.loc[2, "result"]) and out.loc[2, "qual"] == "<" and out.loc[2, "detection_limit"] == 0.03
    # Plain numeric keeps dl as given (no change)
    assert out.loc[3, "result"] == 1.0 and pd.isna(out.loc[3, "qual"]) and out.loc[3, "detection_limit"] == 0.04
    # Explicit <0.005 overrides row DL for that row
    assert pd.isna(out.loc[4, "result"]) and out.loc[4, "qual"] == "<" and out.loc[4, "detection_limit"] == 0.005
