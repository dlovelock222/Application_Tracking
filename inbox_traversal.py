import imaplib
import email
import yaml
import openai
import re
import string
import quopri
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
from bs4 import BeautifulSoup
nltk.download('stopwords')
nltk.download('punkt')

api_key = "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"

def open_yml_file(fileName):
    with open(fileName) as f:
        content = f.read()
    return yaml.load(content, Loader=yaml.FullLoader)

def load_inbox(credentialsFileName):
    my_credentials = open_yml_file(credentialsFileName)
    user, password = my_credentials["user"], my_credentials["password"]
    imap_url = 'imap.gmail.com'
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select('Inbox')
    return my_mail

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
    return email_body

def perform_search(my_mail, date):
    key = 'SINCE'
    value = date
    _, data = my_mail.search(None, key, value)
    mail_id_list = data[0].split()
    #Iterate through messages and extract data into the msgs list
    for num in mail_id_list:
        typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        subject = process_subject(msg['subject'])
        sender = process_sender(msg['from'])
        email_body = extract_email_body(msg)
        response = openai.ChatCompletion.create(
            engine="gpt-4",
            prompt=open_yml_file("prompts.yml")['prompt1'],
            max_tokens=100,  # Adjust this value as needed
            api_key=api_key
        ).choices[0].text.strip()
        if response.tolower() == "false":
            print(f"Subject: {subject}\nSender: {sender}\nThis email is not related to a job application")
        else:
            print(f"Subject: {subject}\nSender: {sender}\nContents: \n{response}")
        print("----------------------------------------------------------")
    my_mail.close()
    my_mail.logout()

def process_subject(subject):
    if subject:
        # Decode the subject if it's Quoted-Printable encoded
        if subject.startswith("=?"):
            subject = email.header.decode_header(subject)[0][0]
            if subject is not None and isinstance(subject, bytes):
                subject = quopri.decodestring(subject).decode('utf-8')
            else:
                subject = subject.decode('utf-8')
    return subject
 
def process_sender(text):
    # text = text.replace('@', ' ')
    text = text.replace('<', '')
    text = text.replace('>', '')
    return text

def main():
    quit = False
    while not quit:
        user_input = input("-----CHOICES-----\n--all <DD-MMM-YYYY>\n--<company_name>\n--quit\n").split()
        if user_input[0] == "quit":
            quit = True
        elif user_input[0] == "all":
            date = user_input[1]
            output = perform_search(load_inbox("credentials.yml"), date)
        else:
            company_name = user_input[0]



main()