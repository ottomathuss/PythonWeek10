"""
    Author:          Hartmut Mathussek
    Date Created:    08/23/2020
    Functionality:
                     This module handles sending emails
                     
"""

import smtplib
from smtplib import SMTP
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

smtp_user_name = 'none'
smtp_password = 'none'
db_path = os.path.dirname(os.path.realpath(__file__))

def f_smtp_server(notification, recipient_email):
    # Function that sets up the SMTP server
    # Input: notification - body of email notification
    # Input: recipient_email - email of investor to be notified
    # Output: success or failur message

    #try:
        smtp_user_name, smtp_password = f_set_server_credentials()
        s = smtplib.SMTP(host='smtp.comcast.net', port=587)
        s.starttls()
        s.login(smtp_user_name, smtp_password)
        f_send_message(s, notification, recipient_email)
        return "Investor was successfully notified."
    #except:
    #    return "Error while notifying investor."

def f_set_server_credentials():
    # Function that reads server credentials from text file and assigns values to variables
    # Input: nothing
    # Return: user name and password to access smtp server

    try:
       filename = db_path + '\SMTP Signon.txt'
       with open(filename, mode='r', encoding='utf-8') as credentials_file:
           for credential in credentials_file:
               user_name = credential.split()[0]
               password = credential.split()[1]
       return user_name, password
    except:
        return "error"

def f_send_message(s, notification, email_recipient):
    # Create message
    # Input: s - smtp server
    # Input: notification - body of email
    # Input: email_recipient - email of investor to be notified
    # Return: nothing

    try:
        msg = MIMEMultipart()
        
        # setup the parameters of the message
        msg['From']="Stock Program<otto_mathuss@comcast.net>"
        msg['To']=email_recipient
        msg['Subject']="Stock Program Notification"

        # add in the message body
        msg.attach(MIMEText(notification, 'plain'))

        # send the message via the server
        s.send_message(msg)
        
        del msg

    except SMTPException:
       print("Error: unable to send email")
