"""Gộp deadlock.py + heuristic.py + search.py + solution.py -> dist/solution.py (file nộp bài)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORDER = ["deadlock", "heuristic", "search", "solution"]
LOCAL = "|".join(ORDER)
LOCAL_IMPORT = re.compile(r"^\s*(from\s+(%s)\s+import\s+.*|import\s+(%s))\s*$" % (LOCAL, LOCAL))


def main():
    parts = ['"""Sokoban solver - file nộp bài, được sinh tự động bởi tools/bundle.py."""\n']
    for name in ORDER:
        src = (ROOT / (name + ".py")).read_text(encoding="utf-8")
        if re.search(r"^\s*from\s+__future__", src, re.M):
            raise SystemExit("Không dùng 'from __future__' trong " + name)
        lines = [ln for ln in src.splitlines() if not LOCAL_IMPORT.match(ln)]
        parts.append("\n# " + "=" * 20 + " " + name + ".py " + "=" * 20 + "\n" + "\n".join(lines) + "\n")
    out = ROOT / "dist" / "solution.py"
    out.parent.mkdir(exist_ok=True)
    out.write_text("".join(parts), encoding="utf-8")
    print("Đã tạo", out)


if __name__ == "__main__":
    main()
