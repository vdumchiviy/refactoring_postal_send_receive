import email
import smtplib
import imaplib
# import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Post():

    def __init__(self, login: str, password: str,
                 GMAIL_SMTP: str = "smtp.gmail.com", GMAIL_IMAP: str = "imap.gmail.com"):
        self.login = login
        self.password = password
        self.GMAIL_SMTP = GMAIL_SMTP
        self.GMAIL_IMAP = GMAIL_IMAP

    def create_email_message(self, recipients: str, subject: str, message: str):
        result = MIMEMultipart()
        result['From'] = self.login
        result['To'] = ', '.join(recipients)
        result['Subject'] = subject
        result.attach(MIMEText(message))
        return result

    def send_mail(self, recipients: list, subject: str, message: str):

        if len(recipients) < 1:
            return False

        email_message = self.create_email_message(recipients, subject, message)

        try:
            server = smtplib.SMTP(self.GMAIL_SMTP, 587)
            server.ehlo()   # identify ourselves to smtp gmail client
            server.starttls()  # secure our email with tls encryption
            server.ehlo()  # re-identify ourselves as an encrypted connection

            server.login(self.login, self.password)
            server.sendmail(self.login,  recipients, email_message.as_string())
            server.quit()  # send end
            return True
        except Exception as e:
            print(str(e))
            return False

    def receive_mail(self, filter_by_subject: str = None):
        mail_box = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail_box.login(self.login, self.password)
        mail_box.list()
        mail_box.select("inbox")
        criterion = '(HEADER Subject "%s")' % filter_by_subject if filter_by_subject else 'ALL'
        result, data = mail_box.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail_box.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1].decode('utf-8')
        email_message = email.message_from_string(raw_email)
        mail_box.logout()
        return email_message


if __name__ == "__main__":
    login = ""
    password = ""
    post = Post(login, password)
    result = post.send_mail([login, ],
                            "Hello from Python!", "This is a test message from Python3!")
    print(result)

    result = post.receive_mail()
    print(result)
