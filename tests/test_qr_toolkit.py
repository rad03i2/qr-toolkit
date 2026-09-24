from __future__ import annotations

import json
from pathlib import Path

import pytest

from qr_toolkit import QRToolkitError, decode_qr, generate_qr
from qr_toolkit.cli import main


def test_round_trip_ascii(tmp_path: Path) -> None:
    target = tmp_path / "hello.png"
    generate_qr("https://example.com/path?q=1", target)
    assert target.is_file()
    assert decode_qr(target) == "https://example.com/path?q=1"


def test_round_trip_arabic(tmp_path: Path) -> None:
    target = tmp_path / "arabic.png"
    generate_qr("مرحبا بالعالم", target, error_correction="H")
    assert decode_qr(target) == "مرحبا بالعالم"


def test_refuses_overwrite_without_force(tmp_path: Path) -> None:
    target = tmp_path / "code.png"
    generate_qr("first", target)
    with pytest.raises(QRToolkitError, match="already exists"):
        generate_qr("second", target)
    generate_qr("second", target, force=True)
    assert decode_qr(target) == "second"


@pytest.mark.parametrize("kwargs", [
    {"error_correction": "X"},
    {"box_size": 0},
    {"border": -1},
])
def test_rejects_invalid_generation_options(tmp_path: Path, kwargs: dict) -> None:
    with pytest.raises(QRToolkitError):
        generate_qr("data", tmp_path / "x.png", **kwargs)


def test_rejects_empty_content(tmp_path: Path) -> None:
    with pytest.raises(QRToolkitError, match="non-empty"):
        generate_qr("", tmp_path / "x.png")


def test_requires_png_extension(tmp_path: Path) -> None:
    with pytest.raises(QRToolkitError, match=".png"):
        generate_qr("data", tmp_path / "x.jpg")


def test_decode_missing_file(tmp_path: Path) -> None:
    with pytest.raises(QRToolkitError, match="does not exist"):
        decode_qr(tmp_path / "missing.png")


def test_cli_json_decode(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    target = tmp_path / "cli.png"
    assert main(["generate", "hello", "-o", str(target)]) == 0
    capsys.readouterr()
    assert main(["decode", str(target), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["data"] == "hello"


def test_cli_error_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["decode", str(tmp_path / "missing.png")]) == 2
    assert "error:" in capsys.readouterr().err
