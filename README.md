# AI Smart Based Surplus Food Redistribution System

A Flask-based smart surplus food redistribution system that connects **food donors, NGOs, volunteers, and administrators**. The application provides authentication, food donation intake, food-priority prediction, NGO food requests, volunteer delivery coordination, and administrator monitoring.

The system uses a **Random Forest machine-learning model** to analyze surplus-food information and classify donation urgency as **Low, Medium, High, or Critical**.

---

# Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [User Roles](#user-roles)
5. [System Workflow](#system-workflow)
6. [Technology Stack](#technology-stack)
7. [Prerequisites](#prerequisites)
8. [Backend Setup](#backend-setup)
9. [Virtual Environment](#virtual-environment)
10. [Install Dependencies](#install-dependencies)
11. [Train the AI Model](#train-the-ai-model)
12. [Run Automated Tests](#run-automated-tests)
13. [Run the Backend](#run-the-backend)
14. [Run the Frontend](#run-the-frontend)
15. [Run the Complete Project](#run-the-complete-project)
16. [Demo Accounts](#demo-accounts)
17. [Database](#database)
18. [Reset Database](#reset-database)
19. [AI Food Priority Ranking](#ai-food-priority-ranking)
20. [Priority Prediction Inputs](#priority-prediction-inputs)
21. [Explanation of Inputs](#explanation-of-inputs)
22. [Priority Levels](#priority-levels)
23. [Priority Test Inputs](#priority-test-inputs)
24. [Expiry-Time Demonstration](#expiry-time-demonstration)
25. [Prediction API](#prediction-api)
26. [Testing the Prediction API](#testing-the-prediction-api)
27. [Authentication](#authentication)
28. [Automated Tests](#automated-tests)
29. [Important Files](#important-files)
30. [Troubleshooting](#troubleshooting)
31. [Useful Commands](#useful-commands)
32. [Current Project Verification](#current-project-verification)
33. [Project Objective](#project-objective)
34. [Final Technology Summary](#final-technology-summary)

---

# Project Overview

The **AI Smart Based Surplus Food Redistribution System** is a web-based application designed to improve the redistribution of surplus food.

The system connects:

```text
Food Donors
     ↓
Surplus Food Donations
     ↓
Food Priority Analysis
     ↓
NGOs / Organizations
     ↓
Volunteers
     ↓
People in Need
```

The backend is developed using **Flask**, the database uses **SQLite**, and the frontend uses **HTML, CSS, and JavaScript**.

The system also contains a machine-learning component that uses a **Random Forest Classifier** to analyze food donation information and determine its urgency.

---

# Project Structure

```text
AI-Smart-Based-Surplus-Food-Redistribution-System-main/
│
├── backend/
│   │
│   ├── app.py
│   ├── extensions.py
│   ├── models.py
│   ├── seed.py
│   ├── requirements.txt
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── donations.py
│   │   ├── ngo.py
│   │   ├── volunteer.py
│   │   ├── delivery.py
│   │   ├── admin.py
│   │   ├── analytics.py
│   │   └── notifications.py
│   │
│   ├── ml/
│   │   ├── train_model.py
│   │   ├── predict.py
│   │   ├── training_data.csv
│   │   ├── food_priority_model.pkl
│   │   └── model_metadata.json
│   │
│   ├── tests/
│   │   ├── test_auth_roles.py
│   │   └── test_food_priority.py
│   │
│   └── instance/
│       └── SQLite database
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── donate.html
│   ├── need_food.html
│   ├── ngo_dashboard.html
│   ├── script.js
│   └── style.css
│
└── README.md
```

---

# Features

## Food Donor / Individual

Food donors can:

* Register an account
* Login
* Enter food donation details
* Donate surplus food
* Enter quantity
* Enter expiry information
* Provide food type
* Provide food category
* Provide storage condition
* View donation information
* Receive food-priority analysis

---

## NGO / Organization

NGOs can:

* Register/login
* View available food donations
* Request food
* Claim suitable donations
* Coordinate redistribution
* Track food requests
* Coordinate with volunteers

---

## Volunteer

Volunteers can:

* Login
* View delivery assignments
* Coordinate food pickup
* Coordinate food delivery
* Update delivery status

---

## Administrator

Administrators can:

* Login
* Monitor users
* Monitor donations
* Monitor NGO requests
* Monitor deliveries
* View analytics
* Monitor system activity

---

## AI Food Priority Analysis

The system includes an AI-based food-priority prediction feature.

The Random Forest model predicts:

```text
Low
Medium
High
Critical
```

The prediction considers:

```text
Expiry Hours
Quantity
Food Type
Donation Age
Storage Condition
Food Category
```

---

# User Roles

The frontend provides these main role options:

```text
Food Donor / Individual
NGO / Organization
Administrator
```

The backend also supports the volunteer workflow.

The backend normalizes donor-related role values when required so that role handling remains consistent.

---

# System Workflow

```text
                  FOOD DONOR
                      │
                      │ Donate Food
                      ▼
              ┌───────────────┐
              │ Flask Backend │
              └───────────────┘
                      │
                      ▼
             Food Priority Analysis
                      │
                      ▼
              Random Forest Model
                      │
              ┌───────┴────────┐
              ▼                ▼
          Priority         Confidence
              │
              ▼
          Food Donation
              │
              ▼
              NGO
              │
              │ Request / Claim
              ▼
           Volunteer
              │
              │ Pickup & Delivery
              ▼
        People in Need
```

---

# Technology Stack

## Frontend

* HTML
* CSS
* JavaScript

## Backend

* Python 3.10+
* Flask
* Flask-SQLAlchemy
* Flask-JWT-Extended
* Flask-CORS

## Database

* SQLite

## Machine Learning

* scikit-learn
* pandas
* joblib
* RandomForestClassifier
* ColumnTransformer
* OneHotEncoder

---

# Prerequisites

Install the following before running the project:

* Python 3.10 or newer
* pip
* PowerShell or terminal
* Modern web browser

Check Python:

```powershell
python --version
```

or:

```powershell
py --version
```

Check pip:

```powershell
python -m pip --version
```

---

# Backend Setup

The backend is located inside:

```text
backend/
```

Go to the backend:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"
```

---

# Virtual Environment

From the project root:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"
```

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

After successful activation, PowerShell should show:

```text
(.venv) PS D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main>
```

---

# PowerShell Execution Policy

If PowerShell blocks the virtual-environment activation script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

The `Process` scope means the policy applies only to the current PowerShell session.

---

# Install Dependencies

From the project root:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

---

# Train the AI Model

The AI food-priority model must be trained before using the food-priority prediction feature.

From the project root:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"

.\.venv\Scripts\Activate.ps1

python backend\ml\train_model.py
```

Alternatively:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1

python ml/train_model.py
```

The training process creates or updates:

```text
backend/ml/food_priority_model.pkl
backend/ml/model_metadata.json
backend/ml/training_data.csv
```

---

# Current Model Training Result

The model has been successfully trained in the current project setup.

Current validation accuracy:

```text
0.8750
```

This corresponds to:

```text
87.5% validation accuracy
```

Successful training output is similar to:

```text
Model trained and saved to D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend\ml\food_priority_model.pkl
Dataset saved to D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend\ml\training_data.csv
Validation accuracy: 0.8750
```

> The validation accuracy may change if the training dataset, random seed, preprocessing, or model configuration is changed.

---

# Run Automated Tests

From the project root:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

Current test result:

```text
....                                                                    [100%]
4 passed in 4.26s
```

Therefore:

```text
4 tests passed
0 tests failed
```

> Run the test suite before starting Flask. The current test fixtures reset the local SQLite database; if Flask is already running, restart it after testing so the database tables and demo accounts are recreated.

---

# Run the Backend

Open **Terminal 1**.

Go to the backend:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start Flask:

```powershell
cd backend
python app.py
```

The Flask backend runs at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

Keep this terminal running.

---

# Run the Frontend

Open **Terminal 2**.

Go to the project:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"
```

Activate the virtual environment if required:

```powershell
.\.venv\Scripts\Activate.ps1
```

Go to the frontend:

```powershell
cd frontend
```

Start the frontend server:

```powershell
python -m http.server 8000
```

Successful output:

```text
Serving HTTP on :: port 8000
```

The frontend is available at:

```text
http://localhost:8000
```

You may also see:

```text
http://[::]:8000/
```

in PowerShell. This is normal.

Open the following in your browser:

```text
http://localhost:8000
```

Keep this terminal running.

---

# Complete Project Run

The project uses two terminals.

## Terminal 1 — Flask Backend

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1

python app.py
```

Backend:

```text
http://127.0.0.1:5000
```

---

## Terminal 2 — Frontend

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"

.\.venv\Scripts\Activate.ps1

cd frontend

python -m http.server 8000
```

Frontend:

```text
http://localhost:8000
```

---

# Demo Accounts

The project provides demo accounts for testing.

| Role      | Email                   | Password        |
| --------- | ----------------------- | --------------- |
| Donor     | `donor@example.com`     | `Donor@123`     |
| NGO       | `ngo@example.com`       | `Ngo@123`       |
| Volunteer | `volunteer@example.com` | `Volunteer@123` |
| Admin     | `admin@example.com`     | `Admin@123`     |

These accounts can be used to test the different role-based workflows.

---

# Seed Demo Data

The project includes a seed script.

From the backend folder:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1

python seed.py
```

Successful output should be similar to:

```text
Created donor: donor@example.com
Created ngo: ngo@example.com
Created volunteer: volunteer@example.com
Created admin: admin@example.com
Seed completed.
```

---

# Database

The project uses **SQLite**.

SQLite is used because it:

* Does not require a separate database server
* Is lightweight
* Is easy to configure
* Is suitable for local development
* Stores the database in a local file

The database is created inside:

```text
backend/instance/
```

The database is managed through:

```text
Flask-SQLAlchemy
```

---

# Reset Database

If you need to start with a clean database:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1
```

Remove `.db` files:

```powershell
Remove-Item -Force -ErrorAction SilentlyContinue ..\instance\*.db
```

Remove `.sqlite` files:

```powershell
Remove-Item -Force -ErrorAction SilentlyContinue ..\instance\*.sqlite
```

Remove `.sqlite3` files:

```powershell
Remove-Item -Force -ErrorAction SilentlyContinue ..\instance\*.sqlite3
```

Then recreate demo accounts:

```powershell
python seed.py
```

---

# AI Food Priority Ranking

The project contains an AI-based food-priority feature.

The model predicts the urgency of a food donation as:

```text
Low
Medium
High
Critical
```

---

# Model Used

The machine-learning algorithm is:

```text
RandomForestClassifier
```

Library:

```text
scikit-learn
```

Preprocessing:

```text
ColumnTransformer
+
OneHotEncoder
```

Training file:

```text
backend/ml/train_model.py
```

Prediction file:

```text
backend/ml/predict.py
```

Saved model:

```text
backend/ml/food_priority_model.pkl
```

---

# Why Random Forest?

Random Forest is suitable for this project because it:

* Works well with tabular data
* Handles numerical features
* Can handle categorical features after preprocessing
* Captures nonlinear relationships
* Combines multiple decision trees
* Works well with small-to-medium datasets
* Provides class probabilities that can be used as confidence information

---

# AI Model Workflow

Training:

```text
Training Dataset
       ↓
Data Preprocessing
       ↓
ColumnTransformer
       ↓
OneHotEncoder
       ↓
Random Forest Classifier
       ↓
Trained Model
       ↓
food_priority_model.pkl
```

Prediction:

```text
Food Donation Details
       ↓
Input Validation
       ↓
Preprocessing
       ↓
Random Forest Model
       ↓
Priority Prediction
       ↓
Confidence / Probabilities
```

---

# Priority Prediction Inputs

The Random Forest model uses the following six features:

| Input                | Type   | Example            | Meaning                       |
| -------------------- | ------ | ------------------ | ----------------------------- |
| `expiry_hours`       | Number | `2`                | Hours remaining before expiry |
| `quantity`           | Number | `10`               | Amount of food being donated  |
| `food_type`          | Text   | `"cooked"`         | Type/form of food             |
| `donation_age_hours` | Number | `1`                | Age of the donation/food      |
| `storage_condition`  | Text   | `"refrigerated"`   | How the food has been stored  |
| `food_category`      | Text   | `"non_vegetarian"` | Food category                 |

---

# Required API Inputs

The API requires these four fields:

```text
expiry_hours
quantity
food_type
donation_age_hours
```

Example:

```json
{
  "expiry_hours": 2,
  "quantity": 10,
  "food_type": "cooked",
  "donation_age_hours": 1
}
```

The model also supports:

```text
storage_condition
food_category
```

For a complete prediction request, all six features should be provided.

---

# Explanation of Inputs

## expiry_hours

`expiry_hours` represents how many hours are remaining before the food expires.

Examples:

```text
1 hour
2 hours
4 hours
6 hours
12 hours
24 hours
48 hours
72 hours
```

General relationship:

```text
Less time before expiry
        ↓
Greater urgency
        ↓
Higher redistribution priority
```

For example:

```text
Expires in 2 hours  → very urgent
Expires in 12 hours → moderately urgent
Expires in 24 hours → less urgent
Expires in 72 hours → low urgency
```

The exact final priority is determined by the trained Random Forest model.

---

## quantity

`quantity` represents the amount of food available for redistribution.

Examples:

```text
5
10
20
50
100
200
```

Quantity provides the model with information about the amount of food involved in the donation.

---

## food_type

`food_type` describes the type or form of the food.

Examples include:

```text
cooked
packaged
fresh
raw
```

The values used in the frontend should match the categories represented in the training data.

---

## donation_age_hours

`donation_age_hours` represents how many hours old the food donation is.

Examples:

```text
1
2
5
8
12
```

Older donations can require faster attention depending on their expiry time and storage condition.

---

## storage_condition

`storage_condition` describes how the food has been stored.

Examples:

```text
refrigerated
frozen
dry
room_temperature
```

Storage condition is one of the features considered by the trained model.

---

## food_category

`food_category` describes the category of the food.

Examples:

```text
rice
meals
vegetarian
non_vegetarian
snacks
biscuits
```

The exact category values should match the categories present in the training dataset.

---

# Complete Prediction Input

A complete request can look like this:

```json
{
  "expiry_hours": 2,
  "quantity": 10,
  "food_type": "cooked",
  "donation_age_hours": 1,
  "storage_condition": "refrigerated",
  "food_category": "non_vegetarian"
}
```

---

# Priority Levels

The model can return four priority classes:

| Priority     | Meaning                                               |
| ------------ | ----------------------------------------------------- |
| **Critical** | Requires immediate attention                          |
| **High**     | Requires fast redistribution                          |
| **Medium**   | Should be redistributed within a reasonable timeframe |
| **Low**      | Less urgent compared with other donations             |

---

# Priority Test Inputs

These examples can be used to test the food-priority feature.

> The expected categories below are demonstration expectations. The actual result is produced by the trained Random Forest model.

---

## Test 1 — Extremely Urgent

```json
{
  "expiry_hours": 1,
  "quantity": 20,
  "food_type": "cooked",
  "donation_age_hours": 8,
  "storage_condition": "refrigerated",
  "food_category": "rice"
}
```

Expected urgency:

```text
High / Critical
```

---

## Test 2 — Urgent

```json
{
  "expiry_hours": 4,
  "quantity": 50,
  "food_type": "cooked",
  "donation_age_hours": 5,
  "storage_condition": "refrigerated",
  "food_category": "meals"
}
```

Expected urgency:

```text
High / Critical
```

---

## Test 3 — Medium Urgency

```json
{
  "expiry_hours": 12,
  "quantity": 30,
  "food_type": "cooked",
  "donation_age_hours": 3,
  "storage_condition": "refrigerated",
  "food_category": "rice"
}
```

Expected urgency:

```text
Medium / High
```

---

## Test 4 — Lower Urgency

```json
{
  "expiry_hours": 24,
  "quantity": 20,
  "food_type": "cooked",
  "donation_age_hours": 2,
  "storage_condition": "refrigerated",
  "food_category": "vegetarian"
}
```

Expected urgency:

```text
Medium / Low
```

---

## Test 5 — Low Urgency

```json
{
  "expiry_hours": 48,
  "quantity": 10,
  "food_type": "packaged",
  "donation_age_hours": 1,
  "storage_condition": "dry",
  "food_category": "snacks"
}
```

Expected urgency:

```text
Low
```

---

## Test 6 — Very Low Urgency

```json
{
  "expiry_hours": 72,
  "quantity": 5,
  "food_type": "packaged",
  "donation_age_hours": 1,
  "storage_condition": "dry",
  "food_category": "biscuits"
}
```

Expected urgency:

```text
Low
```

---

# Expiry-Time Demonstration

To demonstrate the effect of expiry time, keep the other inputs the same and change only `expiry_hours`.

| Test | Expiry Hours | Quantity | Donation Age | General Urgency   |
| ---- | -----------: | -------: | -----------: | ----------------- |
| 1    |          `1` |     `20` |          `2` | Extremely urgent  |
| 2    |          `4` |     `20` |          `2` | Urgent            |
| 3    |          `8` |     `20` |          `2` | Moderately urgent |
| 4    |         `12` |     `20` |          `2` | Medium            |
| 5    |         `24` |     `20` |          `2` | Lower             |
| 6    |         `48` |     `20` |          `2` | Low               |
| 7    |         `72` |     `20` |          `2` | Very low          |

The general concept is:

```text
Expiry time decreases
        ↓
Food becomes more urgent
        ↓
Priority generally increases
        ↓
Faster redistribution is needed
```

The actual prediction is determined by the trained model rather than by a manually programmed expiry-hours rule.

---

# Food Priority API

The backend provides the following endpoint:

```http
POST /api/food-priority/predict
```

---

# Example API Request

```json
{
  "expiry_hours": 2,
  "quantity": 10,
  "food_type": "cooked",
  "donation_age_hours": 1,
  "storage_condition": "refrigerated",
  "food_category": "non_vegetarian"
}
```

---

# Example API Response

```json
{
  "success": true,
  "priority": "Critical",
  "confidence": 0.91,
  "probabilities": {
    "Critical": 0.91,
    "High": 0.06,
    "Medium": 0.02,
    "Low": 0.01
  }
}
```

The actual response depends on the trained model and input values.

---

# How the Prediction Feature Works

```text
Donor enters donation details
            ↓
Frontend collects input
            ↓
JavaScript sends POST request
            ↓
Flask API
            ↓
Input validation
            ↓
ml/predict.py
            ↓
Random Forest model
            ↓
Priority prediction
            ↓
Confidence/probabilities
            ↓
Frontend displays result
```

---

# Testing the Prediction API with PowerShell

Start the Flask backend first:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1

python app.py
```

Open another PowerShell terminal.

Create the request body:

```powershell
$body = @{
    expiry_hours = 2
    quantity = 10
    food_type = "cooked"
    donation_age_hours = 1
    storage_condition = "refrigerated"
    food_category = "non_vegetarian"
} | ConvertTo-Json
```

Send the request:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/api/food-priority/predict" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

The response should contain:

```text
success
priority
confidence
probabilities
```

---

# Testing Different Priority Inputs

To test multiple cases, change the values in:

```powershell
$body = @{
    expiry_hours = 1
    quantity = 20
    food_type = "cooked"
    donation_age_hours = 8
    storage_condition = "refrigerated"
    food_category = "rice"
} | ConvertTo-Json
```

Then send:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/api/food-priority/predict" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

Repeat with different `expiry_hours`, quantity, food type, donation age, storage condition, and category values.

---

# Testing Missing Inputs

The API requires:

```text
expiry_hours
quantity
food_type
donation_age_hours
```

For example:

```json
{
  "expiry_hours": 2,
  "quantity": 10
}
```

The API should return an error similar to:

```json
{
  "success": false,
  "error": "Missing required fields: food_type, donation_age_hours"
}
```

This confirms that backend input validation is working.

---

# Authentication

The system uses:

```text
Flask-JWT-Extended
```

for JWT authentication.

Basic authentication workflow:

```text
Register
   ↓
Login
   ↓
Backend verifies credentials
   ↓
JWT token generated
   ↓
Token used for protected requests
```

The application also uses role-based access control.

---

# Role-Based Access Control

Different users have different responsibilities.

```text
Donor
  ↓
Create food donations

NGO
  ↓
Request / claim food

Volunteer
  ↓
Manage deliveries

Admin
  ↓
Monitor system
```

Protected backend routes use role-based authorization where required.

---

# Backend API Areas

The Flask backend contains routes for:

```text
Authentication
Donations
Food Priority
NGO Requests
Volunteer
Delivery
Admin
Analytics
Notifications
```

These routes are located in:

```text
backend/routes/
```

---

# Database Models

The database uses:

```text
Flask-SQLAlchemy
```

with:

```text
SQLite
```

The database models are defined in:

```text
backend/models.py
```

The database stores application information such as:

* Users
* Food donations
* NGO requests
* Deliveries
* Related system information

---

# Automated Tests

Run all tests:

```powershell
python -m pytest -q
```

Current verified result:

```text
4 passed
```

Specific authentication and role tests:

```powershell
python -m pytest tests/test_auth_roles.py -q
```

Specific food-priority tests:

```powershell
python -m pytest tests/test_food_priority.py -q
```

---

# Important Files

| File                                 | Purpose                         |
| ------------------------------------ | ------------------------------- |
| `backend/app.py`                     | Starts Flask application        |
| `backend/extensions.py`              | Flask extensions                |
| `backend/models.py`                  | Database models                 |
| `backend/seed.py`                    | Creates demo data               |
| `backend/routes/auth.py`             | Authentication                  |
| `backend/routes/donations.py`        | Donation APIs                   |
| `backend/routes/ngo.py`              | NGO functionality               |
| `backend/routes/volunteer.py`        | Volunteer functionality         |
| `backend/routes/delivery.py`         | Delivery functionality          |
| `backend/routes/admin.py`            | Admin functionality             |
| `backend/routes/analytics.py`        | Analytics                       |
| `backend/routes/notifications.py`    | Notifications                   |
| `backend/ml/train_model.py`          | Trains Random Forest model      |
| `backend/ml/predict.py`              | Makes food-priority predictions |
| `backend/ml/training_data.csv`       | Training dataset                |
| `backend/ml/food_priority_model.pkl` | Saved trained model             |
| `backend/ml/model_metadata.json`     | Model metadata                  |
| `frontend/index.html`                | Home page                       |
| `frontend/login.html`                | Login page                      |
| `frontend/register.html`             | Registration page               |
| `frontend/donate.html`               | Donation page                   |
| `frontend/dashboard.html`            | User dashboard                  |
| `frontend/ngo_dashboard.html`        | NGO dashboard                   |
| `frontend/need_food.html`            | Food request page               |
| `frontend/script.js`                 | Frontend JavaScript             |
| `frontend/style.css`                 | Frontend styling                |

---

# Troubleshooting

## PowerShell Activation Error

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Flask Backend Is Not Running

Start it with:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1

python app.py
```

Then check:

```text
http://127.0.0.1:5000/api/health
```

---

## Frontend Is Not Running

Start the frontend with:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\frontend"

python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

---

## AI Model Not Found

Train the model again:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"

.\.venv\Scripts\Activate.ps1

python backend\ml\train_model.py
```

---

## Database Problems

Reset the database:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1

Remove-Item -Force -ErrorAction SilentlyContinue ..\instance\*.db

Remove-Item -Force -ErrorAction SilentlyContinue ..\instance\*.sqlite

Remove-Item -Force -ErrorAction SilentlyContinue ..\instance\*.sqlite3

python seed.py
```

---

# Useful Commands

## Activate Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Train AI Model

```powershell
python backend\ml\train_model.py
```

---

## Run Tests

```powershell
python -m pytest -q
```

---

## Seed Database

```powershell
cd backend
python seed.py
```

---

## Start Backend

```powershell
cd backend
python app.py
```

---

## Start Frontend

```powershell
cd frontend
python -m http.server 8000
```

---

# Quick Command Reference

| Task                 | Command                            |
| -------------------- | ---------------------------------- |
| Activate environment | `.\.venv\Scripts\Activate.ps1`     |
| Train AI model       | `python backend\ml\train_model.py` |
| Run all tests        | `python -m pytest -q`              |
| Seed database        | `python backend\seed.py`           |
| Start Flask          | `python backend\app.py`            |
| Start frontend       | `python -m http.server 8000`       |

---

# First-Time Setup — Complete Command Sequence

Run these commands in order.

### 1. Go to project root

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"
```

### 2. Create virtual environment

```powershell
py -m venv .venv
```

### 3. Activate virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r backend\requirements.txt
```

### 5. Train AI model

```powershell
python backend\ml\train_model.py
```

### 6. Run tests

```powershell
python -m pytest -q
```

### 7. Seed demo accounts

```powershell
cd backend
python seed.py
```

### 8. Start backend

```powershell
python app.py
```

### 9. Open a second terminal

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"
```

### 10. Activate environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 11. Start frontend

```powershell
cd frontend
python -m http.server 8000
```

### 12. Open website

```text
http://localhost:8000
```

---

# Daily Run Commands

Once the project has already been installed, you do not need to recreate the virtual environment every time.

## Terminal 1

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\backend"

.\.venv\Scripts\Activate.ps1

python app.py
```

## Terminal 2

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main\frontend"

python -m http.server 8000
```

Open:

```text
http://localhost:8000
```

---

# Current Project Verification

The following commands have been successfully tested in the current project setup:

```powershell
cd "D:\AI-Smart-Based-Surplus-Food-Redistribution-System-main"

.\.venv\Scripts\Activate.ps1

python backend\ml\train_model.py

python -m pytest -q
```

Current results:

```text
AI Model:
TRAINED SUCCESSFULLY

Validation accuracy:
0.8750

Equivalent:
87.5%

Automated Tests:
4 passed
0 failed
```

The frontend has also been successfully started with:

```powershell
cd frontend
python -m http.server 8000
```

Successful output:

```text
Serving HTTP on :: port 8000
```

---

# Important Ports

| Component     |   Port | Address                 |
| ------------- | -----: | ----------------------- |
| Flask Backend | `5000` | `http://127.0.0.1:5000` |
| Frontend      | `8000` | `http://localhost:8000` |

---

# Project Objective

The main objective of the project is to reduce food wastage by providing a platform that connects food donors with organizations and volunteers involved in food redistribution.

The system provides:

```text
Food Donation
      ↓
Food Information
      ↓
Priority Analysis
      ↓
NGO Request
      ↓
Volunteer Delivery
      ↓
Redistribution
```

The AI priority feature helps identify donations that require greater attention based on the information provided by the donor.

---

# AI Priority Analysis Summary

The Random Forest model receives:

```text
expiry_hours
quantity
food_type
donation_age_hours
storage_condition
food_category
```

The model processes these features and produces:

```text
Priority
Confidence
Probabilities
```

Example:

```text
Food Donation
      │
      ├── Expiry: 2 hours
      ├── Quantity: 10
      ├── Food Type: Cooked
      ├── Donation Age: 1 hour
      ├── Storage: Refrigerated
      └── Category: Non-Vegetarian
                │
                ▼
        Random Forest Model
                │
                ▼
        Priority: Critical
        Confidence: 91%
```

The actual result is determined by the trained model.

---

# Final Technology Summary

```text
                 WEB APPLICATION
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
      FRONTEND                     BACKEND
          │                           │
      HTML/CSS/JS                   Python
                                  Flask
                                  SQLAlchemy
                                  JWT
                                  CORS
          │                           │
          └─────────────┬─────────────┘
                        │
                        ▼
                    DATABASE
                        │
                      SQLite
                        │
                        ▼
               MACHINE LEARNING
                        │
                 scikit-learn
                        │
              RandomForestClassifier
                        │
             ColumnTransformer
                        │
                 OneHotEncoder
                        │
                        ▼
               Food Priority
                        │
            ┌───────────┼───────────┐
            ▼           ▼           ▼
          Low        Medium       High
                        │
                        ▼
                     Critical
```

---

# Project Status

Current verified project status:

* ✅ Flask backend
* ✅ SQLite database
* ✅ Flask-SQLAlchemy
* ✅ JWT authentication
* ✅ Role-based access control
* ✅ Food donor workflow
* ✅ NGO workflow
* ✅ Volunteer workflow
* ✅ Admin workflow
* ✅ Food donation workflow
* ✅ Random Forest food-priority model
* ✅ Food-priority prediction API
* ✅ Model training successful
* ✅ 87.5% current validation accuracy
* ✅ Automated tests passing
* ✅ 4/4 tests passed
* ✅ Frontend static server working
* ✅ Frontend runs on port `8000`
* ✅ Flask backend runs on port `5000`
* ✅ Demo accounts available
* ✅ SQLite database seeding available

---

# License

This project is developed for **educational and academic purposes**.
