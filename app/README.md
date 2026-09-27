# Deep Learning Based Phishing Website Detection and Classification System

## 1. Project Overview

Phishing websites are malicious websites designed to deceive users and obtain sensitive information such as usernames, passwords, banking details, and other personal information.

This project presents a Deep Learning Based Phishing Website Detection and Classification System that analyzes website URLs and classifies them into two categories:

- Phishing Website
- Legitimate Website

The system extracts different URL-based features and uses a Deep Learning Neural Network to perform the classification. A Flask-based web interface allows users to enter a URL and receive an instant prediction with a confidence score.

---

## 2. Problem Statement

Phishing attacks are a major cybersecurity threat. Attackers often create URLs that look similar to legitimate websites and use them to deceive users.

The objective of this project is to develop an automated system that can analyze URL characteristics and identify whether a URL is likely to be phishing or legitimate.

---

## 3. Objectives

The main objectives of this project are:

1. To detect phishing websites using URL-based characteristics.
2. To extract useful features from website URLs.
3. To develop a Deep Learning classification model.
4. To evaluate the model using standard performance metrics.
5. To create a user-friendly web interface.
6. To provide real-time prediction and confidence scores.

---

## 4. Technologies Used

- Python
- TensorFlow
- Keras
- Pandas
- NumPy
- Scikit-learn
- Flask
- HTML
- CSS
- Visual Studio Code

---

## 5. Dataset

The project uses a phishing URL dataset containing legitimate and phishing URLs.

The dataset contains two classes:

- 0 = Phishing
- 1 = Legitimate

The dataset was divided into training and testing data using an 80:20 split.

---

## 6. URL Feature Extraction

The system extracts multiple features from each URL, including:

- URL length
- Number of dots
- Number of hyphens
- Number of underscores
- Number of slashes
- Number of question marks
- Number of equal signs
- Number of @ symbols
- Number of digits
- Number of alphabetic characters
- Number of special characters
- HTTPS presence
- IP address presence
- Suspicious keyword count
- Number of subdomains

These features are converted into numerical values and supplied to the Deep Learning model.

---

## 7. Deep Learning Model

A Feed-Forward Neural Network was developed using TensorFlow and Keras.

The architecture consists of:

```text
Input Layer
     ↓
Dense Layer - 64 neurons
     ↓
Dropout - 30%
     ↓
Dense Layer - 32 neurons
     ↓
Dropout - 20%
     ↓
Dense Layer - 16 neurons
     ↓
Output Layer - 1 neuron
```

The hidden layers use the ReLU activation function, while the output layer uses the Sigmoid activation function for binary classification.

The Adam optimizer and Binary Cross-Entropy loss function were used during training.

---

## 8. Model Training

The dataset was divided into:

- 80% Training Data
- 20% Testing Data

Feature scaling was performed using StandardScaler.

Early stopping was used during training to reduce unnecessary training when validation performance stopped improving.

---

## 9. Model Performance

The trained model achieved the following results on the test dataset:

| Metric | Score |
|---|---:|
| Accuracy | 96.77% |
| Precision | 94.67% |
| Recall | 99.12% |
| F1 Score | 96.84% |

### Confusion Matrix

```text
[[18883  1117]
 [  176 19824]]
```

These results are specific to the dataset and train/test split used in this project.

---

## 10. Web Application

A Flask-based web application was developed to provide an easy-to-use interface.

The user enters a website URL into the input field.

The system then:

1. Receives the URL.
2. Extracts URL-based features.
3. Scales the features.
4. Passes the features to the trained Deep Learning model.
5. Generates a prediction.
6. Displays the classification and confidence score.

### Example

**Input:**

`https://www.google.com`

**Output:**

**LEGITIMATE WEBSITE**

**Confidence:** 97.57%

---

## 11. Project Workflow

```text
User enters URL
       ↓
URL Preprocessing
       ↓
Feature Extraction
       ↓
Feature Scaling
       ↓
Deep Learning Neural Network
       ↓
Prediction
       ↓
Phishing / Legitimate
       ↓
Confidence Score
```

---

## 12. Project Structure

```text
Phishing-Website-Detection/
│
├── dataset/
│   └── phishing_url_dataset.csv
│
├── model/
│   ├── phishing_model.keras
│   ├── scaler_mean.npy
│   └── scaler_scale.npy
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
│
├── train_model.py
├── README.md
├── .gitignore
└── venv/
```

---

## 13. How to Run the Project

### Step 1: Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Step 2: Run the Flask Application

```bash
cd app
python app.py
```

### Step 3: Open the Application

Open the following address in a web browser:

```text
http://127.0.0.1:5000
```

### Step 4: Enter a URL

Enter a website URL in the input field and click:

**Check Website**

The system will display the predicted classification and confidence score.

---

## 14. Advantages

- Fast URL-based detection
- Automated classification
- Deep Learning based prediction
- Easy-to-use web interface
- Provides confidence score
- Requires no manual URL analysis

---

## 15. Limitations

- The model mainly relies on URL-based features.
- It does not inspect the complete webpage content.
- Performance may vary for URLs that are very different from the training data.
- A confidence score is a model output and does not guarantee that a website is safe.

---

## 16. Future Scope

The project can be extended by:

1. Using larger and more diverse datasets.
2. Applying LSTM or Transformer models to raw URLs.
3. Adding webpage-content analysis.
4. Adding domain and certificate-related features.
5. Creating browser-extension integration.
6. Continuously updating the model with new phishing patterns.
7. Deploying the application as a cloud-based cybersecurity service.

---

## 17. Conclusion

This project demonstrates a Deep Learning based approach for detecting phishing websites using URL characteristics.

The system extracts relevant URL features, processes them through a trained Neural Network, and classifies the URL as phishing or legitimate.

A Flask web application provides an interactive interface for URL classification.

The model achieved:

- Accuracy: 96.77%
- Precision: 94.67%
- Recall: 99.12%
- F1 Score: 96.84%

These results are based on the selected dataset and test split used during the project.

Further improvements can be made by incorporating webpage content, domain information, and more advanced Deep Learning techniques.

---

## 18. Author

**Mini Project**

**Project Title:** Deep Learning Based Phishing Website Detection and Classification System
