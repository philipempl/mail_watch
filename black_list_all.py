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
	
    if(isInBlackList(sender_email) == False):
      addToBlackList(sender_email)

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
		  	  
init()