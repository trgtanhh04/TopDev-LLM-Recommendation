# ĐỒ ÁN CUỐI KỲ MÔN HỌC MÁY

## 1. Mục tiêu

- Nắm vững kiến thức về mô hình ngôn ngữ lớn (LLMs) thông qua việc áp dụng và huấn luyện các mô hình LLMs.
- Hiểu và thực hiện các kỹ thuật tối ưu hóa như fine-tuning, transfer learning để điều chỉnh mô hình với tập dữ liệu cụ thể.
- Phát triển kỹ năng xử lý ngôn ngữ tự nhiên và áp dụng vào các ứng dụng thực tế.
- Đánh giá và phân tích hiệu suất của mô hình.

## 2. Tiêu chí đánh giá

- Ý tưởng và mục tiêu đề tài
- Phân tích và xác định vấn đề
- Mô hình giải pháp đề xuất
- Thu thập và xử lý dữ liệu (**)
- Thiết kế và triển khai mô hình
- Huấn luyện mô hình (**)
- Đánh giá hiệu suất mô hình
- So sánh và tinh chỉnh mô hình (**)
- Ứng dụng và demo thực tế
- Mức độ tích hợp mô hình vào ứng dụng web
- Giao diện và trải nghiệm người dùng
- Tài liệu, báo cáo minh chứng
- Thuyết trình và trả lời câu hỏi

(**) Các mục được xem là đóng góp hay tính mới của đề tài.

---

## 3. Ý tưởng đề tài

**Tên đề tài:** Hệ thống gợi ý việc làm dựa trên LLM và Machine Learning

**Các bước thực hiện:**

1. **Thu thập dữ liệu:**  
   - Crawl dữ liệu tuyển dụng từ website [https://topdev.vn/](https://topdev.vn/).
2. **Tiền xử lý dữ liệu:**  
   - Làm sạch, chuẩn hóa văn bản, xử lý các trường thông tin.
3. **Áp dụng mô hình:**  
   - Sử dụng LLM (Large Language Model) kết hợp các thuật toán Machine Learning.
   - Fine-tune hoặc transfer learning để phù hợp với dữ liệu tuyển dụng.
4. **Tinh chỉnh mô hình:**  
   - Đánh giá, so sánh các mô hình, chọn giải pháp tối ưu, tinh chỉnh tham số.
5. **Triển khai ứng dụng:**  
   - Deploy mô hình lên một ứng dụng web (app) để người dùng nhập thông tin và nhận gợi ý việc làm phù hợp.
6. **Đánh giá hiệu quả:**  
   - Kiểm tra kết quả, so sánh với các phương pháp truyền thống, lấy phản hồi người dùng nếu có.

---

## 4. Cấu trúc thư mục dự án

```
ML-FINAL-PROJECT/
├── app/                              # Triển khai app
├── data/
│   ├── job_url.csv                  # Danh sách URL tin tuyển dụng đã crawl
│   ├── preprocessed_data.csv         # Dữ liệu đã làm sạch, tiền xử lý
│   └── raw_data.csv                  # Dữ liệu gốc chưa xử lý
├── docs/
│   └── ml-project.pdf                # Báo cáo, tài liệu đồ án
├── notebooks/
│   ├── 1.0-data-collecting.ipynb     # Notebook thu thập dữ liệu
│   ├── 2.0-preprocessing.ipynb       # Notebook tiền xử lý dữ liệu
│   └── 3.0-data-modeling.ipynb       # Notebook xây dựng, huấn luyện, đánh giá mô hình
└── src/              # Mã nguồn về LLM + ML
```

---

## 5. Hướng phát triển

- Tích hợp thêm các nguồn dữ liệu khác.
- Mở rộng chức năng gợi ý theo kỹ năng, vị trí, mức lương...
- Cải tiến giao diện người dùng, trải nghiệm sử dụng.
