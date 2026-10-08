"""[Trưởng nhóm] Lớp ghép nối. File NỘP BÀI được sinh bằng: python tools/bundle.py"""
import time

from deadlock import prepare, is_deadlock
from heuristic import heuristic
from search import astar


def solve(initial_state, timebound=120):
    """Trả về trạng thái đích có chuỗi parent hợp lệ, hoặc False."""
    if timebound <= 0:
        return False
    start = time.perf_counter()
    deadline = start + timebound - min(3.0, timebound * 0.05)   # chừa biên an toàn
    dead = prepare(initial_state)

    def dead_fn(s):
        return is_deadlock(s, dead)

    # Chiến lược 'anytime': tìm nhanh bằng weighted A*, nếu còn giờ thì cải thiện (TODO)
    for weight in (1.0,):
        result = astar(initial_state, deadline, heuristic, dead_fn, weight)
        if result is not None:
            return result
    return False
