from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

with open("random_forest_model.pkl", "rb") as f:
    model, feature_names, model_accuracy = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    input_data = [
        float(request.form[name]) for name in feature_names
    ]

    input_array = np.array(input_data).reshape(1, -1)

    prediction = model.predict(input_array)[0]
    probability = model.predict_proba(input_array)[0][1] * 100

    if prediction == 1:
        result = "Successful Startup 🚀"
    else:
        result = "Not Successful ❌"

    return render_template(
        "result.html",
        result=result,
        probability=round(probability, 2),
        accuracy=round(model_accuracy * 100, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)
