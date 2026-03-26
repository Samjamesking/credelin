# Credit Delinquency Prediction System

A machine learning application for predicting credit delinquency using Random Forest classification. Built with Python, Scikit-learn, and Streamlit for deployment.

## Overview

This system predicts the likelihood of credit delinquency (failure to make loan payments) based on borrower characteristics and loan features. It provides:

- **Single Predictions**: Predict delinquency for individual customers
- **Batch Predictions**: Process multiple customers from Excel/CSV files  
- **Risk Scoring**: Categorize customers into risk levels
- **Probability Estimates**: Get confidence scores for predictions
- **Interactive Dashboard**: Real-time metrics and insights

## Project Structure

```
e:\New Model\
├── train_u6lujuX_CVtuZ9i.xlsx      # Training dataset
├── test_Y3wMUE5_7gLdaTN.xlsx       # Test dataset
├── model_training.py               # Model training script
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── credit_delinquency_model.pkl    # Trained model (after training)
├── label_encoders.pkl              # Feature encoders (after training)
└── model_config.pkl                # Model configuration (after training)
```

## Installation

### Step 1: Install Python Dependencies

```bash
cd e:\New Model
pip install -r requirements.txt
```

Or install individually:

```bash
pip install pandas openpyxl numpy scikit-learn streamlit plotly joblib
```

### Step 2: Verify Installation

```bash
python -c "import pandas, sklearn, streamlit; print('All packages installed successfully!')"
```

## Usage

### Step 1: Train the Model

Before running the app, train the Random Forest model on your training dataset:

```bash
python model_training.py
```

This will:
- Load training and test datasets
- Preprocess features and handle missing values
- Train a Random Forest classifier
- Evaluate performance on test data
- Save the trained model and encoders

**Output files created:**
- `credit_delinquency_model.pkl` - Trained model
- `label_encoders.pkl` - Feature encoders
- `model_config.pkl` - Model configuration

### Step 2: Run the Streamlit App

```bash
streamlit run app.py
```

