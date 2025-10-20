from pathlib import Path
import pandas as pd
import pytest
from src.data.importer import DataImporter, ImportedFrame, ImportErrorUnsupportedFormat


def test_read_csv(tmp_path: Path) -> None:
    p = tmp_path / "a.csv"
    pd.DataFrame({"x": [1, 2]}).to_csv(p, index=False)
    imp = DataImporter()
    df = imp.read_table(p)
    assert list(df.columns) == ["x"]
    assert len(df) == 2


def test_read_xlsx(tmp_path: Path) -> None:
    p = tmp_path / "a.xlsx"
    pd.DataFrame({"x": ["a", "b"]}).to_excel(p, index=False)
    imp = DataImporter()
    df = imp.read_table(p)
    assert list(df.columns) == ["x"]
    assert len(df) == 2


def test_read_many(tmp_path: Path) -> None:
    p1 = tmp_path / "a.csv"
    p2 = tmp_path / "b.csv"
    pd.DataFrame({"x": [1]}).to_csv(p1, index=False)
    pd.DataFrame({"y": [2]}).to_csv(p2, index=False)

    imp = DataImporter()
    frames = imp.read_many([p1, p2])
    assert len(frames) == 2
    assert isinstance(frames[0], ImportedFrame)
    assert frames[0].source_path.name == "a.csv"


def test_read_directory(tmp_path: Path) -> None:
    (tmp_path / "a.csv").write_text("x\n1\n")
    pd.DataFrame({"y": [2]}).to_excel(tmp_path / "b.xlsx", index=False)

    imp = DataImporter()
    frames = imp.read_from_directory(tmp_path)
    names = [f.source_path.name for f in frames]
    assert set(names) == {"a.csv", "b.xlsx"}


def test_unsupported_extension(tmp_path: Path) -> None:
    p = tmp_path / "a.txt"
    p.write_text("hello")
    imp = DataImporter()
    with pytest.raises(ImportErrorUnsupportedFormat):
        imp.read_table(p)
