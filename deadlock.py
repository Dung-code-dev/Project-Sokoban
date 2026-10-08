"""[Thành viên C] Phát hiện deadlock. Giao diện cố định - KHÔNG đổi tên/tham số:

    prepare(initial_state) -> dead        # tính 1 lần trước khi tìm kiếm
    is_deadlock(state, dead) -> bool      # True nếu state chắc chắn vô nghiệm
"""


def prepare(initial_state):
    """Trả về frozenset các ô 'chết': thùng đặt vào đó (ngoài ô đích) là hết cứu."""
    w, h = initial_state.width, initial_state.height
    obs, storage = initial_state.obstacles, initial_state.storage

    def wall(x, y):
        return x < 0 or y < 0 or x >= w or y >= h or (x, y) in obs

    dead = set()
    for x in range(w):
        for y in range(h):
            if (x, y) in obs or (x, y) in storage:
                continue
            # BẢN CƠ BẢN: chỉ bắt thùng kẹt góc. TODO: ô dọc tường không có đích...
            if (wall(x - 1, y) or wall(x + 1, y)) and (wall(x, y - 1) or wall(x, y + 1)):
                dead.add((x, y))
    return frozenset(dead)


def is_deadlock(state, dead):
    # TODO: freeze deadlock (2x2, thùng kề thùng/tường...)
    for b in state.boxes:
        if b in dead:
            return True
    return False
