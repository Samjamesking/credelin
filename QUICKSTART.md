# Quick Start Guide - Credit Delinquency Prediction App

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

Open PowerShell in the project directory and run:

```powershell
cd "e:\New Model"
pip install -r requirements.txt
```

**Status**: Wait for all packages to install ✓

### Step 2: Train the Model (3 minutes)

```powershell
python model_training.py
```

**What happens:**
- Loads your training and test datasets
- Trains a Random Forest model
- Shows performance metrics
- Saves model files

**Expected output:**
```
Loading training data from e:\New Model\train_u6lujuX_CVtuZ9i.xlsx
Training data shape: (X, Y)
...
TRAINING COMPLETE
```

### Step 3: Run the Web App

```powershell
streamlit run app.py
```

**What happens:**
- Opens http://localhost:8501 in browser
- You can now make predictions!

---

## What You Can Do Now

### 📊 Make Single Predictions
1. Go to **Single Prediction** tab
2. Enter customer information
3. Click **Make Prediction**
4. See delinquency risk score

### 📦 Process Batch Files
1. Go to **Batch Prediction** tab
2. Upload Excel/CSV file with customer data
3. Click **Run Batch Prediction**
4. Download results as CSV

### 📈 View Dashboard
1. Go to **Dashboard** tab
2. See model information
3. View feature list

---

## Folder Structure After Setup

```
e:\New Model\
├── train_u6lujuX_CVtuZ9i.xlsx          (Your training data)
├── test_Y3wMUE5_7gLdaTN.xlsx           (Your test data)
├── model_training.py                   (Training script)
├── app.py                              (Web app)
├── eda_analysis.py                     (Data analysis)
├── prediction_api.py                   (API interface)
├── requirements.txt                    (Dependencies list)
├── README.md                           (Full documentation)
├── QUICKSTART.md                       (This file)
│
├── credit_delinquency_model.pkl        (Generated: trained model)
├── label_encoders.pkl                  (Generated: feature encoders)
└── model_config.pkl                    (Generated: model config)
```

---

## Common Tasks

### Task 1: Check Data Quality

```powershell
python eda_analysis.py
```

This analyzes your datasets and reports:
- Missing values
- Data types
- Class distribution
- Outliers
- Correlations

### Task 2: Make Predictions Programmatically

```python
from prediction_api import PredictionAPI

api = PredictionAPI()
result = api.predict_single({'age': 35, 'income': 50000, ...})
print(result)
```

### Task 3: Retrain on New Data

```python
from model_training import CreditDelinquencyModel
import pandas as pd

model = CreditDelinquencyModel()
new_data = pd.read_excel('new_training_data.xlsx')
model.train(new_data)
model.save_model()
```

---

## Understanding Results

### Prediction Output Format

```json
{
  "success": true,
  "prediction": 0,                                    // 0 = Low Risk, 1 = High Risk
  "probability_non_delinquent": 0.85,               // 85% chance of paying
  "probability_delinquent": 0.15,                   // 15% chance of default
  "risk_level": "Low"                               // Risk category
}
```

### Risk Levels

| Risk Level | Probability | Color  | Action |
|-----------|------------|--------|--------|
| 🟢 Low    | < 30%      | Green  | Approve loan |
| 🟡 Medium | 30-60%     | Yellow | Monitor closely |
| 🔴 High   | > 60%      | Red    | Require additional verification |

---

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Module not found" | Run: `pip install -r requirements.txt` |
| "Model files not found" | Run: `python model_training.py` |
| "Port 8501 already in use" | Run: `streamlit run app.py --server.port 8502` |
| "Excel file not loading" | Check file format is .xlsx or .xls |
| "Predictions seem wrong" | Check input data matches training format |

---

## Next Steps

1. ✅ **Install dependencies** - `pip install -r requirements.txt`
2. ✅ **Analyze data** - `python eda_analysis.py`
3. ✅ **Train model** - `python model_training.py`
4. ✅ **Run app** - `streamlit run app.py`
5. 📈 **Make predictions** - Use web interface or API
6. 📊 **Monitor results** - Track prediction accuracy

---

## Tips for Best Results

### Data Preparation
- Ensure all required features are present
- Handle missing values before uploading
- Use consistent data types (numbers vs text)
- Remove duplicate records

### Model Training
- Train with balanced dataset (equal classes)
- Use historical data for better predictions
- Retrain quarterly with new data
- Monitor performance metrics

### Making Predictions
- Use data in same format as training
- Provide all required features
- Check input ranges are reasonable
- Review high-risk predictions manually

---

## Support Resources

- **Full Documentation**: See [README.md](README.md)
- **Model Details**: See [model_training.py](model_training.py)
- **Web App Code**: See [app.py](app.py)
- **API Usage**: See [prediction_api.py](prediction_api.py)
- **Data Analysis**: See [eda_analysis.py](eda_analysis.py)

---

**Ready to go!** 🚀

Start with Step 1 above and you'll have predictions in minutes.

---

Last Updated: March 2026
