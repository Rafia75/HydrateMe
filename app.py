from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("water_model.pkl", "rb"))

def feet_inches_to_cm(feet, inches):
    return feet * 30.48 + inches * 2.54
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        try:
            temp = float(request.form["temperature"])
            weight = float(request.form["weight"])
            feet = float(request.form["height_feet"])
            inches = float(request.form["height_inches"])
            height_cm = feet_inches_to_cm(feet, inches)
            activity = request.form["activity"]
            gender = request.form["gender"]

            X_new = pd.DataFrame([{
                "temperature_C": temp,
                "weight_kg": weight,
                "height_cm": height_cm,
                "activity_label": activity,
                "gender": gender
            }])

            glasses = model.predict(X_new)[0]
            glasses = round(max(glasses, 1))
            liters = round(glasses * 0.25, 2)

            result = f"""
            <h3>💧 Water Intake Suggestion</h3>
            <p><b>Glasses of water:</b> {glasses}</p>
            <p><b>You need about:</b> {liters} L water</p>
            """
        except Exception as e:
            result = f"<p style='color:red;'>Error: {e}</p>"

    # ALWAYS return a response
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
