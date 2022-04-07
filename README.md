# Server_IP_Updater

## Introduction

 A Python script that sends email notifications when IP change is detected.

Can be helpful when you want to remotely access a machine whose IP is dynamically assigned.

Now supports Google Gmail API and OAuth 2.0.

## Workflow

- This script uses Gmail APIs, you need a Gmail account to get started.

- This script compares the current IP address with the snapshot IP cached in a txt file.  

- When initialized or IP change detected, an email will be sent to notify the latest IP.

        if (initialize) {
            create cache file
            send email notification
        } else if (current IP = cached IP){
            do nothing
        } else {
            update cache
            send email notification
        }


## How to Use

### Install Google Client Library (Python)
- Quick Start Guide: https://developers.google.com/gmail/api/quickstart/python

        pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

### Create Google Cloud Project and Download Credentials
1. Create a Google Cloud project: https://developers.google.com/workspace/guides/create-project

2. Create access credentials (Desktop app): https://developers.google.com/workspace/guides/create-credentials

3. Download credentials json file into the root directory and rename as "credentials.json".

4. Go to Google Cloud Platform -> [Your Project] -> APIs & Services -> OAuth consent screen, add your Gmail account as a test user (or publish the app).

### Initialization

1. Change the `sender_email` and `receiver_email` in the main function before first use.

2. Execute the Python script:

        python3 ip_updater.py
    
    When executed for the first time, Google authentication process will start in the terminal for headless servers. 
    Or replace line 54 with line 53 to prompt a webpage for authentication, if your server has a monitor. 
    
3. Follow the instructions in the terminal, login with your Gmail account (must be added as a test user) and grant the sending email permission.

4. Google OAuth API will generate a "token.json" file at the root directory.

5. You are all set if no error occurs.

### Automation
Running this script is a one-time detection. 
You can set up a scheduled task using third-party libraries, such as Cron, to periodically execute this script.

Below is an example of using [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) to periodically check the IP every 30 minutes, which remains valid even after a server reboot.

    30 * * * * /usr/bin/python3 /YOUR/PATH/TO/ip_updater.py


## Known Issues

- Currently only supports Gmail account.
- Tested on macOS 12.3.1 & Ubuntu 20.04 LTS running Python 3.8.

- ~~The email password is **NOT** protected. You need to be aware of the password leakage risk. Please **ONLY** use this in a trusted environment or replace the password authentication with a secure API.~~


## License

LICENSE'D under the Apache 2 license by Xin Yang.

Part of the code is derived from the python documentation examples thus some of the code is Copyright © 2001-2013 Python Software Foundation; All Rights Reserved under the PSF license (GPL compatible) http://docs.python.org/2/library/socketserver.html
