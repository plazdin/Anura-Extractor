'''Simple module that sends anura extractor log
mail to specific list of addresses'''
from datetime import date, timedelta
import smtplib, os, ssl

from config import conf


class SENDER():
    sender = 'mail'
    passw = 'pass'
    recievers =['plazdin@sanjorge-sa.com.ar']
    wrecievers = [
        
        ]
    
    context = ssl.create_default_context()
    
    @classmethod
    def send_mail(cls, log_time):
        file = open(
        os.path.join(cls.conf.LOG_PATH, f'{log_time}.log'),
        encoding='utf-8')
        
        send = f'From: ANURA SERVICE<{cls.sender}>'
        subjt = f'Subject: Anura extractor Log ({log_time})'        
        to = f'To: {",".join(["<%s>" % m for m in cls.recievers])}'
        
        message = '{}\n{}\n{}\n{}'.format(
            send, subjt, to, file.read()
        )
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=cls.context) as server:
            server.login(cls.sender, cls.passw)
            server.comand_encoding = 'utf-8'
            server.sendmail(cls.sender, cls.recievers, message.encode('utf-8'))

if __name__ == '__main__':
    log_time =  date.today() - timedelta(days=1)
    mailer = SENDER()
    mailer.send_mail(log_time)

        