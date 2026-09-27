from flask import Flask, render_template, request
import numpy as np
import re
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)

# ==============================
# LOAD TRAINED MODEL
# ==============================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "model",
    "phishing_model.keras"
)

SCALER_MEAN_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "model",
    "scaler_mean.npy"
)

SCALER_SCALE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "model",
    "scaler_scale.npy"
)

model = load_model(MODEL_PATH)

scaler_mean = np.load(SCALER_MEAN_PATH)
scaler_scale = np.load(SCALER_SCALE_PATH)


# ==============================
# FEATURE EXTRACTION
# ==============================

def extract_features(url):

    url = str(url)

    features = []

    # URL length
    features.append(len(url))

    # Number of dots
    features.append(url.count("."))

    # Number of hyphens
    features.append(url.count("-"))

    # Number of underscores
    features.append(url.count("_"))

    # Number of slashes
    features.append(url.count("/"))

    # Number of question marks
    features.append(url.count("?"))

    # Number of equal signs
    features.append(url.count("="))

    # Number of @ symbols
    features.append(url.count("@"))

    # Number of digits
    features.append(sum(c.isdigit() for c in url))

    # Number of letters
    features.append(sum(c.isalpha() for c in url))

    # Number of special characters
    features.append(
        sum(not c.isalnum() for c in url)
    )

    # HTTPS
    features.append(
        1 if url.lower().startswith("https") else 0
    )

    # IP address
    ip_pattern = r"(?:\d{1,3}\.){3}\d{1,3}"

    features.append(
        1 if re.search(ip_pattern, url) else 0
    )

    # Suspicious keywords
    suspicious_words = [
        "login",
        "verify",
        "update",
        "secure",
        "account",
        "bank",
        "signin",
        "password",
        "confirm",
        "verification"
    ]

    url_lower = url.lower()

    keyword_count = sum(
        word in url_lower
        for word in suspicious_words
    )

    features.append(keyword_count)

    # Subdomains
    try:

        domain_part = (
            url.split("//")[-1]
            .split("/")[0]
        )

        subdomain_count = max(
            domain_part.count(".") - 1,
            0
        )

    except:

        subdomain_count = 0

    features.append(subdomain_count)

    return features


# ==============================
# SCALE FEATURES
# ==============================

def scale_features(features):

    features = np.array(features, dtype=float)

    scaled = (
        features - scaler_mean
    ) / scaler_scale

    return scaled.reshape(1, -1)


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==============================
# PREDICTION
# ==============================

@app.route("/predict", methods=["POST"])
def predict():

    url = request.form.get("url", "").strip()

    if not url:

        return render_template(
            "index.html",
            error="Please enter a website URL."
        )

    # Extract features
    features = extract_features(url)

    # Scale features
    scaled_features = scale_features(
        features
    )

    # Model prediction
    probability = model.predict(
        scaled_features,
        verbose=0
    )[0][0]

    # Our dataset:
    # 0 = Phishing
    # 1 = Legitimate

    if probability >= 0.5:

        result = "LEGITIMATE"

        confidence = probability * 100

    else:

        result = "PHISHING"

        confidence = (1 - probability) * 100

    return render_template(
        "index.html",
        url=url,
        result=result,
        confidence=round(confidence, 2)
    )


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True
    )