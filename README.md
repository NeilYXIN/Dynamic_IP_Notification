# IP_Updater
 A Python script that can send out emails to notify dynamic IP changes.

## Introduction

This Python script can be deployed to detect IP changes and send out email notifications.

It only uses Python's built-in APIs.


## How it works

- This script compares the latest IP address with the previous one cached in a .txt file.  

- When initialized or IP change detected, an email notification containing the latest IP address will be sent.

- This script uses Gmail server as default, you will need a Gmail account to send out the email notifications.

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
Note: This is a one-time detection. You can set up a scheduled task using third-party libraries, such as Cron, to periodically detect IP changes.

## Security Risks/Known Issues

- The email password in the example code is **NOT** protected. You need to be aware of potential risks like password leakage. Please ONLY use this script in a trusted environment or replace the password authentication with a secure API.

- This script is tested on macOS 11.5.2 & Ubuntu 20.04 LTS running Python 3.8.

## License

LICENSE'D under the Apache 2 license by Xin Yang.

Part of the code is derived from the python documentation examples thus some of the code is Copyright © 2001-2013 Python Software Foundation; All Rights Reserved under the PSF license (GPL compatible) http://docs.python.org/2/library/socketserver.html