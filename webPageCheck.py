# -*- coding: UTF-8 -*-

#######
# Author： BlueelWang
# Desc：网站可达性监控，支持https，支持防抖，通过邮件报警
# Date：2023-08-02
#######

import smtplib
import time
import requests

from email.mime.text import MIMEText

# 目标网站
WEBSITE = "https://test.com"
# 检测次数
MAX_RETRIES = 2
# 间隔时间（秒）
INTERVAL = 5
# 报警邮箱
ALERT_EMAIL = ["bbb@gmail.com"]
# 邮件内容
EMAIL_SUBJECT = "【warning】xxx网站不可用"

# SMTP服务器配置
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USERNAME = "bbb@outlook.com"
SMTP_PASSWORD = "xxxxx"
RRCEIVER = ';'.join(ALERT_EMAIL)

def send_alert_email():
    msg = MIMEText(EMAIL_SUBJECT)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = SMTP_USERNAME
    msg["To"] = RRCEIVER

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, ALERT_EMAIL, msg.as_string())
        print("报警邮件已发送")
    except Exception as e:
        print("发送邮件时发生错误:", str(e))
def check_website_reachability():
    try:
        response = requests.get(WEBSITE)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print("发生异常:", str(e))
        return False

retries = 0
while True:
    if check_website_reachability():
        print("网站可达")
        break
    else:
        retries += 1
        if retries > MAX_RETRIES:
            print("网站不可达，发送报警邮件")
            send_alert_email()
            break
        else:
            print("网站不可达，重试第", retries, "次")
            time.sleep(INTERVAL)
