import pandas as pd
import numpy as np
import re
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


# ==============================
# 1. LOAD DATASET
# ==============================

print("Loading dataset...")

df = pd.read_csv("dataset/phishing_url_dataset.csv")

df = df.dropna(subset=["URL", "Label"])
df = df.drop_duplicates(subset=["URL"])

print("Dataset shape:", df.shape)
print("\nLabel distribution:")
print(df["Label"].value_counts())


# ==============================
# 2. FEATURE EXTRACTION
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

    # HTTPS present
    features.append(1 if url.lower().startswith("https") else 0)

    # IP address present
    ip_pattern = r"(?:\d{1,3}\.){3}\d{1,3}"
    features.append(1 if re.search(ip_pattern, url) else 0)

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
        word in url_lower for word in suspicious_words
    )

    features.append(keyword_count)

    # Number of subdomains
    try:
        domain_part = url.split("//")[-1].split("/")[0]
        subdomain_count = max(domain_part.count(".") - 1, 0)
    except:
        subdomain_count = 0

    features.append(subdomain_count)

    return features


print("\nExtracting URL features...")

X = np.array(
    [extract_features(url) for url in df["URL"]]
)

y = df["Label"].values

print("Feature matrix shape:", X.shape)


# ==============================
# 3. TRAIN TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==============================
# 4. FEATURE SCALING
# ==============================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# ==============================
# 5. DEEP LEARNING MODEL
# ==============================

print("\nBuilding Deep Learning model...")

model = Sequential([

    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),

    Dropout(0.3),

    Dense(32, activation="relu"),

    Dropout(0.2),

    Dense(16, activation="relu"),

    Dense(1, activation="sigmoid")
])


model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


model.summary()


# ==============================
# 6. TRAIN MODEL
# ==============================

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

print("\nTraining model...")

history = model.fit(
    X_train,
    y_train,
    validation_split=0.2,
    epochs=30,
    batch_size=128,
    callbacks=[early_stopping],
    verbose=1
)


# ==============================
# 7. PREDICTION
# ==============================

print("\nEvaluating model...")

y_probability = model.predict(X_test)

y_pred = (y_probability >= 0.5).astype(int).flatten()


# ==============================
# 8. EVALUATION
# ==============================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)

recall = recall_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred)

cm = confusion_matrix(y_test, y_pred)


print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

print("\nConfusion Matrix:")
print(cm)


# ==============================
# 9. SAVE MODEL
# ==============================

os.makedirs("model", exist_ok=True)

model.save("model/phishing_model.keras")

np.save("model/scaler_mean.npy", scaler.mean_)

np.save("model/scaler_scale.npy", scaler.scale_)

print("\nModel saved successfully!")
print("Location: model/phishing_model.keras")