from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, get_all_patients, add_patient, get_patient_by_id, update_patient, delete_patient
from ai_service import get_health_prediction
from datetime import date
import re

app = Flask(__name__)
app.secret_key = "mira_secret_key_2024"

init_db()

# VALIDATION 
def validate_form(data):
    errors = []

    if not data["full_name"].strip():
        errors.append("Full Name is required.")

    if not data["dob"]:
        errors.append("Date of Birth is required.")
    else:
        try:
            dob = date.fromisoformat(data["dob"])
            if dob >= date.today():
                errors.append("Date of Birth cannot be today or a future date.")
        except ValueError:
            errors.append("Invalid Date of Birth format.")

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    if not data["email"] or not re.match(email_regex, data["email"]):
        errors.append("Please enter a valid email address.")

    for field in ["glucose", "haemoglobin", "cholesterol"]:
        val = data[field].strip()
        if not val:
            errors.append(f"{field.capitalize()} is required.")
        else:
            try:
                num = float(val)
                if num <= 0:
                    errors.append(f"{field.capitalize()} must be a positive number.")
            except ValueError:
                errors.append(f"{field.capitalize()} must be a numeric value.")

    return errors



# READ — list all patients

@app.route("/")
def index():
    patients = get_all_patients()
    return render_template("index.html", patients=patients)



# CREATE

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = {
            "full_name":   request.form.get("full_name", "").strip(),
            "dob":         request.form.get("dob", "").strip(),
            "email":       request.form.get("email", "").strip(),
            "glucose":     request.form.get("glucose", "").strip(),
            "haemoglobin": request.form.get("haemoglobin", "").strip(),
            "cholesterol": request.form.get("cholesterol", "").strip(),
        }

        errors = validate_form(data)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("add.html", form_data=data)

        remarks = get_health_prediction(
            float(data["glucose"]),
            float(data["haemoglobin"]),
            float(data["cholesterol"])
        )

        add_patient(
            data["full_name"], data["dob"], data["email"],
            float(data["glucose"]), float(data["haemoglobin"]),
            float(data["cholesterol"]), remarks
        )

        flash(f"Patient <strong>{data['full_name']}</strong> added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html", form_data={})



# UPDATE

@app.route("/edit/<int:patient_id>", methods=["GET", "POST"])
def edit(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        flash("Patient not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        data = {
            "full_name":   request.form.get("full_name", "").strip(),
            "dob":         request.form.get("dob", "").strip(),
            "email":       request.form.get("email", "").strip(),
            "glucose":     request.form.get("glucose", "").strip(),
            "haemoglobin": request.form.get("haemoglobin", "").strip(),
            "cholesterol": request.form.get("cholesterol", "").strip(),
        }

        errors = validate_form(data)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("edit.html", patient=data, patient_id=patient_id)

        remarks = get_health_prediction(
            float(data["glucose"]),
            float(data["haemoglobin"]),
            float(data["cholesterol"])
        )

        update_patient(
            patient_id,
            data["full_name"], data["dob"], data["email"],
            float(data["glucose"]), float(data["haemoglobin"]),
            float(data["cholesterol"]), remarks
        )

        flash(f"Patient <strong>{data['full_name']}</strong> updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", patient=patient, patient_id=patient_id)



# DELETE

@app.route("/delete/<int:patient_id>", methods=["POST"])
def delete(patient_id):
    patient = get_patient_by_id(patient_id)
    if patient:
        delete_patient(patient_id)
        flash(f"Patient <strong>{patient['full_name']}</strong> deleted.", "warning")
    return redirect(url_for("index"))



# VIEW DETAILS 

@app.route("/patient/<int:patient_id>")
def patient_detail(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(patient))


if __name__ == "__main__":
    app.run(debug=True)
