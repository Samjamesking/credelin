# Project Index - Credit Delinquency Prediction System

**Quick Navigation Guide for All Project Files**

---

## 📚 START HERE

Choose your entry point based on what you want to do:

### 🚀 **First Time Setup?**
→ Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)

### 📖 **Need Full Documentation?**
→ Read [README.md](README.md) (comprehensive guide)

### 📋 **Project Overview?**
→ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) (this project summary)

---

## 📁 PROJECT FILES

### Core Application Files

| File | Type | Purpose | When to Use |
|------|------|---------|------------|
| [model_training.py](model_training.py) | Python | Train Random Forest model | Before running app, or to retrain |
| [app.py](app.py) | Python | Streamlit web application | To run the web interface |
| [prediction_api.py](prediction_api.py) | Python | API for programmatic access | Integration with other systems |
| [eda_analysis.py](eda_analysis.py) | Python | Data analysis & quality checks | Understand your dataset |
| [examples.py](examples.py) | Python | Usage examples (8 total) | Learn how to use everything |
| [config.py](config.py) | Python | Centralized configuration | Customize system behavior |

### Data Files

| File | Type | Size | Purpose |
|------|------|------|---------|
| [train_u6lujuX_CVtuZ9i.xlsx](train_u6lujuX_CVtuZ9i.xlsx) | XLSX | Dataset | Training data for model |
| [test_Y3wMUE5_7gLdaTN.xlsx](test_Y3wMUE5_7gLdaTN.xlsx) | XLSX | Dataset | Testing/validation data |

### Configuration & Dependencies

| File | Type | Purpose |
|------|------|---------|
| [requirements.txt](requirements.txt) | Text | Python package dependencies |

### Documentation Files

| File | Pages | Purpose | Read Time |
|------|-------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | 2 | 5-minute setup guide | 5 min |
| [README.md](README.md) | 20+ | Comprehensive documentation | 20 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 5 | Project overview & summary | 10 min |
| [INDEX.md](INDEX.md) | 1 | This file - navigation guide | 5 min |

### Generated Files (After Training)

These are created automatically when you run `python model_training.py`:

| File | Purpose | Type |
|------|---------|------|
| credit_delinquency_model.pkl | Trained Random Forest model | Binary |
| label_encoders.pkl | Feature encoders | Binary |
| model_config.pkl | Model configuration | Binary |

---

## 🎯 COMMON TASKS

### I want to... Get Started Quickly
1. Open [QUICKSTART.md](QUICKSTART.md)
2. Follow the 3-step setup
3. Done! 🎉

### I want to... Understand My Data
1. Run: `python eda_analysis.py`
2. Review the output analysis
3. Check for issues or anomalies

### I want to... Train the Model
1. Run: `python model_training.py`
2. Wait for completion
3. Check performance metrics
4. Model files are saved automatically

### I want to... Run the Web App
1. Run: `streamlit run app.py`
2. Open: http://localhost:8501
3. Make predictions!

### I want to... Use the API
1. See [examples.py](examples.py) for code samples
2. Check [prediction_api.py](prediction_api.py) for all methods
3. Integrate with your system

### I want to... See Usage Examples
1. Run: `python examples.py`
2. Choose from 8 different examples
3. See real code in action

### I want to... Customize Settings
1. Edit [config.py](config.py)
2. Adjust parameters as needed
3. Re-run with new settings

---

## 📊 WORKFLOW DIAGRAM

```
Installation
    ↓
pip install -r requirements.txt
    ↓
Analyze Data (Optional)
    ↓
python eda_analysis.py
    ↓
Train Model
    ↓
python model_training.py
    ↓
Choose Usage Method
    ├─→ Web App: streamlit run app.py
    ├─→ API: python prediction_api.py
    ├─→ Examples: python examples.py
    └─→ Custom: Import modules in your script
    ↓
Make Predictions
    ↓
Done! 🎉
```

---

## 🔑 KEY FILES BY PURPOSE

### **For Data Scientists**
- [model_training.py](model_training.py) - Model training
- [eda_analysis.py](eda_analysis.py) - Data analysis
- [config.py](config.py) - Model parameters

### **For Developers**
- [app.py](app.py) - Web application
- [prediction_api.py](prediction_api.py) - API interface
- [examples.py](examples.py) - Usage examples

### **For Administrators**
- [requirements.txt](requirements.txt) - Dependencies
- [config.py](config.py) - System configuration
- [README.md](README.md) - Full documentation

### **For End Users**
- [QUICKSTART.md](QUICKSTART.md) - Quick start
- [app.py](app.py) - Web interface
- [examples.py](examples.py) - How-to guide

---

