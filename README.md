# QR Toolkit

A local-first Python toolkit for generating and decoding QR codes from the command line or Python.

> **Status:** Functional project. QR generation uses the `qrcode` package; decoding uses OpenCV's `QRCodeDetector`. No network access, telemetry, or API keys are required.

## English

### Overview
QR Toolkit provides a small, dependable interface for creating QR images from text/URLs and decoding QR codes from image files. It is designed for scripts, CI jobs, desktop workflows, and developers who want a clear Python API without an online QR service.

### Why it exists
Online QR generators can expose the content being encoded. QR Toolkit performs generation and decoding locally and offers validation, predictable output, and machine-readable JSON.

### Key features
- Generate PNG QR codes from Unicode text, URLs, or stdin.
- Decode QR codes from PNG/JPEG/WebP images.
- Configurable error correction (`L`, `M`, `Q`, `H`), box size and border.
- Safe overwrite policy: existing output files are preserved unless `--force` is used.
- Human-readable and JSON decode output.
- Python API plus `qr-toolkit` CLI.
- Arabic/Unicode content support.
- No network calls or telemetry.

### Preview
```console
$ qr-toolkit generate "https://example.com" -o code.png
Created code.png

$ qr-toolkit decode code.png
https://example.com
```
For screenshots, show the terminal beside a QR image generated from non-sensitive sample content. Do not publish QR codes containing credentials or private URLs.

### Requirements & installation
- Python 3.10+

```bash
git clone https://github.com/rad03i2/qr-toolkit.git
cd qr-toolkit
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

For development:
```bash
python -m pip install -e ".[dev]"
```

### Usage
```bash
qr-toolkit generate "Hello world" -o hello.png
qr-toolkit generate "مرحبا بالعالم" -o arabic.png --error-correction H
printf "https://example.com" | qr-toolkit generate - -o site.png
qr-toolkit decode site.png
qr-toolkit decode site.png --json
qr-toolkit --version
```

Python API:
```python
from pathlib import Path
from qr_toolkit import generate_qr, decode_qr

generate_qr("Hello", Path("hello.png"))
print(decode_qr(Path("hello.png")))
```

### Configuration
The tool intentionally has no config file or environment variables. Behavior is explicit through CLI options/API arguments. `--force` is required to replace an existing image.

### Project structure
```text
src/qr_toolkit/      library, CLI and module entry point
tests/               unit/integration tests
examples/            safe text examples
.github/workflows/   cross-platform CI
```

### Testing
```bash
python -m pytest
python -m compileall -q src tests
```
CI runs tests on Ubuntu, Windows, and macOS with supported Python versions.

### Limitations
- Decoding depends on OpenCV and image quality; damaged, tiny, highly stylized, or poorly contrasted QR codes may fail.
- This release decodes the first QR payload detected in an image; it is not a barcode suite.
- Generated output is PNG only.
- QR codes can contain malicious links. Decoding a QR code does **not** make its payload trustworthy; review decoded URLs before opening them.

### Security & privacy
Processing is local. The application does not open decoded URLs, execute payloads, upload images, or make network requests. Treat decoded content as untrusted input. See [SECURITY.md](SECURITY.md).

### Optional roadmap
Possible future additions include SVG generation, multi-code decoding, and an optional desktop UI. These are not claimed as current features.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused, tested, and backward-compatible where practical.

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
QR Toolkit حزمة Python محلية لإنشاء رموز QR من النصوص والروابط وفك رموز QR من ملفات الصور، مع واجهة أوامر واضحة وواجهة برمجية قابلة لإعادة الاستخدام.

### لماذا المشروع؟
قد ترسل مولدات QR على الويب النص أو الرابط إلى خدمة خارجية. هذا المشروع ينفذ الإنشاء وفك الترميز محليًا مع تحقق من المدخلات ومخرجات قابلة للاستخدام في الأتمتة.

### الميزات
- إنشاء صور PNG من النصوص والروابط وUnicode والعربية.
- قراءة QR من PNG وJPEG وWebP.
- التحكم بمستوى تصحيح الخطأ وحجم الوحدات والإطار.
- عدم استبدال الملفات الموجودة إلا عند تمرير `--force` صراحة.
- إخراج عادي أو JSON عند فك الترميز.
- CLI وPython API.
- لا اتصالات شبكة ولا telemetry ولا مفاتيح API.

### معاينة
```console
$ qr-toolkit generate "https://example.com" -o code.png
Created code.png
$ qr-toolkit decode code.png
https://example.com
```
يفضل أن تعرض أي لقطة شاشة محتوى تجريبيًا غير حساس فقط.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث:
```bash
git clone https://github.com/rad03i2/qr-toolkit.git
cd qr-toolkit
python -m venv .venv
python -m pip install -e .
```
للتطوير والاختبارات:
```bash
python -m pip install -e ".[dev]"
```

### الاستخدام
```bash
qr-toolkit generate "مرحبا بالعالم" -o arabic.png --error-correction H
qr-toolkit decode arabic.png
qr-toolkit decode arabic.png --json
```
ويمكن استخدام `generate_qr` و`decode_qr` مباشرة من حزمة `qr_toolkit` داخل Python.

### الإعداد
لا يحتاج المشروع ملف إعداد أو متغيرات بيئة. جميع الخيارات صريحة عبر CLI أو Python API، ويلزم `--force` لاستبدال ملف موجود.

### بنية المشروع
المصدر في `src/qr_toolkit/`، والاختبارات في `tests/`، والأمثلة في `examples/`، وإعداد CI في `.github/workflows/`.

### الاختبارات
```bash
python -m pytest
python -m compileall -q src tests
```
وتشغّل GitHub Actions الاختبارات على Linux وWindows وmacOS.

### القيود
- نجاح القراءة يعتمد على جودة الصورة وقد يفشل مع الرموز التالفة أو الصغيرة جدًا أو شديدة الزخرفة.
- الإصدار الحالي يعيد أول QR يتم اكتشافه وليس حزمة شاملة لكل أنواع الباركود.
- الإنشاء حاليًا بصيغة PNG.
- محتوى QR غير موثوق تلقائيًا؛ افحص الرابط الناتج قبل فتحه.

### الأمان والخصوصية
المعالجة محلية؛ لا يفتح البرنامج الروابط الناتجة ولا ينفذ المحتوى ولا يرفع الصور ولا يجري اتصالات شبكة. تعامل دائمًا مع النص المفكوك كمدخل غير موثوق. راجع [SECURITY.md](SECURITY.md).

### تطوير اختياري
يمكن مستقبلًا إضافة SVG، وقراءة عدة رموز من صورة واحدة، وواجهة سطح مكتب اختيارية. هذه ليست ميزات حالية.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md)، وأرفق اختبارات مع التغييرات الوظيفية.

### الترخيص
MIT — راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
