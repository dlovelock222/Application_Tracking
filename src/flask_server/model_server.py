from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict_job_application', methods=['GET'])
def predict_job_application():
    sender = request.args.get('sender')
    subject = request.args.get('subject')
    snippet = request.args.get('snippet')

    # Assuming your model is already trained and loaded
    # You can use the model.predict method here
    # Example: prediction = model.predict([data['preview']])

    # For this example, I'll return a random prediction (0 or 1)
    import random
    prediction = random.choice([0, 100])

    response = {'prediction': prediction}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)