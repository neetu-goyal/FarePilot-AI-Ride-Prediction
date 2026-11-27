# 🚖 FarePilot-AI-Ride-Predition

### Machine Learning | Python | FastAPI | Streamlit

## 📌 About the Project

Uber Fare Prediction & Smart Ride Estimation System is an end-to-end Machine Learning application developed to estimate ride fares using trip-related information.

The application allows users to select their country, pickup location, drop-off location, and vehicle type (Bike or Car) to obtain an estimated ride fare.

The project combines Data Science, Machine Learning, Backend API Development, and Interactive Frontend Development to create a complete ride fare estimation system.

The trained Machine Learning model is integrated with FastAPI, while Streamlit provides an interactive user interface.

## 🎯 Project Objectives

- Analyze ride booking data and identify important fare-related patterns.
- Perform data cleaning and exploratory data analysis (EDA).
- Apply feature engineering to improve model performance.
- Train and compare different Machine Learning regression models.
- Evaluate model performance using regression metrics.
- Integrate the trained model with FastAPI.
- Develop an interactive Streamlit application for fare estimation.

## ✨ Key Features

- **Location Selection:** Select pickup and destination locations.
- **Multiple Vehicle Options:** Choose between Bike and Car.
- **Fare Estimation:** Predict estimated ride fares using the trained ML model and configured fare logic.
- **Country Selection:** Support for country-based selection and currency display, as implemented.
- **Interactive Frontend:** User-friendly Streamlit interface.
- **REST API:** FastAPI backend for prediction requests.
- **API Documentation:** Swagger UI for testing API endpoints.
- **Saved ML Model:** Trained model stored in a `.pkl` file.

## 🧠 Machine Learning Approach

The project follows an end-to-end Machine Learning workflow:

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis
4. Feature Engineering
5. Data Preprocessing
6. Model Training
7. Model Comparison
8. Model Evaluation
9. Model Saving
10. API Integration

### Algorithms Used

- Linear Regression
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor (if implemented)

### Model Evaluation Metrics

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Backend Framework | FastAPI |
| Frontend Framework | Streamlit |
| API Documentation | Swagger UI |
| Model Serialization | Pickle |
| Development Tools | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |

## 📂 Project Structure

```text
Uber-Fare-Prediction/
│
├── app/
│   ├── main.py
│   ├── crud.py
│   └── model.py
│
├── data/
│   └── uber_trips_dataset_50k.csv
│
├── models/
│   └── uber_fare_model.pkl
│
├── notebooks/
│   └── uber_fare_prediction.ipynb
│
├── frontend.py
│
├── requirements.txt
│
└── README.md
```

*Note: File names and locations should match the actual repository. Add `__init__.py` if your app uses it.*

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project folder:

```bash
cd Uber-Fare-Prediction
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment.

**For macOS / Linux:**

```bash
source .venv/bin/activate
```

**For Windows:**

```bash
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

### Step 5: Start the Streamlit Frontend

Open a second terminal and activate the virtual environment.

Run:

```bash
streamlit run frontend.py
```

Frontend URL:

http://localhost:8501

## 🔄 Application Workflow

1. Open the Streamlit application.
2. Select the country.
3. Enter or select the pickup location.
4. Select the destination location.
5. Choose the vehicle type (Bike or Car).
6. Submit the ride details.
7. The frontend communicates with the FastAPI backend.
8. The trained model processes the prediction request.
9. The estimated fare is displayed to the user.

## 📈 Project Highlights

- End-to-end Machine Learning project.
- Regression-based fare prediction.
- Model serialization using Pickle.
- Backend development using FastAPI.
- Interactive frontend using Streamlit.
- API integration and testing.
- Practical implementation of Data Science concepts.

## 🔮 Future Enhancements

- Real-time traffic data integration.
- Advanced map-based location selection.
- Additional vehicle categories.
- Database integration for ride history.
- Cloud deployment and public live demo.
- Further model optimization using real-world ride data.

## ⚠️ Disclaimer

This project is an educational Machine Learning application. The displayed fares are estimates based on the trained model and application logic. They are not official Uber prices and may differ from actual ride charges.

## 👩‍💻 Author

Developed as a Data Science and Machine Learning portfolio project to demonstrate practical skills in data analysis, predictive modeling, API development, and frontend integration.

**Technologies:** Python | Machine Learning | FastAPI | Streamlit
