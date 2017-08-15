#coding=utf-8

import urllib2
import re
import time
import smtplib
import json
import curses
from email.mime.text import MIMEText

mailto = ["XXX@qq.com"]# Receiving mailbox

mail_host = "smtp.163.com"# SMTP of sending mailbox
mail_user = "XXX@163.com"# Sending mailbox
mail_pass = "XXXXXX"# Password of sending mailbox
mail_postfix = "163.com"# Suffix of sending mailbox

me = mail_user+"<"+mail_user+"@"+mail_postfix+">"

def send_mail(to_list,sub,context):
	me = mail_user
	msg = MIMEText(context)
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	

	try:
		s = smtplib.SMTP(mail_host)
		s.login(mail_user,mail_pass)
		s.sendmail(me, to_list, msg.as_string())
		s.quit()

		return True
	except Exception, e:

		return False









url = 'https://eth.waterhole.io:8080/api/accounts/0x7cd26d6d0362eaa6210943e32128cb3ccb019998'
# Replace the url with your Waterhole's API. Like this "https://eth.waterhole.io:8080/api/accounts/'YourAddress'"

headers = {
                "GET":url,
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
          }

req = urllib2.Request(url)
for key in headers:
	req.add_header(key,headers[key])


myscreen = curses.initscr()
myscreen.border(0)


badminer = []
badminerd = []
displayminer = []

while True:



	page = urllib2.urlopen(req).read()
	js1 = json.loads(page)
	workers = js1["workers"]
	
	refstr = str("© Copyright PANGOLINMINER 2017.\n#\n"+time.strftime('%Y-%m-%d %X',time.localtime(time.time())))+"     All Hashrate: "+str(js1["currentHashrate"]/1000000)+(" MH/s\n#\n{} Miners:\n\n".format(len(workers)))


	for k,v in workers.items():
		hr = v["hr"]
		offline = v["offline"]

		if hr > 80000000: # Setting your hashrate standard(80000000 = 80MH/s)
			
			if k in badminer:
				badminer.remove(k)
				send_mail(mailto,"Good News",("Miner: {}\nCurrent Hashrate: {} MH/s\nThis miner is back. Congrats!".format(k,hr/1000000)))

			if k not in displayminer and len(displayminer) < 10:
				displayminer.append(k)
				refstr = refstr + ("{}, {} MH/s\n".format(k,hr/1000000))
			elif k in displayminer:
				displayminer.remove(k)

			
		else:
			
			if k not in badminer:
				badminer.append(k)
				send_mail(mailto,"Bad News",("Miner: {}\nCurrent Hashrate: {} MH/s\nThis miner is not good, it's better to check it.".format(k,hr/1000000)))

			
			if k not in displayminer and len(displayminer) < 10:
				displayminer.append(k)
				refstr = refstr + ("{}, {} MH/s. \n".format(k,hr/1000000))
			elif k in displayminer:
				displayminer.remove(k)



	refstr = refstr + ("#\nYou have {} bad miners: {}".format(len(badminer),", ".join(badminer)))



	badminerd = badminer
	

	myscreen.addstr(0, 0, "\n"*23)
	myscreen.refresh()
	myscreen.addstr(0, 0, refstr)
	myscreen.refresh()
	time.sleep(2)
