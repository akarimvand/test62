import requests
import base64

# تنظیمات اولیه
GITHUB_TOKEN = 'xxxxxx'  # توکن دسترسی خود را اینجا وارد کنید
REPO_OWNER = 'akarimvand'
REPO_NAME = 'test62'
FILE_PATH = 'db.txt'  # مسیر فایل در مخزن
COMMIT_MESSAGE = 'Add or update db.txt file'

# خواندن فایل به صورت باینری
try:
    with open('db.txt', 'rb') as file:  # 'rb' برای خواندن فایل به صورت باینری
        file_content = file.read()
except Exception as e:
    print(f"خطا در خواندن فایل: {e}")
    exit()

# تبدیل محتوای فایل به Base64
encoded_content = base64.b64encode(file_content).decode('utf-8')

# URL API GitHub
url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'

# سرآیند (Headers)
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

# ارسال درخواست GET برای بررسی وجود فایل
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # فایل وجود دارد، بنابراین آن را به‌روزرسانی می‌کنیم
    file_sha = response.json()['sha']
    
    # داده‌های درخواست برای به‌روزرسانی فایل
    update_data = {
        'message': COMMIT_MESSAGE,
        'content': encoded_content,
        'sha': file_sha
    }
    
    # ارسال درخواست PUT برای به‌روزرسانی فایل
    update_response = requests.put(url, headers=headers, json=update_data)

    # بررسی پاسخ
    if update_response.status_code == 200:
        print("فایل موجود به‌روزرسانی شد.")
    else:
        print(f"خطا در به‌روزرسانی فایل: {update_response.status_code}")
        print(update_response.json())
else:
    # فایل وجود ندارد، بنابراین آن را ایجاد می‌کنیم
    create_data = {
        'message': COMMIT_MESSAGE,
        'content': encoded_content
    }
    
    # ارسال درخواست PUT برای ایجاد فایل
    create_response = requests.put(url, headers=headers, json=create_data)

    # بررسی پاسخ
    if create_response.status_code == 201:
        print("فایل با موفقیت به مخزن اضافه شد.")
    else:
        print(f"خطا در ایجاد فایل: {create_response.status_code}")
        print(create_response.json())
