"""Sokoban: Weighted A* (anytime) + heuristic ghép cặp thùng-đích + cắt ô chết."""
import heapq
import time
from functools import lru_cache

from sokoban import sokoban_goal_state



NAMES = ("up", "right", "down", "left")
INF = 10 ** 9
CAP = 400000                                    # số trạng thái tối đa mỗi lượt (giới hạn bộ nhớ)


def solve(initial_state, timebound=120):
    if timebound <= 0:
        return False
    end = time.perf_counter() + timebound - min(3.0, timebound * 0.08)
    s0 = initial_state
    if sokoban_goal_state(s0):
        return s0
    W, H = s0.width, s0.height
    N = W * H
    nbr = [[-1] * 4 for _ in range(N)]          # nbr[c][d]: ô kề theo hướng d (UP,RIGHT,DOWN,LEFT)
    for y in range(H):
        for x in range(W):
            for d, (dx, dy) in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))):
                a, b = x + dx, y + dy
                if (x, y) not in s0.obstacles and 0 <= a < W and 0 <= b < H and (a, b) not in s0.obstacles:
                    nbr[y * W + x][d] = b * W + a
    goals = [y * W + x for x, y in s0.storage]
    # pd[g][c] = số lần đẩy tối thiểu đưa thùng từ ô c tới đích g (BFS ngược)
    pd = []
    for g in goals:
        q = [g]
        dist = {g: 0}
        for p in q:
            for d in range(4):
                c = nbr[p][d ^ 2]
                if c >= 0 and c not in dist and nbr[c][d ^ 2] >= 0:
                    dist[c] = dist[p] + 1
                    q.append(c)
        pd.append(dist)
    dead = [all(c not in dist for dist in pd) for c in range(N)]   # ô chết

    @lru_cache(maxsize=None)
    def h(boxes):                               # ghép cặp thùng-đích, tổng số lần đẩy nhỏ nhất
        @lru_cache(maxsize=None)
        def f(i, used):
            if i == len(boxes):
                return 0
            return min((pd[j][boxes[i]] + f(i + 1, used | 1 << j) for j in range(len(goals))
                        if not used >> j & 1 and boxes[i] in pd[j]), default=INF)
        return f(0, 0)

    def frozen(c, bset, stack):                 # thùng c bị chặn cả hai trục (tường/ô chết/thùng bị đóng băng)?
        stack.add(c)
        res = True
        for a, z in ((3, 1), (0, 2)):
            l, r = nbr[c][a], nbr[c][z]
            if (l < 0 or r < 0 or (dead[l] and dead[r]) or (l in bset and (l in stack or frozen(l, bset, stack)))
                    or (r in bset and (r in stack or frozen(r, bset, stack)))):
                continue
            res = False
            break
        stack.discard(c)
        return res

    gset = set(goals)
    robots = tuple(y * W + x for x, y in s0.robots)
    boxes = tuple(sorted(y * W + x for x, y in s0.boxes))
    best_actions, ub = None, INF
    for w in (5, 20, 60, 2.5, 1.5, 1):
        if time.perf_counter() >= end:
            break
        if best_actions and w > 5:
            continue                            # w lớn chỉ là phương án dự phòng khi chưa có lời giải
        # --- một lượt A* có trọng số, cắt nhánh bằng ub ---
        heap = [(w * h(boxes), 0, robots, boxes, None)]
        seen = {(tuple(sorted(robots)), boxes): 0}
        found, tick = None, 0
        while heap and found is None:
            tick += 1
            if len(seen) > CAP or (not tick & 255 and time.perf_counter() >= end):
                break
            _, g, rs, bs, node = heapq.heappop(heap)
            if seen[(tuple(sorted(rs)), bs)] < g:
                continue
            if all(b in goals for b in bs):
                found = (g, node, None)
                break
            bset = set(bs)
            for i, p in enumerate(rs):
                for d in range(4):
                    n = nbr[p][d]
                    if n < 0 or n in rs:
                        continue
                    nb = bs
                    if n in bset:               # đẩy thùng
                        m = nbr[n][d]
                        if m < 0 or m in bset or m in rs or dead[m]:
                            continue
                        nb = tuple(sorted(m if b == n else b for b in bs))
                        nset = set(nb)
                        if any(c not in gset and frozen(c, nset, set()) for c in [m] + [x for x in nbr[m] if x in nset]):
                            continue                # deadlock đóng băng
                    nr = rs[:i] + (n,) + rs[i + 1:]
                    key = (tuple(sorted(nr)), nb)
                    hv = h(nb)
                    if hv >= INF or g + 1 + hv >= ub or seen.get(key, INF) <= g + 1:
                        continue
                    seen[key] = g + 1
                    heapq.heappush(heap, (g + 1 + w * hv, g + 1, nr, nb, (node, i * 4 + d)))
        if found:
            ub = found[0]
            acts, node = [], found[1]
            while node:
                node, a = node
                acts.append(a)
            best_actions = acts[::-1]
        elif not heap:
            break                               # cạn kiệt: UB đã tối ưu (hoặc vô nghiệm)
    if best_actions is None:
        return False
    s = s0                                      # dựng chuỗi parent bằng successors() của framework
    for a in best_actions:
        want = "%d %s" % (a // 4, NAMES[a % 4])
        s = next(t for t in s.successors() if t.action == want)
    return s


if __name__ == "__main__":
    from sokoban import PROBLEMS
    print("=== Đang giải thử nghiệm Sokoban Map 0 ===")
    problem = PROBLEMS[0]
    t0 = time.perf_counter()
    res = solve(problem, timebound=10)
    dt = time.perf_counter() - t0

    if res:
        # Lần ngược từ trạng thái đích về đầu để lấy danh sách hành động
        actions = []
        curr = res
        while curr.parent:
            actions.append(curr.action)
            curr = curr.parent
        actions.reverse()

        print(f"\n✅ Đã tìm thấy lời giải sau {dt:.3f}s (tổng cộng {len(actions)} bước):\n")
        for i, act in enumerate(actions, 1):
            parts = act.split()
            robot_id, direction = parts[0], parts[1]
            print(f"Bước {i:02d}: Robot {robot_id} di chuyển {direction}")

        print(f"\nDanh sách rút gọn: {actions}")
    else:
        print("\n❌ Không tìm thấy lời giải!")