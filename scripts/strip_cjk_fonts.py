# -*- coding: utf-8 -*-
"""Remove CJK font definitions from .docx packages so the file is strictly English.

python-docx's default template ships a fontTable listing MS Mincho / MS Gothic and a theme
naming CJK script faces. They never render in English text, but they are still CJK content
inside the file, so they get stripped here.
"""
import re
import shutil
import zipfile
from pathlib import Path

CJK = r"\u3000-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef"

FONT_BLOCK = re.compile(r'<w:font\b[^>]*w:name="[^"]*[' + CJK + r'][^"]*"[^>]*>.*?</w:font>', re.S)
THEME_FACE = re.compile(r'(typeface=")[^"]*[' + CJK + r'][^"]*(")')
RESIDUAL = re.compile(r"[" + CJK + r"]+")


def clean_xml(text: str) -> str:
    text = FONT_BLOCK.sub("", text)
    text = THEME_FACE.sub(r"\1Times New Roman\2", text)
    return RESIDUAL.sub("", text)


def clean_docx(path: Path) -> int:
    tmp = path.with_suffix(".tmp")
    removed = 0
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename.endswith(".xml") or item.filename.endswith(".rels"):
                original = data.decode("utf-8")
                cleaned = clean_xml(original)
                if cleaned != original:
                    removed += 1
                data = cleaned.encode("utf-8")
            dst.writestr(item, data)
    shutil.move(tmp, path)
    return removed


def main():
    root = Path(r"D:\src\amtocsoft\amtocsoft-megagent\work\round3")
    for p in sorted(root.rglob("*.docx")):
        n = clean_docx(p)
        print(f"{p.name}: {n} parts cleaned")


if __name__ == "__main__":
    main()
