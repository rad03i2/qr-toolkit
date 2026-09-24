# Contributing

Thanks for improving QR Toolkit.

1. Create a focused branch.
2. Use Python 3.10+ and install `python -m pip install -e ".[dev]"`.
3. Keep processing local-first; do not add telemetry, embedded credentials, or network calls without a clear documented reason.
4. Add or update tests for behavior changes.
5. Run `python -m compileall -q src tests` and `python -m pytest`.
6. Update the English and Arabic README sections when user-facing behavior changes.
7. Open a pull request describing the motivation, behavior, and validation performed.

Keep commits scoped and never commit generated QR images containing sensitive data.
