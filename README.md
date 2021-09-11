# Server_IP_Updater
 A Python script that can send emails to notify dynamic IP changes using Python's built-in APIs.

## Introduction

This Python script can detect IP changes and send the latest IP through email notifications. This can be helpful when you want to remotely access a machine but its IP is dynamically assigned.

## How it works

- This script compares the latest IP address with the previous IP cached in a .txt file.  

- When initialized or IP change detected, an email will be sent to notify the latest IP.

- This script uses Gmail as default, you need a Gmail account to send emails.

Script Actions:  

        if (used for the first time) {
            create cache file;
            send email notification;
        } else if (current IP = cached IP){
            do nothing;
        } else {
            overwrite cache;
            send email notification;
        }


## How to Use

Change all **{** replaceable parts **}** in the code before first use.

Using this script is easy:

        python ip_updater.py    
Note: This is a one-time detection. You can set up a scheduled task using third-party libraries (e.g., Cron), to automate the IP change detection in a periodical manner.  

## Security Risks/Known Issues

- The email password is **NOT** protected. You need to be aware of the password leakage risk. Please **ONLY** use this in a trusted environment or replace the password authentication with a secure API.

- Tested on macOS 11.5.2 & Ubuntu 20.04 LTS running Python 3.8.

## License

LICENSE'D under the Apache 2 license by Xin Yang.

Part of the code is derived from the python documentation examples thus some of the code is Copyright © 2001-2013 Python Software Foundation; All Rights Reserved under the PSF license (GPL compatible) http://docs.python.org/2/library/socketserver.html
