import imaplib
import email
import yaml
import json
import os
import email_parsing

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
    print("successfully logged into my inbox")
    return my_mail

def perform_search(my_mail, date):
    key = 'SINCE'
    value = date
    _, data = my_mail.search(None, key, value)
    mail_id_list = data[0].split()
    cleaned_and_labeled_emails = []
    
    for num in mail_id_list:
        cleaned_and_labeled_emails.append(act_on_email(num, my_mail))

    my_mail.close()
    my_mail.logout()
    return cleaned_and_labeled_emails

def act_on_email(email_id, my_mail):

    # grab and decode the email contents and flags from the server
    email_fetch_succcess, email_contents = my_mail.fetch(email_id, '(RFC822)') 
    theEmail = email.message_from_string(email_contents[0][1].decode('utf-8'))
    flag_fetch_succcess, email_flags = my_mail.fetch(email_id, '(FLAGS)')
    theFlags = email_flags[0].split()[2].decode('utf-8')

    # grab subject, sender, and email body, and clean them
    subject = email_parsing.process_subject(theEmail['subject'])
    sender = email_parsing.process_sender(theEmail['from'])
    email_body = email_parsing.extract_email_body(theEmail)

    # determine whether or not the email is flagged
    flagged = False
    if "(\Flagged" in theFlags:
        flagged = True
    print("the following email has been cleaned and labeled:"+ "\nSubject: " + str(subject) + "\nSender: "+ str(sender))
    return [subject,sender,email_body], flagged

def add_emails_to_jsonFile(cleaned_and_labeled_emails, jsonFileName):
    jsonObjects = []
    for email in cleaned_and_labeled_emails:
        data = {
            "subject": email[0][0],
            "sender": email[0][1],
            "body": email[0][2],
            "related": email[1]
        }
        jsonObjects.append(data)
        print("the following email has been added to the JSON file: "+ "\nSubject: " + str(email[0][0]) + "\nSender: " + (email[0][1]))
    with open(jsonFileName, "w") as json_file:
        json.dump(jsonObjects, json_file, indent=4) 
    print("all emails added to json file")

def main():
    date = input("Please specify the start date in DD-MMM-YYYY format: ")
    inbox = load_inbox("credentials.yml")
    cleaned_and_labeled_emails = perform_search(inbox,date)
    print("--------Emails successfully cleaned and labeled--------")
    name = input("What's ya name yung blud (first and last, lowercase, underscore inbetween): ")
    if not os.path.exists("Email_data"):
        os.makedirs("Email_data")
    add_emails_to_jsonFile(cleaned_and_labeled_emails, os.path.join("Email_data", name+"_labeled_emails.json"))

main()