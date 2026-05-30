import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_health_prediction(glucose: float, haemoglobin: float, cholesterol: float) -> str:
    """
    Calls Google Gemini AI with blood test values and returns a health prediction remark.
    Falls back to rule-based logic if the API is unavailable.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""You are a medical AI assistant. A patient has submitted the following blood test results:

- Glucose: {glucose} mg/dL  (Normal fasting range: 70–99 mg/dL)
- Haemoglobin: {haemoglobin} g/dL  (Normal: Men 13.5–17.5, Women 12–15.5 g/dL)
- Cholesterol: {cholesterol} mg/dL  (Desirable: <200 mg/dL)

Based on these values, write a concise health assessment in 2–3 sentences.
- Identify any abnormal values and the associated health risk.
- Suggest one simple lifestyle precaution.
- Do NOT recommend specific medications or dosages.
- Be professional, clear, and compassionate."""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception:
        return _rule_based_remark(glucose, haemoglobin, cholesterol)


def _rule_based_remark(glucose: float, haemoglobin: float, cholesterol: float) -> str:
    """Fallback when Gemini API is unavailable."""
    flags = []

    if glucose > 126:
        flags.append("elevated glucose levels suggesting possible diabetes")
    elif glucose > 100:
        flags.append("borderline glucose indicating pre-diabetic tendencies")
    elif glucose < 70:
        flags.append("low glucose indicating possible hypoglycaemia")

    if haemoglobin < 12:
        flags.append("low haemoglobin consistent with anaemia")
    elif haemoglobin > 17.5:
        flags.append("elevated haemoglobin which may warrant further evaluation")

    if cholesterol > 240:
        flags.append("high cholesterol posing significant cardiovascular risk")
    elif cholesterol > 200:
        flags.append("borderline high cholesterol requiring dietary attention")

    if flags:
        return (
            f"Patient presents with {', '.join(flags)}. "
            "It is recommended to consult a healthcare professional for a thorough evaluation. "
            "Adopting a balanced diet, regular physical activity, and routine monitoring can help manage these values."
        )
    return (
        "All blood test values are within normal reference ranges. "
        "The patient appears to be in good health based on these indicators. "
        "Continue maintaining a healthy lifestyle with regular check-ups."
    )
