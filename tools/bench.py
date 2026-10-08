"""Chạy solver trên 20 map (mỗi map 1 tiến trình riêng), kiểm tra bằng validation, in bảng kết quả.

  python tools/bench.py                    # dùng solution.py ở thư mục gốc (bản dev)
  python tools/bench.py --bundled          # build rồi test đúng file nộp bài dist/solution.py
  python tools/bench.py --maps 0 3 5 --tb 30 --csv ket_qua.csv
"""
import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_one(idx, tb, root):
    sys.path.insert(0, root)
    import solution, sokoban, validation
    initial = sokoban.PROBLEMS[idx]
    t = time.perf_counter()
    final = solution.solve(initial, timebound=tb)
    dt = time.perf_counter() - t
    if final is False:
        print(json.dumps(dict(ok=False, steps=None, time=dt, msg="False")))
        return
    ok, msg = validation.validate_solution(sokoban.PROBLEMS[idx], final)
    print(json.dumps(dict(ok=ok, steps=final.gval if ok else None, time=dt, msg=msg)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--one", type=int)
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--tb", type=float, default=30)
    ap.add_argument("--maps", type=int, nargs="*")
    ap.add_argument("--bundled", action="store_true")
    ap.add_argument("--csv")
    a = ap.parse_args()
    if a.one is not None:
        return run_one(a.one, a.tb, a.root)

    root = str(ROOT)
    if a.bundled:
        subprocess.run([sys.executable, str(ROOT / "tools" / "bundle.py")], check=True)
        tmp = Path(tempfile.mkdtemp())
        for f in ("state.py", "sokoban.py", "validation.py"):
            shutil.copy(ROOT / f, tmp / f)
        shutil.copy(ROOT / "dist" / "solution.py", tmp / "solution.py")
        root = str(tmp)
    maps = list(a.maps) if a.maps else list(range(20))
    rows, solved, total_steps = [], 0, 0
    print("%-4s %-8s %-8s %-8s %s" % ("map", "ket qua", "so buoc", "giay", "ghi chu"))
    for i in maps:
        r = None
        try:
            r = subprocess.run([sys.executable, __file__, "--one", str(i), "--tb", str(a.tb), "--root", root],
                               capture_output=True, text=True, timeout=a.tb + 15)
            d = json.loads(r.stdout.strip().splitlines()[-1])
        except subprocess.TimeoutExpired:
            d = dict(ok=False, steps=None, time=a.tb + 15, msg="TIMEOUT (không tôn trọng timebound!)")
        except Exception:
            err = (r.stderr.strip().splitlines() or ["?"])[-1] if r else "?"
            d = dict(ok=False, steps=None, time=0, msg="CRASH: " + err)
        solved += d["ok"]
        total_steps += d["steps"] or 0
        rows.append([i, d["ok"], d["steps"], round(d["time"], 2), d["msg"]])
        print("%-4d %-8s %-8s %-8.2f %s" % (i, "OK" if d["ok"] else "FAIL", d["steps"], d["time"], d["msg"]), flush=True)
    print("\nGiải được %d/%d map, tổng số bước = %d" % (solved, len(maps), total_steps))
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["map", "ok", "steps", "seconds", "msg"])
            w.writerows(rows)


if __name__ == "__main__":
    main()
