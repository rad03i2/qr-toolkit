# Security Policy

## Supported version
The latest version on `main` receives security fixes.

## Security model
QR Toolkit processes files locally and does not intentionally make network requests, open decoded links, or execute decoded payloads. Decoded QR content is untrusted data and should be reviewed before use. The CLI refuses to overwrite generated files unless `--force` is supplied and refuses symlinks as decode inputs.

Dependencies should be kept current through normal reviewed updates. Do not use this project to encode secrets into QR codes that will be shared publicly.

## Reporting
If you find a vulnerability, please use GitHub's private security reporting feature when it is available for this repository. Avoid publishing exploit details before a fix is available. Do not include real credentials, tokens, or private data in reports.
