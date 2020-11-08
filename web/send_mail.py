#
#   template for sending mail with Python!
#

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import argv 

email_password = 'PASSWORD!'

from_addr = 'FROM@EMAIL.com'
to_addr = 'TO@EMAIL.com'

# create email message
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr

if len(argv) >= 3:
    subj = argv[1]
    msg_body = argv[2]
else:
    subj = 'AUTOMATED MESSAGE'
    msg_body = ''

msg['Subject'] = subj

body = f'''
{msg_body}
'''

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, email_password)

    server.sendmail(from_addr, to_addr, msg.as_string())

    print('Message sent')

    server.quit()

except Exception as e:
    print('Message failure')
    print(f'Error message: {e}')
