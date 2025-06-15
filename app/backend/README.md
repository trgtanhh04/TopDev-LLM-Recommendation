# Setup Backend

## 1. Tạo Conda Environment
Chạy lệnh sau để tạo môi trường Conda với Python 3.10:
```sh
conda create -n topdev-backend python=3.10 -y
conda activate topdev-backend
```

## 2. Cài đặt các thư viện
Chạy lệnh sau để cài đặt các thư viện từ `requirements.txt`:
```sh
pip install -r requirements.txt
```

## 3. Chạy Backend
Chạy lệnh sau để khởi động backend:
```sh
uvicorn main:app --reload
```

Backend sẽ chạy tại `http://127.0.0.1:8000`.