## 📋 FILE DESCRIPTIONS

### model_training.py
**Train the Random Forest model**
- Load and preprocess data
- Handle missing values and encoding
- Train Random Forest classifier
- Evaluate model performance
- Save trained model

Key Class: `CreditDelinquencyModel`

### app.py
**Interactive web application**
- Dashboard with model info
- Single prediction interface
- Batch prediction upload
- Results visualization
- Download functionality

Framework: Streamlit

### prediction_api.py
**Programmatic API for predictions**
- Single customer prediction
- Batch processing
- DataFrame support
- Feature importance
- Model information

Key Class: `PredictionAPI`

### eda_analysis.py
**Exploratory Data Analysis**
- Data quality assessment
- Statistical analysis
- Missing value detection
- Outlier identification
- Correlation analysis

Key Class: `DataAnalyzer`

### examples.py
**8 complete usage examples**
1. Train model from scratch
2. Single prediction
3. Batch predictions
4. Feature importance
5. Model information
6. Custom batch processing
7. Comparison analysis
8. Export to Excel

Interactive menu for selection

### config.py
**Centralized configuration**
- Model parameters
- Data paths
- Risk thresholds
- Performance settings
- Deployment options
- Helper functions

Edit this to customize behavior

### requirements.txt
**Python dependencies**
```
pandas>=1.3.0
openpyxl>=3.6.0
numpy>=1.21.0
scikit-learn>=1.0.0
streamlit>=1.10.0
plotly>=5.0.0
joblib>=1.1.0
```

---

## 🔍 FINDING WHAT YOU NEED

### I'm looking for...

**How to install?**
→ [QUICKSTART.md](QUICKSTART.md) Step 1

**How to train the model?**
→ [QUICKSTART.md](QUICKSTART.md) Step 2 or [model_training.py](model_training.py)

**How to use the web app?**
→ [QUICKSTART.md](QUICKSTART.md) Step 3 or [app.py](app.py)

**API documentation?**
→ [prediction_api.py](prediction_api.py) or [examples.py](examples.py)

**Data analysis?**
→ [eda_analysis.py](eda_analysis.py)

**Configuration options?**
→ [config.py](config.py)

**Complete guide?**
→ [README.md](README.md)

**Troubleshooting?**
→ [README.md](README.md) Troubleshooting section

**Deployment?**
→ [README.md](README.md) Deployment section

---

## ⚡ QUICK COMMANDS

```bash
# Install dependencies
pip install -r requirements.txt

# Analyze data
python eda_analysis.py

# Train model
python model_training.py

# Run web app
streamlit run app.py

# See examples
python examples.py

# Test API
python prediction_api.py
```

---

## 📱 ACCESSING DIFFERENT INTERFACES

### **Web Interface**
- Command: `streamlit run app.py`
- URL: http://localhost:8501
- Best for: End users, quick predictions

### **Command Line**
- Command: `python model_training.py`
- Best for: Data scientists, model training

### **Python API**
- Module: `prediction_api.py`
- Best for: Developers, system integration

### **Examples**
- Command: `python examples.py`
- Best for: Learning, testing features

---

## 🎓 LEARNING PATH

**Beginner**: 
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `python model_training.py`
3. Run `streamlit run app.py`
4. Make a prediction!

**Intermediate**:
1. Read [README.md](README.md)
2. Run `python eda_analysis.py`
3. Edit [config.py](config.py)
4. Run `python examples.py`

**Advanced**:
1. Study [model_training.py](model_training.py)
2. Study [prediction_api.py](prediction_api.py)
3. Integrate API into your system
4. Deploy to production

---

## ✅ CHECKLIST FOR FIRST-TIME USE

- [ ] Read [QUICKSTART.md](QUICKSTART.md)
- [ ] Run: `pip install -r requirements.txt`
- [ ] Run: `python model_training.py`
- [ ] Run: `streamlit run app.py`
- [ ] Make a test prediction
- [ ] Download results
- [ ] Read [README.md](README.md) for advanced features
- [ ] Explore [examples.py](examples.py)
- [ ] Customize [config.py](config.py)

---

## 🚀 YOU'RE READY!

All files are in place and ready to use. Choose your starting point:

1. **Fast Start** → [QUICKSTART.md](QUICKSTART.md)
2. **Full Guide** → [README.md](README.md)
3. **Project Info** → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
4. **See Examples** → Run `python examples.py`

---

**Getting started is just 3 steps away!** 🎉

```bash
pip install -r requirements.txt
python model_training.py
streamlit run app.py
```

---

*Last Updated: March 2026*  
*Version: 1.0*  
*Status: ✅ Production Ready*
