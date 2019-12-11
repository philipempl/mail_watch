import imaplib, base64, os, email, re, configparser
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from email import generator
from dateutil.parser import parse

def init():
  
  mail = imaplib.IMAP4_SSL(config['SERVER']['Host'],config['SERVER']['Port'])
  pwd = str(input("PWD: "))
  print(pwd)
  mail.login(str(config['ADDRESS']['Email']),pwd )
  for dir in config['MAIL_DIRS']:
    dir = config['MAIL_DIRS'][dir]
    print('\n ##########################     ' + dir + '     ##################################\n')
    mail.select(dir)
    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    readAllMails(id_list, mail)
  
def readAllMails(id_list, mail):

  counter = 0
  l = len(id_list)
  for num in id_list:
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
    
	# converts byte literal to string removing b''
    try:
      raw_email_string = raw_email.decode('utf-8')
      email_message = email.message_from_string(raw_email_string)
	# get sender from mail
    except:
      continue
    sender_name = ''
    sender_email = ''
    sender_array = email_message['from'].split('<')
    if(len(sender_array) > 1):
       sender_email = (sender_array[1][:-1]).lower()
       sender_name = re.sub(r"[^a-zA-Z0-9]+", ' ',sender_array[0]).strip()
    else:
       sender_email = (sender_array[0]).lower()
    counter = counter + 1
    printProgressBar(counter, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    if(isInWhiteList(sender_email)):
      downloadMail(email_message, sender_email)
    elif(isInBlackList(sender_email) == False):
      openDialog(sender_email, email_message)

def downloadMail(email_message, sender):

	# create directory if not exist
    filePath = os.path.join(directoryName, sender)
    if not os.path.exists(filePath):
      os.makedirs(filePath)

    for part in email_message.walk():
	
        # extract and format date
        date = email_message['Date']
        date_time_obj = ''
        try:
          date_time_obj = parse(date)
        except:
          print(date)

        # extract subject and dir name
        file_storage = str(date_time_obj.year)+ str(date_time_obj.strftime('%m')) +  str(date_time_obj.strftime('%d'))
        subject = re.sub(r"[^a-zA-Z0-9]+", ' ',email_message['subject']).strip()
		
        file_path_subject = filePath + "/" + file_storage

        if not os.path.exists(file_path_subject):
          os.makedirs(file_path_subject)

        if not os.path.isfile(file_path_subject):

		   # download email text into eml format
           o_file_name = subject + '.eml'
           output_file = os.path.join(file_path_subject, o_file_name)
           with open(output_file, 'w') as outfile:
             try:
               gen = generator.Generator(outfile)
               gen.flatten(email_message)
             except:
               continue

        # checking if data is available
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        data = part.get_payload(decode=True)
        if not data:
            continue
        if filename is None:
            continue
        try:
          attachment = open(os.path.join(file_path_subject, filename), 'wb')
          attachment.write(data)
          attachment.close()
        except: 
          continue

def openDialog(sender, email_message):
    root = tk.Tk()
    root.withdraw()
    MsgBox = tk.messagebox.askquestion( sender,sender + '  \n\nWhat should be done with this sender? \n\n [yes] = white list \n [no] = black list' ,icon = 'warning')
    if MsgBox == 'yes':
      addToWhiteList(sender)
      downloadMail(email_message, sender)
    else:
      addToBlackList(sender)

def isInWhiteList(sender):

  with open(white_list) as whiteList:
    if sender in whiteList.read():
      return True
    else:
      return False

def isInBlackList(sender):

  with open(black_list) as blackList:
    if sender in blackList.read():
      return True
    else:
      return False

def addToBlackList(sender):

   hs = open("blackList.txt","a")
   hs.write(sender + "\n")
   hs.close() 

def addToWhiteList(sender):

   hs = open("whiteList.txt","a")
   hs.write(sender + "\n")
   hs.close() 

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


config = configparser.ConfigParser()
config.read('config.ini')
directoryName = str(config['DOWNLOAD_DIR']['Download'])
white_list = str(config['FILES']['Whitelist'])
black_list = str(config['FILES']['Blacklist'])
init()

