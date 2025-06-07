# 1. Tạo thư mục dự án và thiết lập môi trường ảo
mkdir insurance_management
cd insurance_management

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 2. Cài đặt các package cần thiết
pip install django
pip install djangorestframework
pip install django-cors-headers
pip install djangorestframework-simplejwt
pip install python-decouple

# Hoặc nếu có requirements.txt
# pip install -r requirements.txt

# 3. Tạo dự án và các app
django-admin startproject insurance_project .

python manage.py startapp authentication
python manage.py startapp core

python manage.py startapp khachhang
python manage.py startapp sanpham  
python manage.py startapp hopdong
python manage.py startapp phi
python manage.py startapp thanhtoan

# 4. Tạo migrations cho tất cả các app
python manage.py makemigrations

# 5. Chạy migrations để cập nhật database
python manage.py migrate

# 6. Tạo superuser quản trị
python manage.py createsuperuser

# 7. Tạo dữ liệu mẫu (nếu có command tạo sẵn)
python manage.py create_sample_data

# Hoặc tạo mới hoàn toàn (xóa dữ liệu cũ)
# python manage.py create_sample_data --reset

# 8. Chạy server để kiểm tra
python manage.py runserver
