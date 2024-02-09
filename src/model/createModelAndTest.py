import json
import pandas as pd
import os
import sklearn
import re
import openai
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import flask

#Text Processing libraries
import nltk
nltk.download('stopwords')
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger'])
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


#Model libraries
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

#Save the model
import joblib
from joblib import dump, load

#Evaluate the model
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()
api_key = "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"

def main():
    filename = input("Please input the name of the user: ")
    modelType = input("Select one of the following options:\n1. Open AI\n2. Linear Regression\n")
    if modelType == "1":
        X,y = preprocess_data(filename,1)
        y_pred = GPTModel(X)
        # printError(y, y_pred)
    elif modelType == "2":
        X,y = preprocess_data(filename,2)
        y_test, y_pred = LogReg(X,y)
        printError(y_test, y_pred)
        
def preprocess_data(filename, modelVal):
    while True:
        if filename == "quit":
            exit()
        try:
            with open(os.path.join("Email_data", filename+"_labeled_emails.json"), 'r') as file:
                data = json.load(file)
                df = pd.DataFrame(data)
                if modelVal == 1:
                    return df[['subject','sender', 'body']], df['related']
                df['clean_subject'] = df['subject'].apply(lambda x: tokenize(x))
                df['clean_sender'] = df['sender'].apply(lambda x: tokenize(x))
                df['clean_body'] = df['body'].apply(lambda x: tokenize(x))
                for index, row in df.iterrows():
                    c_subject = row['clean_subject']
                    c_sender = row['clean_sender']
                    subject = row['subject']
                    sender = row['sender']
                    print(f"{index}. c_subject: '{c_subject}'\n{index}. c_sender: '{c_sender}'")
                    print(f"{index}. subject: '{subject}'\n{index}. sender: '{sender}'")
                print("all emails have been tokenized")
                X = df[['clean_subject','clean_sender', 'clean_body']]
                y = df['related']
                return X,y
        except FileNotFoundError:
            filename = input("File not found, please try again. (or type quit to exit program): ")
    
def GPTModel(X):
    toReturn = []
    prompt = "I am going to give you the sender and subject for a list of emails. Tell me the following two things for each email: whether or not the email is related to a job application update, and a certainty score expressed as a percentage.\n"
    output_formatting = "---BEGIN OUTPUT FORMAT TEMPLATE---\nTrue or False, Certainty: X%\n---END OUTPUT FORMAT TEMPLATE---\n"
    curr_prompt = prompt + output_formatting
    words = len(curr_prompt)
    for index, row in X.iterrows():
        if words < 2000:
            subject = row['subject']
            sender = row['sender']
            curr_prompt += f"{index}. subject: '{subject}', sender: '{sender}'\n"
            words += 3+len(subject)+len(sender)
        else:
            print(curr_prompt)
            # response = openai.Completion.create(
            #     engine="davinci",  # Choose an appropriate engine
            #     prompt=curr_prompt,
            #     max_tokens=1000,
            #     api_key=api_key
            # )
            # print(response.choices[0].text)
            # if "false" in response.choices[0].text.lower():
            #     print("false")
            #     toReturn.append("False")
            # else:
            #     toReturn.append("True")
            #     print("true")
            words = len(prompt+output_formatting)
            curr_prompt = prompt+output_formatting
    return toReturn

def LogReg(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train['clean_subject'] + ' ' + X_train['clean_sender']+ ' ' + X_train['clean_body'])
    model = LogisticRegression(max_iter=1000)  # You can adjust hyperparameters if needed
    model.fit(X_train_vec, y_train)
    filename = 'linear_regression_model.pkl'
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    X_test_vec = vectorizer.transform(X_test['clean_subject'] + ' ' + X_test['clean_sender'] + ' ' + X_test['clean_body'])
    return y_test, model.predict(X_test_vec)

def tokenize(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower().strip())
    tokens = word_tokenize(text)
    words = [w for w in tokens if w not in stopwords.words("english")]
    lemmed_words = [WordNetLemmatizer().lemmatize(w) for w in words]
    clean_tokens = []
    for i in lemmed_words:
        clean_tokens.append(i)
    
    text = " ".join(clean_tokens)
    return text

def printError(y_test, y_pred):
    confusion = confusion_matrix(y_test, y_pred)
    actual_positives = sum(true == 1 for true in y_test)
    actual_negatives = sum(true == 0 for true in y_test)
    tn, fp, fn, tp = confusion.ravel()
    total = tn + fp + fn + tp
    tn = tn / actual_negatives * 100
    fp = fp / actual_negatives * 100
    fn = fn / actual_positives * 100
    tp = tp / actual_positives * 100
    print(f"True Negatives: {tn:.2f}%, False Positives: {fp:.2f}%, False Negatives: {fn:.2f}%, True Positives: {tp:.2f}%")

main()