
# Mail Watch
![](https://img.shields.io/github/stars/philipempl/mail_watch) ![](https://img.shields.io/github/forks/philipempl/mail_watch) ![]](https://img.shields.io/github/issues/philipempl/mail_watch) 

Mail Watch makes it possible to save desired emails and their attachments in EML format using a black list and white list system. Thus, the most important invoices or even customer emails are always archived in the right place and correctly.
Originally this script was developed for my own use, but since it was often asked for, I decided to share it with the public.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Basically Python should be installed. Additional modules that have been installed or used are listed below:

```
imaplib
base64 
os
email
re
configparser
tkinter
datetime
```
### Configuration

The configuration file is shown below. In order to save the e-mails and attachments, the file must be configured correctly. 
The following entries must be corrected: Host, Email and Download.  Additionally subfolders can be specified as arrays in [MAIL_DIRS]. Another folder within the inbox would be described like this:
Inbox/example.
```
[SERVER]
Host = imap.example.com
Port = 993

[ADDRESS]
Email = name@example.de

[DOWNLOAD_DIR]
Download = C:/users/example/

[MAIL_DIRS]
1 = Inbox

[FILES]
Whitelist = whiteList.txt
BlackList = blackList.txt
```

## Run

Basically, the principle of white list (sender I want to save) and black list (sender to be ignored) is used here. Furthermore 
 there are two different Python scripts in the repository:
* mail_watcher.py 
* black_list_all.py

The first is the main script and can also be executed separately from the second script.  The second serves only as an addition to move all email addresses to the blacklist at the beginning. By manual changes desired senders can be moved into the white list afterwards. 



### Commands
The following command executes the script:
```
py mail_watcher.py
```

or

The following command executes the script:
```
py black_list_all.py
```

### Storage Location

Within the specified folder, the structure is structured as follows:

--mail@example.de

---- [YEAR][MONTH][DAY]

---------- content.eml
---------- attachment.pdf


## Contributing

Feel free to email me if you want to make any improvements. I would be very happy about that in any case.

## Authors

* **Philip Empl** - *Initial work* - [Philip Empl](https://github.com/philipempl)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
