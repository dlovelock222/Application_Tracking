import imaplib
import email
import yaml
import openai

api_key = "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"

def open_yml_file(fileName):
    with open(fileName) as f:
        content = f.read()
    return yaml.load(content, Loader=yaml.FullLoader)

class JobApplication:
    def __init__(self, company, job_title, submitted_date):
        self.submitted_date = submitted_date
        self.status = "active" # active, offer, or rejected
        self.company = company
        self.updates = [[submitted_date, "applied", "none"]]
    
    # Updates are going to be in the form of date,type,other information
    def add_update(self, update):
        self.updates.append(update)

def load_inbox(credentialsFileName):
    my_credentials = open_yml_file(credentialsFileName)
    user, password = my_credentials["user"], my_credentials["password"]
    imap_url = 'imap.gmail.com'
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select('Inbox')
    return my_mail

def perform_search(my_mail, date):
    key = 'SINCE'
    value = date
    _, data = my_mail.search(None, key, value)
    mail_id_list = data[0].split()
    #Iterate through messages and extract data into the msgs list
    for num in mail_id_list:
        typ, data = my_mail.fetch(num, '(RFC822)') #RFC822 returns whole message (BODY fetches just body)
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        subject = msg['subject']
        sender = msg['from']
        description = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    temp = part.get_payload(decode=True).decode('utf-8')
                    if temp:
                        description += temp
        prompts = open_yml_file("prompts.yml")
        pre_screen_prompt = prompts["subject_and_sender_prompt1"]
        likelihood = openai.Completion.create(
            engine="text-davinci-002",
            prompt=pre_screen_prompt+ "\n" + "subject: {subject}\nsender: {sender}\n description: {description}",
            max_tokens=50,
            api_key=api_key,
            n=1
        )
        print(f"Subject: {subject}\nSender: {sender}", likelihood.choices[0].text)


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
