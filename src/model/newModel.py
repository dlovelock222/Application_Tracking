# Import necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report

# Sample dataset
data = [
    {'sender': 'john.doe@example.com', 'subject': 'Job Application', 'preview': 'Dear Hiring Manager, ...'},
    {'sender': 'jane.smith@example.com', 'subject': 'Meeting Tomorrow', 'preview': 'Hi, I hope you are doing well...'},
    # Add more examples with labels indicating if they are job application emails or not
]

# Create a DataFrame
import pandas as pd
df = pd.DataFrame(data)

# Assign labels (1 for job application, 0 for not related)
df['label'] = df['subject'].apply(lambda x: 1 if 'job' in x.lower() or 'application' in x.lower() else 0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[['sender', 'subject', 'preview']], df['label'], test_size=0.2, random_state=42)

# Create a pipeline with CountVectorizer and Multinomial Naive Bayes classifier
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train['preview'], y_train)

# Make predictions on the test set
predictions = model.predict(X_test['preview'])

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print(f"Accuracy: {accuracy}")
print("Classification Report:\n", report)

# Now you can use the trained model to make predictions on new data
new_data = {'sender': 'test@example.com', 'subject': 'Job Opportunity', 'preview': 'Dear Hiring Team, ...'}
new_prediction = model.predict([new_data['preview']])
print(f"Predicted likelihood for job application: {new_prediction[0]}")