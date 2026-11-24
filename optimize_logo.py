from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "logo.png"
OUTPUT = ROOT / "logo.webp"

if not SOURCE.exists():
    raise SystemExit("logo.png is missing; refusing to generate a replacement.")

with Image.open(SOURCE) as original:
    image = original.convert("RGBA")
    image.thumbnail((720, 720), Image.Resampling.LANCZOS)
    image.save(OUTPUT, format="WEBP", quality=88, method=6)

extensions = {".html", ".css", ".js", ".xml", ".json", ".md", ".txt"}
updated = []

for path in ROOT.rglob("*"):
    if not path.is_file() or path == SOURCE or path == OUTPUT or path == Path(__file__):
        continue
    if ".git" in path.parts or ".github" in path.parts:
        continue
    if path.suffix.lower() not in extensions:
        continue

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue

    changed = re.sub(
        r'((?:src|srcset)\s*=\s*["\'][^"\']*?)logo\.png(?:\?v=[^"\']*)?',
        r'\1logo.webp',
        text,
        flags=re.IGNORECASE,
    )
    changed = re.sub(
        r'(url\(\s*["\']?[^)"\']*?)logo\.png(?:\?v=[^)"\']*)?',
        r'\1logo.webp',
        changed,
        flags=re.IGNORECASE,
    )

    if changed != text:
        path.write_text(changed, encoding="utf-8")
        updated.append(str(path.relative_to(ROOT)))

original_bytes = SOURCE.stat().st_size
optimized_bytes = OUTPUT.stat().st_size
print(f"Original logo: {original_bytes:,} bytes")
print(f"Optimized WebP: {optimized_bytes:,} bytes")
print(f"Estimated reduction: {100 * (1 - optimized_bytes / original_bytes):.1f}%")
print(f"Updated {len(updated)} text files:")
for name in updated:
    print(f" - {name}")
