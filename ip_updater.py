import os.path
import smtplib
import socket
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#  Copyright (c) 2021. Xin Yang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python ip_updater.py

# Please replace the information included in the brackets {}
cache_path = "{./ip_cache.txt}" # Path for the IP cache file
sender_email = "{sender@gmail.com}"
receiver_email = "{receiver@gmail.com}"
sender_pswd = "{password}" # Password of the sender email, only run in a trusted environment or replace with a secure authentication API
msg_subject = "[IP Updater] {IP Change Detected}" # Email subject


# get current ip using socket
def get_curr_ip():
    hostname = socket.gethostname()
    curr_ip = socket.gethostbyname(hostname)
    return curr_ip


# Detect the existence of the IP cache file
def cache_exist(cache_path):
    if os.path.exists(cache_path):
        return True
    else:
        return False


# Compose email content and send out
def send_ip_email(new_ip):
    # Compose a plain text email
    message = MIMEMultipart("alternative")
    message["Subject"] = msg_subject
    message["From"] = sender_email
    message["To"] = receiver_email
    msg_text = "\n{Updated IP:\n" + new_ip + "\n}" # Modify your message accordingly, start with '\n' to separate message and header
    msg_part = MIMEText(msg_text, "plain")
    message.attach(msg_part)

    # Connect with server and send email through SSL
    context = ssl.create_default_context()
    # Default server set as gmail, change accordingly
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_pswd)
        server.sendmail(sender_email, receiver_email, message.as_string())


# If IP change detected, overwrite the cached IP, close cache file and send out email notification
def update_ip(f, new_ip):
    f.write(new_ip)
    f.close()
    send_ip_email(new_ip)


if __name__ == "__main__":
    curr_ip = get_curr_ip()
    if not cache_exist(cache_path):
        # Cache file doesn't exist, create cache file
        f = open(cache_path, "w")
        print("[IP Updater] Cache file created!")
        # Send out email notification for initialization
        update_ip(f, curr_ip)
        print("[IP Updater] Initialized.\n", curr_ip)

    else:
        # Cache file exist, read cached IP and compare with the current one
        f = open(cache_path, "r+")
        cached_ip = f.readline()
        if cached_ip != curr_ip:
            update_ip(f, curr_ip)
            print("[IP Updater] New IP detected!\n", cached_ip, "->", curr_ip)
        else:
            print("[IP Updater] IP unchanged.\n", curr_ip)