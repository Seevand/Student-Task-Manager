
# Student Task Manager

سامانه مدیریت وظایف دانش‌آموزان

## Technologies

- Python
- Flask
- HTML
- CSS
- Bootstrap 5
- JavaScript
- JSON

## Features

- ایجاد وظایف توسط مدیر
- ویرایش وظایف
- حذف وظایف
- نمایش وظایف در صفحه کاربر
- تأیید انجام وظایف
- ثبت نام انجام‌دهنده
- ذخیره اطلاعات در فایل JSON
- نمایش وظایف تکمیل‌شده

## Project Structure

```text
Student-Task-Manager/
│
├── app.py
├── requirements.txt
├── data/
│   └── tasks.json
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── adminpanel.html
│
└── static/
    ├── css/
    ├── js/
    ├── images/
    └── fonts/
```

## Installation

Create virtual environment:

```bash
py -m venv .venv
```

Activate environment:

```bash
.venv\Scripts\activate
```

Install requirements:

```bash
py -m pip install -r requirements.txt
```

Run project:

```bash
py app.py
```

## URLs

User page:

http://127.0.0.1:5000

Admin panel:

http://127.0.0.1:5000/admin

## Database

All task information is stored in:

data/tasks.json

## Note

This is a simple educational project.
Admin authentication and user account management
are not implemented.
