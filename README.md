------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------
☀️ Solar Power Forecast Agent
------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Project Overview***

The Solar Power Forecast Agent is a Machine Learning-based web application that predicts solar power generation using weather and environmental parameters. The system uses an XGBoost Regression model to estimate future solar power output and provides AI-based recommendations for efficient energy utilization.

The application follows a two-tier architecture consisting of a Streamlit frontend and a FastAPI backend. The frontend collects user inputs and displays prediction results, while the backend performs machine learning inference, stores prediction records, and exposes REST APIs.

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Objectives***

***Phase 1*** – Machine Learning Model

- Collect and preprocess solar power generation data.

- Train regression models for solar power prediction.

- Evaluate model performance using:

- Mean Absolute Error (MAE)

- Mean Squared Error (MSE)

- Root Mean Squared Error (RMSE)

- R² Score

- Select the best-performing model.

- Save the trained model using Joblib.

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Phase 2*** – Solar Power Forecast Agent

Develop a complete forecasting system capable of:

- Accepting weather parameters.
 
- Predicting solar power generation.

- Providing AI-based recommendations.

- Displaying forecasting reports.

- Saving prediction history.

- Providing REST APIs through FastAPI.

- Displaying results using Streamlit.

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***System Architecture:***

```
                Streamlit Frontend
                       │
                HTTP Requests
                       │
                       ▼
                 FastAPI Backend
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   XGBoost Model   StandardScaler   SQLite Database
```

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Dataset:***

The project uses a Solar Power Generation Dataset containing weather and environmental measurements.

***Input Features:***

- Wind Speed

- Sunshine Duration

- Air Pressure

- Solar Radiation

- Air Temperature

- Relative Humidity

- Hour

- Day

- Month

------------------------------------------------------------------------------------------------------------------------------------

***Target Variable:***

- Solar Power Generation (Watts)

------------------------------------------------------------------------------------------------------------------------------------

***Technologies Used:***

- Python

- Streamlit

- FastAPI

- Uvicorn

- Requests

- Pandas

- NumPy

- Scikit-learn

- XGBoost

- Joblib

- SQLite

- Matplotlib

- Seaborn

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Machine Learning Model:***

Model Used:

- XGBoost Regressor

------------------------------------------------------------------------------------------------------------------------------------

Model Evaluation:

The model is evaluated using:

- Mean Absolute Error (MAE)

- Mean Squared Error (MSE)

- Root Mean Squared Error (RMSE)

- R² Score

------------------------------------------------------------------------------------------------------------------------------------

The trained model is saved as:

- model.pkl

------------------------------------------------------------------------------------------------------------------------------------

The trained scaler is saved as:

- scaler.pkl

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***FastAPI Backend***

The backend is developed using FastAPI and exposes REST APIs for prediction and history management.

***API Endpoints:***

Home

GET /

Returns API information.

***Health Check:***

```GET /health```

Returns backend health status.

***Forecast Solar Power:***

```POST /forecast```

Predicts solar power generation based on weather parameters.

***Returns:***

- Predicted Power

- Generation Level

- Estimated Efficiency

- AI Recommendation

- AI Insight

***Prediction History:***

```GET /history```

Returns all stored prediction records from the SQLite database.

***Streamlit Frontend:***

The Streamlit application provides an interactive interface for users.

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Features:***

- Enter weather parameters

- Predict solar power generation

- Display prediction report

- Show AI recommendation

- Show AI insight

- View prediction history

- Dashboard statistics

- Prediction trend chart

- Generation level distribution

- Download prediction history as CSV

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Database***

Prediction records are stored in an SQLite database.

***Database File:***

prediction_records.db

***Stored Information:***

- Prediction Date
- Prediction Time
- Predicted Power
- Generation Level
- Estimated Efficiency

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Project Structure:***

```
Solar-Power-Forecast-Agent/
│
├── frontend.py
├── backend.py
├── model.pkl
├── scaler.pkl
├── prediction_records.db
├── solar_dataset.csv
├── requirements.txt
├── README.md
└── .gitignore
```

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Installation:***

Clone the repository:

bash git clone https://github.com/9154327992/solar-power-forecast-agent.git [URL 🔗](https://github.com/9154327992/solar-power-forecast-agent.git)

Move into the project directory:

```bash cd solar-power-forecast-agent```

Install dependencies:

```bash pip install -r requirements.txt```

Running the Project

Start FastAPI Backend

```bash python -m uvicorn backend:app --reload```

Backend URL:

http://127.0.0.1:8000 [URL 🔗](http://127.0.0.1:8000/)

API Documentation:

http://127.0.0.1:8000/docs [URL 🔗](http://127.0.0.1:8000/docs)

Start Streamlit Frontend

```bash python -m streamlit run frontend.py```

Streamlit URL:

https://solar-power-forecast-agent-gk8zjahuz3hgjypbw4zk2p.streamlit.app/ [URL 🔗](https://solar-power-forecast-agent-gk8zjahuz3hgjypbw4zk2p.streamlit.app/)

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Results:***

The application successfully:

- Predicts solar power generation.
- Displays generation level.
- Calculates estimated efficiency.
- Generates AI recommendations.
- Provides AI insights.
- Stores prediction history.
- Displays dashboard analytics.
- Downloads prediction history as CSV.

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Conclusion:***

The Solar Power Forecast Agent combines Machine Learning, FastAPI, Streamlit, and SQLite to create a complete solar power forecasting system. The project demonstrates an end-to-end workflow, including model training, backend API development, frontend integration, and persistent storage, providing a practical solution for renewable energy forecasting.

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***Future Scope:***

- Real-time weather API integration
- Deep Learning-based forecasting models
- Interactive analytics dashboard
- Solar plant monitoring system
- Mobile application integration
- Cloud deployment
- User authentication
- Automated email notifications

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

***👨‍💻 Author:***

Matta Venkata Karthik

🎓 B.Tech – Computer Science and Design (Data Science)

🏫 College: NRI Institute Of Technology

🔗 LinkedIn: https://www.linkedin.com/in/venkata-karthik-matta-b0536b321

🏫 College LinkedIn: https://www.linkedin.com/company/datascience-nriit

💻 GitHub: https://github.com/9154327992
