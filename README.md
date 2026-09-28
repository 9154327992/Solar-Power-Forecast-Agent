# Solar Power Forecast Agent

An AI-powered solar energy forecasting and recommendation system built with **Python, Streamlit, FastAPI, and XGBoost**.

The application predicts solar power generation using weather and time-based features and provides forecasting, live weather, analytics, prediction history, reporting, and an AI energy assistant through an interactive web dashboard.

## 🌞 Live Application

**Backend API:**
[Solar Power Forecast Agent — Render]: [https://github.com/9154327992/Solar-Power-Forecast-Agent?utm_source=chatgpt.com](https://solar-power-forecast-agent.onrender.com)

**Frontend:**
[Solar Power Forecast Agent — Streamlit]: [https://solar-power-forecast-agent-sombc9mcuyfkyexhlmeqgz.streamlit.app/?utm_source=chatgpt.com](https://solar-power-forecast-agent-sombc9mcuyfkyexhlmeqgz.streamlit.app/)

---

## ✨ Features

* ☀️ **Solar Power Forecasting**

  * Predicts solar power generation using an XGBoost regression model.
  * Uses weather and time-based input features.

* 🌤️ **Live Weather Integration**

  * Temperature
  * Humidity
  * Atmospheric pressure
  * Wind speed
  * Cloud cover
  * Sunrise and sunset

* 🤖 **AI Energy Assistant**

  * Answers questions about solar generation.
  * Provides energy-saving recommendations.
  * Supports battery and appliance-related queries.
  * Provides information about forecasts and reports.

* 📊 **Analytics Dashboard**

  * Prediction statistics
  * Historical prediction charts
  * Distribution analysis
  * Prediction tables
  * CSV export

* 🕒 **Prediction History**

  * Stores previous forecasts.
  * Displays historical prediction data.

* 📄 **Report Generation**

  * Provides forecast and system information in report form.

* ⚙️ **Admin Dashboard**

  * System health
  * Model information
  * Dataset upload
  * Model retraining
  * Backup
  * Logs
  * API endpoint information

* 🎨 **Responsive Streamlit Interface**

  * Light and dark appearance support through Streamlit.
  * Custom solar-themed interface.
  * Responsive dashboard layout.

---

## 🧠 Machine Learning

The project uses an **XGBoost Regressor** for solar power prediction.

### Input Features

The forecasting system uses weather and temporal parameters including:

```text
Wind Speed
Sunshine Duration
Air Pressure
Solar Radiation
Air Temperature
Relative Humidity
Hour
Day
Month
```

### Prediction Output

The API returns information such as:

```json
{
  "prediction": 6.87,
  "level": "High",
  "efficiency": 100,
  "recommendation": "Good conditions for solar generation."
}
```

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │   Weather Data       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Preprocessing    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Feature Engineering   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ XGBoost ML Model     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Solar Prediction     │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │ Streamlit   │ │ FastAPI     │ │ AI Assistant│
        │ Dashboard   │ │ Backend API │ │             │
        └─────────────┘ └─────────────┘ └─────────────┘
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Analytics & Reports  │
                    └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology        | Purpose                            |
| ----------------- | ---------------------------------- |
| **Python**        | Core programming language          |
| **Streamlit**     | Interactive frontend and dashboard |
| **FastAPI**       | Backend REST API                   |
| **XGBoost**       | Machine learning regression model  |
| **Scikit-learn**  | Machine learning utilities         |
| **Pandas**        | Data processing                    |
| **NumPy**         | Numerical computation              |
| **Plotly**        | Interactive visualizations         |
| **Matplotlib**    | Data visualization                 |
| **Joblib**        | Model serialization                |
| **Requests**      | API communication                  |
| **python-dotenv** | Environment configuration          |
| **SQLite**        | Data storage                       |
| **Git/GitHub**    | Version control                    |

---

## 📁 Project Structure

```text
Solar-Power-Forecast-Agent/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   ├── banner.jpg
│   ├── logo.png
│   └── style.css
│
├── backend/
│   └── ...
│
├── datasets/
│   └── ...
│
├── models/
│   └── ...
│
├── notebooks/
│   └── ...
│
├── pages/
│   ├── ...
│   └── 8_Settings.py
│
├── tests/
│   └── ...
│
├── frontend.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/9154327992/Solar-Power-Forecast-Agent.git
```

### 2. Enter the project directory

```bash
cd Solar-Power-Forecast-Agent
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file for local development.

Example:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
```

For Streamlit Community Cloud, configure sensitive API keys through **Streamlit Secrets** rather than committing them to GitHub.

---

## ▶️ Running the Application

### Start the Streamlit frontend

```bash
streamlit run frontend.py
```

The application will open in your browser.

### Start the FastAPI backend

Run the backend according to the backend application's entry point.

Example:

```bash
uvicorn backend.main:app --reload
```

The exact backend module should match the entry point in your project.

---

## 🔌 API Endpoints

The application provides endpoints including:

```text
POST /api/predict/forecast
GET  /api/history
POST /assistant
```

### Forecast

```text
POST /api/predict/forecast
```

Accepts weather and temporal features and returns a solar generation prediction.

### History

```text
GET /api/history
```

Returns previous prediction records.

### AI Assistant

```text
POST /assistant
```

Provides responses and recommendations related to solar energy and the application.

---

## 📊 Dashboard

The Streamlit application contains multiple sections:

```text
Home
│
├── Solar Forecast
├── Live Weather
├── AI Energy Assistant
├── Prediction History
├── Analytics
├── Reports
├── Admin Dashboard
└── Settings
```

---

## 🎨 Theme

The application uses Streamlit's built-in appearance system.

Users can change the application appearance through:

```text
⋮ → Settings → Appearance
```

Available modes depend on the Streamlit interface and include Light, Dark, and System.

---

## 📈 Analytics

The analytics dashboard provides visual analysis of historical predictions, including:

* KPI summaries
* Prediction trends
* Distribution charts
* Histograms
* Box plots
* Historical prediction tables
* CSV export

---

## ⚙️ Admin Features

The Admin Dashboard provides tools for:

* Checking system health
* Viewing model information
* Uploading datasets
* Retraining the model
* Creating backups
* Viewing logs
* Checking API endpoints

---

## ☁️ Deployment

### Frontend

The Streamlit frontend is deployed using **Streamlit Community Cloud**.

### Backend

The FastAPI backend is deployed separately and accessed by the Streamlit frontend through the configured API URL.

---

## 🔄 Development Workflow

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push
```

The deployment can then be updated from the connected hosting service.

---

## 🔒 Security

Do not commit secrets or API keys to GitHub.

The following should remain private:

```text
.env
API keys
Access tokens
Passwords
Private credentials
```

Use environment variables locally and Streamlit Secrets for deployed applications.

---

## 🔮 Future Enhancements

Possible future improvements include:

* Real-time solar generation monitoring
* More advanced forecasting models
* Automated model retraining
* Battery charge/discharge optimization
* Solar panel performance monitoring
* More detailed weather forecasting
* Cloud-based database storage
* User authentication
* Automated scheduled reports
* Additional energy-consumption analytics

---

## 👨‍💻 Project

**Solar Power Forecast Agent**

Built using:

**Python • Streamlit • FastAPI • XGBoost • Plotly**

---

## 📄 License

Add your preferred open-source license here, such as **MIT License**, if you intend to distribute the project under that license.

---

## 👨‍💻 Author

Matta Venkata Karthik

🎓 B.Tech – Computer Science and Design (Data Science)

🏫 College: NRI Institute Of Technology

🔗 LinkedIn: https://www.linkedin.com/in/venkata-karthik-matta-b0536b321

🏫 College LinkedIn: https://www.linkedin.com/company/datascience-nriit

💻 GitHub: https://github.com/9154327992
