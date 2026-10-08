"""[Thành viên B] Heuristic. Giao diện cố định:

    heuristic(state) -> int/float     # ước lượng số bước còn lại, càng sát thật càng tốt
"""


def heuristic(state):
    """BẢN CƠ BẢN (admissible): mỗi thùng chưa ở đích -> khoảng cách Manhattan tới đích gần nhất.
    TODO: matching tối thiểu thùng-đích, cộng khoảng cách robot->thùng gần nhất..."""
    total = 0
    storage = state.storage
    for bx, by in state.boxes:
        if (bx, by) in storage:
            continue
        total += min(abs(bx - sx) + abs(by - sy) for sx, sy in storage)
    return total
