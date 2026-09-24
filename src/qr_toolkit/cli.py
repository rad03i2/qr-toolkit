from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import QRToolkitError, decode_qr, generate_qr

VERSION = "1.0.0"
AUTHOR = "Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="qr-toolkit", description="Generate and decode QR codes locally.")
    parser.add_argument("--version", action="version", version=f"QR Toolkit {VERSION} — {AUTHOR}")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate a PNG QR code")
    gen.add_argument("data", help="Text to encode, or '-' to read UTF-8 text from stdin")
    gen.add_argument("-o", "--output", type=Path, required=True, help="Output .png path")
    gen.add_argument("--error-correction", choices=("L", "M", "Q", "H"), default="M")
    gen.add_argument("--box-size", type=int, default=10)
    gen.add_argument("--border", type=int, default=4)
    gen.add_argument("--force", action="store_true", help="Replace an existing output file")

    dec = sub.add_parser("decode", help="Decode the first QR code from an image")
    dec.add_argument("image", type=Path)
    dec.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            data = sys.stdin.read() if args.data == "-" else args.data
            if args.data == "-":
                data = data.rstrip("\r\n")
            output = generate_qr(
                data,
                args.output,
                error_correction=args.error_correction,
                box_size=args.box_size,
                border=args.border,
                force=args.force,
            )
            print(f"Created {output}")
            return 0

        payload = decode_qr(args.image)
        if args.as_json:
            print(json.dumps({"image": str(args.image), "data": payload}, ensure_ascii=False))
        else:
            print(payload)
        return 0
    except (QRToolkitError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
