from __future__ import annotations

from pathlib import Path

import cv2
import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

_ERROR_LEVELS = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


class QRToolkitError(ValueError):
    """Raised when QR Toolkit cannot safely complete an operation."""


def generate_qr(
    data: str,
    output: Path | str,
    *,
    error_correction: str = "M",
    box_size: int = 10,
    border: int = 4,
    force: bool = False,
) -> Path:
    """Generate a PNG QR code and return its resolved output path."""
    if not isinstance(data, str) or not data:
        raise QRToolkitError("QR content must be a non-empty string")
    level = error_correction.upper()
    if level not in _ERROR_LEVELS:
        raise QRToolkitError("error_correction must be one of L, M, Q, H")
    if not 1 <= box_size <= 100:
        raise QRToolkitError("box_size must be between 1 and 100")
    if not 0 <= border <= 100:
        raise QRToolkitError("border must be between 0 and 100")

    path = Path(output).expanduser()
    if path.suffix.lower() != ".png":
        raise QRToolkitError("output must use the .png extension")
    if path.exists() and not force:
        raise QRToolkitError(f"output already exists: {path}; use force=True to replace it")
    if path.exists() and not path.is_file():
        raise QRToolkitError(f"output is not a regular file: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)
    qr = qrcode.QRCode(
        version=None,
        error_correction=_ERROR_LEVELS[level],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    image.save(path)
    return path.resolve()


def decode_qr(image_path: Path | str) -> str:
    """Decode the first QR payload in an image without opening or executing it."""
    path = Path(image_path).expanduser()
    if not path.exists():
        raise QRToolkitError(f"image does not exist: {path}")
    if not path.is_file() or path.is_symlink():
        raise QRToolkitError(f"image must be a regular non-symlink file: {path}")

    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise QRToolkitError(f"could not read image: {path}")
    data, points, _ = cv2.QRCodeDetector().detectAndDecode(image)
    if points is None or not data:
        raise QRToolkitError("no decodable QR code found in image")
    return data
