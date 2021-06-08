import smtplib
import time
import datetime

oldtime=0

######### Steps ###########################
# Replace your gmail_user & password
# Script uses a plain text password so 
# it is unsecure
# Replace the email id to which mail
# will be sent. 
# You also need to enable less secure 
# app enablement. Search google for details
############################################

######### Email ##########
gmail_user = 'xxxx@gmail.com'
gmail_password = 'password'
sent_from = gmail_user
to = ['yyyy@gmail.com']
subject = "Cowin Alert - Vaccine Availability- {}".format(datetime.datetime.today())
body = ""
email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

#https://stackoverflow.com/questions/25189554/countdown-clock-0105/50148334
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

def hour_passed(oldtime):
    return time.time() - oldtime >= 3600

def send_gmail():
    global oldtime
    if not hour_passed(oldtime): return
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        oldtime = time.time()
        print ('Email sent!')
    except:
        print ('Something went wrong...')
