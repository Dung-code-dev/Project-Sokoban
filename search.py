"""[Thành viên A] Thuật toán tìm kiếm. Giao diện cố định:

    astar(initial, deadline, h, is_dead, weight=1.0) -> goal_state | None
        deadline: mốc time.perf_counter() phải dừng (hết giờ -> trả None)
        h(state) -> số;  is_dead(state) -> bool
"""
import heapq
import time

from sokoban import sokoban_goal_state


def astar(initial, deadline, h, is_dead, weight=1.0):
    if sokoban_goal_state(initial):
        return initial
    counter = 0
    heap = [(weight * h(initial), 0, counter, initial)]
    best_g = {initial.hashable_state(): 0}
    ticks = 0
    while heap:
        ticks += 1
        if ticks % 64 == 0 and time.perf_counter() >= deadline:
            return None
        _, g, _, state = heapq.heappop(heap)
        if g > best_g.get(state.hashable_state(), g):
            continue                      # bản cũ, đã có đường tốt hơn
        if sokoban_goal_state(state):
            return state
        for nxt in state.successors():    # CHỈ dùng successors() để sinh trạng thái
            key = nxt.hashable_state()
            if key in best_g and best_g[key] <= nxt.gval:
                continue
            if is_dead(nxt):
                continue
            best_g[key] = nxt.gval
            counter += 1
            heapq.heappush(heap, (nxt.gval + weight * h(nxt), nxt.gval, counter, nxt))
    return None
