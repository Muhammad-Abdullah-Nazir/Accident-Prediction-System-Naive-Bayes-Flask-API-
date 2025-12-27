# Accident Prediction System (Naive Bayes + Flask API)

This project is a **rule-based Naive Bayes accident prediction system** implemented using **Python and Flask**.
It predicts whether an **accident is likely to occur** based on driving conditions such as **weather, road condition, traffic, and engine status**.

The system exposes a **REST API** that returns:

* Accident prediction (Yes / No)
* Probability percentages
* Confidence score
* Detailed probability breakdown

---

## Project Objective

* Apply **Naive Bayes probability theory** on a small dataset
* Build a **backend prediction API** using Flask
* Understand **conditional probability and prior probability**
* Serve predictions in **JSON format**

---

## Technologies Used

* Python 3
* Flask
* Flask-CORS
* Naive Bayes (rule-based implementation)
* JSON

---

## Dataset Summary

The probabilities are derived from a manually created dataset:

| Category       | Count | Percentage |
| -------------- | ----- | ---------- |
| Accident (Yes) | 4     | 40%        |
| Safe (No)      | 6     | 60%        |
| Total Records  | 10    | 100%       |

---

## Features Used for Prediction

| Feature        | Possible Values     |
| -------------- | ------------------- |
| Weather        | Rain, Snow, Clear   |
| Road Condition | Good, Bad, Average  |
| Traffic        | High, Normal, Light |
| Engine Problem | Yes, No             |

Laplace smoothing is applied where probabilities were zero in the dataset.

---

## How Prediction Works (Naive Bayes)

The model calculates:

```
P(Accident | Conditions) proportional to
P(Weather | Accident) ×
P(Road | Accident) ×
P(Traffic | Accident) ×
P(Engine | Accident) ×
P(Accident)
```

The same calculation is done for **No Accident**, and the larger probability determines the prediction.

---

## API Endpoints

### Home

GET /

```
http://localhost:5000/
```

Returns server status and dataset summary.

---

### Predict Accident

POST /predict

#### Request Body (JSON):

```json
{
  "weather": "Rain",
  "road": "Bad",
  "traffic": "High",
  "engine": "Yes"
}
```

#### Response:

```json
{
  "prediction": "YES - Accident Likely",
  "confidence": 87.45,
  "prob_yes_percent": 87.45,
  "prob_no_percent": 12.55,
  "breakdown": {
    "weather": { "p_yes": 0.25, "p_no": 0.333 },
    "road": { "p_yes": 0.5, "p_no": 0.167 },
    "traffic": { "p_yes": 0.75, "p_no": 0.167 },
    "engine": { "p_yes": 0.5, "p_no": 0.333 }
  }
}
```

---

## How to Run the Project

### Install Dependencies

```bash
pip install flask flask-cors
```

### Run the Server

```bash
python app.py
```

### Access API

```
http://localhost:5000
```

---

## Project Structure

```
├── app.py
├── README.md
```

---

## Key Highlights

* Uses Bayes Theorem
* No machine learning training required
* Lightweight and fast
* Easy integration with frontend applications
* Transparent probability calculations

---

## Use Cases

* Accident risk estimation
* Educational AI and statistics projects
* Backend API development practice
* Smart traffic system prototypes

---

## Learning Outcomes

* Practical understanding of Naive Bayes
* Hands-on experience with conditional probability
* REST API development using Flask
* Serving AI logic via JSON

---

## Author

**Muhammad Abdullah Nazir**
AI | Machine Learning | Python | Flask

---

