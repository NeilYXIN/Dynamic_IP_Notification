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

import os.path
import socket
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def initialize_gmail_api():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    return service

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

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except HttpError as error:
    print('An error occurred: %s' % error)

def send_gmail(service, sender_email, receiver_email, msg_subject, curr_ip):
    msg_text = "\nIP updated:\n" + curr_ip # Modify your message accordingly, begin with '\n' to separate message and header
    message = create_message(sender_email, receiver_email, msg_subject, msg_text)
    send_message(service, sender_email, message)

# If IP change detected, overwrite the cached IP, close cache file and send out email notification
def write_cache(cache_path, ip):
    with open(cache_path, "w") as f:
        f.write(ip)

def read_cache(cache_path):
    with open(cache_path, "r") as f:
        cached_ip = f.readline()
    return cached_ip

if __name__ == "__main__":
    # Please replace the information included in the brackets {}
    cache_path = "ip_cache.txt" # Path for the cache file
    sender_email = "XXXX@XXX.XXX" # Gmail ONLY
    receiver_email = "XXXX@XXX.XXX"
    msg_subject = "[IP Updater] IP Change Detected" # Email subject

    service = initialize_gmail_api()
    curr_ip = get_curr_ip()

    if not cache_exist(cache_path):
        # Cache file doesn't exist, create cache
        write_cache(cache_path, curr_ip)
        print("[IP Updater] Initialized: " + curr_ip)
        # Send email notification
        send_gmail(service, sender_email, receiver_email, msg_subject, curr_ip)
    else:
        # Compare with cached IP
        cached_ip = read_cache(cache_path)
        if cached_ip != curr_ip:
            # Update cache file
            write_cache(cache_path, curr_ip)
            print("[IP Updater] IP change detected: " + cached_ip + " -> " + curr_ip)
            # Send email notification
            send_gmail(service, sender_email, receiver_email, msg_subject, curr_ip)
        else:
            print("[IP Updater] " + curr_ip)
