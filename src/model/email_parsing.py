import email
import re
import quopri
from bs4 import BeautifulSoup

def process_subject(subject):
    if subject:
        # Decode the subject if it's Quoted-Printable encoded
        if subject.startswith("=?"):
            subject = email.header.decode_header(subject)[0][0]
            if subject is not None and isinstance(subject, bytes):
                subject = quopri.decodestring(subject).decode('utf-8')
            else:
                subject = subject.decode('utf-8')
        return ''.join(char for char in subject if ord(char) < 128)
    return ""
 
def process_sender(text):
    if text.startswith("=?"):
        text = email.header.decode_header(text)[0][0]
        if text is not None and isinstance(text, bytes):
            text = quopri.decodestring(text).decode('utf-8')
        else:
            text = text.decode('utf-8')
    text = text.replace('<', '')
    text = text.replace('>', '')
    return text

def extract_email_body(msg):
    email_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                try:
                    email_body = part.get_payload(decode=True).decode('utf-8')
                except UnicodeDecodeError:
                    # Attempt decoding with a different codec, e.g., 'latin-1'
                    email_body = part.get_payload(decode=True).decode('latin-1')
                if part.get_content_type() == "text/html":
                    soup = BeautifulSoup(email_body, 'html.parser')
                    for a in soup.find_all('a'):
                        a.extract()
                    email_body = soup.get_text()
    if " " in email_body:
        email_body = re.sub(r'\s+', ' ', email_body)
    if "\n" in email_body:
        email_body = re.sub(r'\n+', '\n', email_body)
    # removing all non ascii characters
    email_body = ''.join(char for char in email_body if ord(char) < 128)
    return email_body