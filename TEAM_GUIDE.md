# Hướng dẫn làm việc nhóm - Sokoban

## 1. Phân công (4 người, mỗi người sở hữu 1 file -> không đụng nhau)

| Vai trò | File sở hữu | Nhiệm vụ chính |
|---|---|---|
| **A - Search** | `search.py` | Cải tiến A*: weighted A* (anytime), tối ưu bộ nhớ/tốc độ, chuẩn hóa trạng thái (robot hoán đổi), cải thiện lời giải khi còn giờ |
| **B - Heuristic** | `heuristic.py` | Heuristic mạnh hơn mà vẫn admissible: matching tối thiểu thùng-đích, cộng khoảng cách robot->thùng; cache tính toán |
| **C - Deadlock** | `deadlock.py` | Ô chết dọc tường, deadlock 2x2/freeze, tiền xử lý ô chết bằng "kéo ngược" từ đích |
| **D (trưởng nhóm) - Tích hợp & Test** | `solution.py`, `tools/`, báo cáo | Ghép nối, quản lý timebound, chạy bench mỗi tuần, review PR, nộp bài, viết báo cáo |

Giao diện giữa các module đã **cố định** (xem docstring đầu mỗi file). Ai đổi chữ ký hàm phải báo cả nhóm.

## 2. Thiết lập Git (làm 1 lần)

Trưởng nhóm:
```bash
cd sokoban_team
git init && git add . && git commit -m "Khung du an ban dau"
# tao repo rong tren GitHub (private), moi 3 ban lam Collaborator, roi:
git branch -M main
git remote add origin https://github.com/<ten>/sokoban-team.git
git push -u origin main
```
Thành viên:
```bash
git clone https://github.com/<ten>/sokoban-team.git && cd sokoban-team
```

## 3. Quy trình hằng ngày

```bash
git checkout main && git pull                 # luon cap nhat truoc khi lam
git checkout -b feat/heuristic-matching       # moi tinh nang 1 nhanh
# ... sua CHI file cua minh ...
python tools/bench.py --tb 20                 # tu kiem thu truoc khi day
git add heuristic.py && git commit -m "B: heuristic matching toi thieu"
git push -u origin feat/heuristic-matching    # roi mo Pull Request tren GitHub
```
Quy tắc: **không push thẳng `main`**; PR phải được trưởng nhóm review và bench **không kém hơn** bản hiện tại
(số map giải được không giảm, tổng số bước không tăng) mới merge. Không có Git? Gửi file qua Zalo/Drive cũng được,
nhưng chỉ gửi **đúng file mình sở hữu** cho trưởng nhóm để thay vào.

## 4. Kiểm thử

| Lệnh | Mục đích |
|---|---|
| `python -m unittest test_framework` | Framework còn nguyên |
| `python autograder.py` | 3 test giao diện chính thức (public) |
| `python tools/bench.py --tb 20` | 20 map với bản dev, in OK/FAIL, số bước, thời gian |
| `python tools/bench.py --maps 9 10 --tb 60` | Chỉ chạy vài map khó |
| `python tools/bench.py --bundled --tb 60 --csv kq.csv` | **Test đúng file sẽ nộp** (`dist/solution.py`) |

Mỗi lần merge, trưởng nhóm ghi bảng kết quả (map giải được, tổng bước) vào `TEAM_GUIDE`/báo cáo để thấy tiến bộ.

## 5. Nộp bài

```bash
python tools/bundle.py                 # gop 4 module -> dist/solution.py
python tools/bench.py --bundled --tb 120
```
Chỉ nộp **`dist/solution.py`** (đổi tên thành `solution.py`). Bundle chỉ gỡ các dòng `from deadlock/heuristic/search import ...`,
nên: không dùng `from __future__`, không đặt trùng tên hàm/biến toàn cục giữa các file (đặt tên có tiền tố nếu cần),
và chỉ dùng thư viện chuẩn.

## 6. Lộ trình gợi ý

1. Tuần 1: mọi người chạy được bench; B, C, A mỗi người làm bản cải tiến đầu tiên (baseline hiện giải 9/20 map).
2. Tuần 2: merge lần lượt, đo lại; D thêm chiến lược anytime (weighted A* trước, A* tối ưu sau).
3. Tuần 3: tinh chỉnh các map 9-19, kiểm thử bundle, viết `REPORT_TEMPLATE.md`, nộp.

## 7. Checklist trước khi nộp
- [ ] `solve(..., timebound=0)` trả đúng `False`; hết giờ trả `False`, không treo/crash
- [ ] Không sửa `initial_state`; chỉ dùng `successors()`
- [ ] Không thread/process/mạng, không hard-code theo map
- [ ] `python tools/bench.py --bundled` không có TIMEOUT/CRASH
