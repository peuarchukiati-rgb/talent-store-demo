"""Quote check must treat composed and decomposed Vietnamese as the same text.

Run: python3 tests/test_quote_check.py
"""
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from talentstore.prescreen import _check  # noqa: E402
from talentstore.store import load_jd, read_md, RAW  # noqa: E402

_, jd_meta, _ = load_jd("JD-SC-014")
_, body = read_md(RAW / "candidates" / "C-009.md")
quote = "Quản lý nhóm 3 chuyên viên kế hoạch"
cases = {
    "NFC quote (as typed)": unicodedata.normalize("NFC", quote),
    "NFD quote (decomposed tone marks)": unicodedata.normalize("NFD", quote),
    "tone mark dropped (must FAIL)": "Quan ly nhom 3 chuyen vien ke hoach",
    "translated, not quoted (must FAIL)": "Manages a team of 3 planners",
}
expect = [True, True, False, False]
ok = True
for (name, q), want in zip(cases.items(), expect):
    result = {"requirements": [{"id": "R5", "status": "evidenced", "evidence": [{"quote": q}]}]}
    _check(result, {"requirements": [r for r in jd_meta["requirements"] if r["id"] == "R5"]}, body)
    got = result["requirements"][0]["evidence"][0]["verified"]
    ok &= got == want
    print(f"{'PASS' if got == want else 'FAIL'}  {name}: verified={got}")
sys.exit(0 if ok else 1)
