# CV & Job Matcher Web App

**CV & Job Matcher** là một nền tảng web giúp bạn **so sánh CV với tin tuyển dụng (JD)** để đánh giá mức độ phù hợp và nhận các lời khuyên phát triển kỹ năng dựa trên trí tuệ nhân tạo.

---

## Tính năng nổi bật

- **Tải lên CV**: Nhập hoặc tải lên CV của bạn (dưới dạng JSON), chỉ cần thao tác một lần.
- **Phân tích tin tuyển dụng (JD)**: Trích xuất và phân tích các yêu cầu, kỹ năng, kinh nghiệm từ JD.
- **So sánh tự động**: Chấm điểm mức độ phù hợp giữa CV và JD, liệt kê các kỹ năng còn thiếu, gợi ý khóa học phát triển bản thân.
- **Tư vấn AI**: Sử dụng AI (Mistral API, model `mistral-medium`) để đưa ra nhận xét, gợi ý chi tiết và cá nhân hóa.
- **Giao diện thân thiện**: Dễ dàng thao tác, hiển thị trực quan điểm số, kỹ năng, và gợi ý ngay bên cạnh JD.
- **Bảo mật & riêng tư**: CV của bạn chỉ lưu trên trình duyệt (localStorage), không bị gửi lên server.

---

## Kiến trúc dự án

```
app/
├── backend/   # Flask API - Xử lý logic, kết nối Mistral AI
└── frontend/  # Vue 3 - Giao diện người dùng, lưu trữ CV, trình bày kết quả
```

### Backend (`app/backend`)

- **Ngôn ngữ:** Python 3.x
- **Framework:** Flask
- **Endpoint chính:** `/give_advice`
    - Nhận dữ liệu CV & JD, gửi prompt tới Mistral, trả về nhận xét, điểm số, kỹ năng còn thiếu, gợi ý học tập.
- **Tích hợp AI:** Gọi API Mistral (`https://api.mistral.ai/v1/chat/completions`) để sinh phản hồi thông minh.

### Frontend (`app/frontend`)

- **Ngôn ngữ:** JavaScript (Vue 3, Composition API, Single File Component)
- **Chức năng:**
    - Cho phép người dùng nhập CV hoặc tải lên file JSON.
    - Gửi CV & JD lên backend qua API `/give_advice`.
    - Lưu thông tin CV vào **localStorage** để sử dụng lại cho các lần sau.
    - Hiển thị kết quả so sánh, điểm số, kỹ năng còn thiếu, và gợi ý học tập trực tiếp bên cạnh phần JD.
- **Trải nghiệm:** Tương tác mượt mà, realtime, dễ sử dụng cho cả người tìm việc lẫn HR.

---

## Cài đặt & Khởi chạy

### 1. Clone dự án

```bash
git clone https://github.com/yourusername/cv-job-matcher.git
cd cv-job-matcher
```

### 2. Cài đặt Backend

```bash
cd app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Cấu hình biến môi trường:**
- Tạo file `.env` và thêm:
    ```
    MISTRAL_API_KEY=your_mistral_api_key
    ```

**Chạy server:**
```bash
flask run
```

### 3. Cài đặt Frontend

```bash
cd ../../app/frontend
npm install
npm run dev
```

### 4. Truy cập ứng dụng

- Mở trình duyệt và truy cập [http://localhost:5173](http://localhost:5173) (hoặc port mà Vite/Vue báo).

---

## Ví dụ sử dụng

1. **Tải lên hoặc nhập CV** (dạng JSON).
2. **Dán tin tuyển dụng** muốn so sánh.
3. **Nhận kết quả:** 
    - Điểm phù hợp CV-JD
    - Danh sách kỹ năng còn thiếu
    - Gợi ý khóa học/phát triển
    - Phản hồi chi tiết từ AI

---

## Công nghệ sử dụng

- **Frontend:** Vue 3, Composition API, Vite
- **Backend:** Python, Flask, Requests, dotenv
- **AI:** Mistral API (`mistral-medium`)
- **Khác:** localStorage, RESTful API

---

## Đóng góp & Liên hệ

- Gửi ý kiến hoặc PR tại [github.com/yourusername/cv-job-matcher](https://github.com/yourusername/cv-job-matcher)
- Liên hệ: your.email@example.com

---

## ⚖️ Giấy phép

MIT License