This will:
- Start a local web server (default: http://localhost:8501)
- Open the app in your default browser
- Load the trained model and encoders

### Step 3: Using the App

#### Dashboard Page
- View model information
- Check model status
- See feature list

#### Single Prediction Page
- Enter customer information
- Get immediate delinquency prediction
- View probability distribution
- See risk category

#### Batch Prediction Page
- Upload Excel/CSV file with customer data
- Process multiple predictions at once
- Download results with predictions
- View risk distribution

#### About Page
- Application documentation
- Model details
- Risk categories explanation
- Business use cases

## Model Details

### Algorithm: Random Forest Classifier

**Configuration:**
- Number of Trees: 100
- Max Depth: 15
- Min Samples Split: 10
- Min Samples Leaf: 4
- Class Weight: Balanced (handles imbalanced data)

### Data Processing

**Features:**
- Numeric features: Filled with median for missing values
- Categorical features: Label encoded, filled with mode for missing values
- All features included in final model

**Target Variable:**
- Binary classification (Delinquent / Non-Delinquent)
- Last column in datasets assumed to be target

### Performance Metrics

The model evaluates performance using:
- Accuracy: Overall correctness of predictions
- Precision: Positive prediction correctness
- Recall: Ability to find delinquent customers
- F1-Score: Balance between precision and recall
- ROC-AUC: Performance across all classification thresholds

## Risk Categories

- 🟢 **Low Risk**: Delinquency probability < 30%
  - Customers with strong payment history and favorable characteristics

- 🟡 **Medium Risk**: Delinquency probability 30-60%
  - Customers requiring monitoring and potential intervention

- 🔴 **High Risk**: Delinquency probability > 60%
  - Customers with high likelihood of payment default

## Business Applications

1. **Credit Risk Assessment**
   - Evaluate loan applicant profiles
   - Adjust pricing based on risk

2. **Portfolio Management**
   - Identify risky loans in existing portfolio
   - Plan collection strategies

3. **Customer Segmentation**
   - Segment customers by risk profile
   - Tailor retention strategies

4. **Preventive Intervention**
   - Target high-risk customers for support
   - Reduce default rates

5. **Loan Decision Making**
   - Approve/deny loan applications
   - Set loan terms based on risk

## Configuration

### Modifying Model Parameters

Edit `model_training.py` to adjust Random Forest parameters:

```python
self.model = RandomForestClassifier(
    n_estimators=100,        # Number of trees
    max_depth=15,            # Maximum tree depth
    min_samples_split=10,    # Minimum samples to split
    min_samples_leaf=4,      # Minimum samples in leaf
    random_state=42,         # Reproducibility
    n_jobs=-1,              # Use all CPU cores
    class_weight='balanced' # Handle class imbalance
)
```

### Expected Dataset Format

**Requirements:**
- Excel format (.xlsx or .xls) or CSV
- First row: Column headers
- Last column: Target variable (0=Non-Delinquent, 1=Delinquent)
- Numeric and categorical features supported
- Missing values handled automatically

**Example:**

| Age | Income | LoanAmount | CreditScore | Employment | ... | Target |
|-----|--------|------------|-------------|------------|-----|--------|
| 35  | 50000  | 25000      | 720        | Employed   | ... | 0      |
| 42  | 75000  | 50000      | 680        | Employed   | ... | 1      |

## Troubleshooting

### Error: "Module not found"
- Ensure all packages from `requirements.txt` are installed
- Try: `pip install --upgrade pandas scikit-learn streamlit`

### Error: "Model files not found"
- Run `model_training.py` first to train and save the model
- Verify model files exist in the project directory

### Prediction seems incorrect
- Check input data format matches training data
- Verify numeric features are in valid ranges
- Ensure categorical features use expected values

### App runs slowly
- Reduce dataset size for batch predictions
- Close other applications to free system memory
- Consider using a machine with more RAM

## Advanced Usage

### Making Programmatic Predictions

```python
from model_training import CreditDelinquencyModel
import pandas as pd

# Load model
model = CreditDelinquencyModel()
model.load_model(
    model_path='credit_delinquency_model.pkl',
    encoder_path='label_encoders.pkl'
)

# Prepare data
data = pd.read_excel('new_customers.xlsx')

# Make predictions
predictions, probabilities = model.predict(data)

print(f"Delinquency Predictions: {predictions}")
print(f"Probabilities: {probabilities}")
```

### Retraining on New Data

```python
# Load new training data
train_df = pd.read_excel('new_training_data.xlsx')

# Retrain model
model = CreditDelinquencyModel()
model.train(train_df, target_column='delinquency_status')
model.save_model()
```

## Deployment

### Streamlit Cloud

1. Push project to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with one click
4. Share public URL

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t credit-delinquency-app .
docker run -p 8501:8501 credit-delinquency-app
```

### Local Production Server

```bash
streamlit run app.py --server.port=80 --server.address=0.0.0.0
```

## Performance Optimization

### For Large Datasets

1. **Batch Processing**: Split large files into smaller chunks
2. **Parallel Processing**: Random Forest uses `n_jobs=-1` for all cores
3. **Feature Selection**: Consider removing less important features
4. **Model Simplification**: Reduce number of trees or max depth

### For Production

1. Use model serialization (joblib) for fast loading
2. Implement caching for repeated predictions
3. Monitor prediction latency
4. Log all predictions for audit trail

## Security Considerations

1. **Data Privacy**: Never log sensitive customer information
2. **Model Access**: Restrict access to prediction endpoints
3. **Input Validation**: Validate user inputs before prediction
4. **HTTPS**: Use SSL/TLS in production
5. **Authentication**: Implement user authentication

## Maintenance

### Regular Tasks

1. **Monthly**: Review model performance metrics
2. **Monthly**: Check for data drift in predictions
3. **Quarterly**: Retrain on new data if available
4. **Yearly**: Benchmark against updated benchmarks

### Model Monitoring

Monitor:
- Prediction accuracy over time
- Feature distribution changes
- Class imbalance trends
- Concept drift in predictions

## Support & Contribution

For issues or suggestions:
1. Check the troubleshooting section
2. Review dataset format requirements
3. Verify all dependencies installed
4. Contact data science team for advanced issues

## License

This project is for internal use. All rights reserved.

## Version History

- **v1.0** (2026): Initial release
  - Random Forest model with 100 trees
  - Streamlit web interface
  - Single and batch prediction modes
  - Dashboard with metrics

---

**Last Updated**: March 2026  
**Python Version**: 3.8+  
**Framework**: Scikit-learn 1.0+, Streamlit 1.10+
