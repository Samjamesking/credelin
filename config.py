"""
Configuration file for Credit Delinquency Prediction System
Customize model parameters and application settings here
"""

# ============================================================================
# MODEL PARAMETERS
# ============================================================================

MODEL_CONFIG = {
    # Random Forest Parameters
    'n_estimators': 100,              # Number of trees in the forest
    'max_depth': 15,                  # Maximum depth of trees
    'min_samples_split': 10,          # Minimum samples required to split
    'min_samples_leaf': 4,            # Minimum samples required at leaf
    'random_state': 42,               # Reproducibility seed
    'n_jobs': -1,                     # Use all CPU cores (-1 = all)
    'class_weight': 'balanced',       # Handle imbalanced classes
    
    # Training Configuration
    'target_column': 'target',        # Name of target variable
    'random_seed': 42,
}

# ============================================================================
# DATA PATHS
# ============================================================================

DATA_PATHS = {
    'training_data': r'E:\New Model\train_u6lujuX_CVtuZ9i.xlsx',
    'test_data': r'E:\New Model\test_Y3wMUE5_7gLdaTN.xlsx',
    'model_path': r'E:\New Model\credit_delinquency_model.pkl',
    'encoder_path': r'E:\New Model\label_encoders.pkl',
    'config_path': r'E:\New Model\model_config.pkl',
}

# ============================================================================
# RISK THRESHOLDS
# ============================================================================

RISK_THRESHOLDS = {
    'low_risk': 0.30,      # Probability < 30% = Low Risk
    'medium_risk': 0.60,   # Probability 30-60% = Medium Risk
    'high_risk': 1.0,      # Probability > 60% = High Risk
}

# Risk categories
RISK_CATEGORIES = {
    'Low': {
        'min': 0.0,
        'max': 0.30,
        'color': '#00FF00',
        'emoji': '🟢',
        'action': 'Approve loan'
    },
    'Medium': {
        'min': 0.30,
        'max': 0.60,
        'color': '#FFD700',
        'emoji': '🟡',
        'action': 'Monitor closely'
    },
    'High': {
        'min': 0.60,
        'max': 1.0,
        'color': '#FF0000',
        'emoji': '🔴',
        'action': 'Require additional verification'
    }
}

# ============================================================================
# STREAMLIT APP SETTINGS
# ============================================================================

STREAMLIT_CONFIG = {
    'page_title': 'Credit Delinquency Predictor',
    'page_icon': '💳',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'max_upload_size': 200,  # MB
}

# ============================================================================
# PERFORMANCE THRESHOLDS
# ============================================================================

PERFORMANCE_THRESHOLDS = {
    'min_accuracy': 0.70,        # Minimum acceptable accuracy
    'min_precision': 0.65,       # Minimum acceptable precision
    'min_recall': 0.60,          # Minimum acceptable recall
    'min_f1_score': 0.62,        # Minimum acceptable F1 score
}

# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

FEATURE_ENGINEERING = {
    'handle_missing_numeric': 'median',    # 'mean', 'median', or 'drop'
    'handle_missing_categorical': 'mode',   # 'mode' or 'drop'
    'encode_categorical': 'label',         # 'label' or 'onehot'
    'scale_features': False,               # Normalize/standardize features
}

# ============================================================================
# LOGGING & MONITORING
# ============================================================================

LOGGING_CONFIG = {
    'log_level': 'INFO',           # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'log_predictions': True,       # Log all predictions
    'log_file': 'predictions.log',
    'enable_monitoring': True,     # Track model performance
}

# ============================================================================
# BATCH PROCESSING
# ============================================================================

BATCH_CONFIG = {
    'batch_size': 100,             # Size of batches for processing
    'max_file_size_mb': 500,       # Maximum upload file size
    'timeout_seconds': 300,        # Timeout for batch processing
    'enable_parallel': True,       # Use parallel processing
    'n_workers': 4,                # Number of workers for parallel processing
}

# ============================================================================
# API SETTINGS
# ============================================================================

API_CONFIG = {
    'enable_api': True,
    'api_host': '0.0.0.0',
    'api_port': 5000,
    'debug_mode': False,
    'max_requests_per_minute': 60,
    'require_authentication': False,
}

# ============================================================================
# MODEL DEPLOYMENT
# ============================================================================

DEPLOYMENT_CONFIG = {
    'model_version': '1.0',
    'deployment_platform': 'streamlit',  # 'streamlit', 'docker', 'fastapi'
    'auto_retrain': False,
    'retrain_frequency': 'monthly',      # 'daily', 'weekly', 'monthly', 'quarterly'
    'model_versioning': True,
    'backup_models': True,
    'max_model_versions': 5,
}

# ============================================================================
# DATA QUALITY CHECKS
# ============================================================================

DATA_QUALITY_CONFIG = {
    'max_missing_percentage': 50,  # Maximum % of missing values allowed
    'check_duplicates': True,
    'check_outliers': True,
    'outlier_method': 'iqr',       # 'iqr' or 'zscore'
    'outlier_threshold': 3.0,      # Z-score threshold for outliers
    'check_data_types': True,
}

# ============================================================================
# FEATURE SELECTION
# ============================================================================

FEATURE_SELECTION = {
    'enable_feature_selection': False,
    'method': 'importance',        # 'importance', 'correlation', 'rfe'
    'n_features_to_select': None,  # None = keep all
    'importance_threshold': 0.001,
}

# ============================================================================
# ALERTS & NOTIFICATIONS
# ============================================================================

ALERTS_CONFIG = {
    'enable_alerts': False,
    'alert_on_low_performance': True,
    'alert_threshold_accuracy': 0.65,
    'alert_method': 'email',       # 'email', 'slack', 'sms'
    'alert_email': 'admin@example.com',
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_risk_level(probability):
    """Get risk level category based on probability"""
    if probability < RISK_THRESHOLDS['low_risk']:
        return 'Low'
    elif probability < RISK_THRESHOLDS['medium_risk']:
        return 'Medium'
    else:
        return 'High'

def get_risk_config(risk_level):
    """Get configuration for a specific risk level"""
    return RISK_CATEGORIES.get(risk_level, RISK_CATEGORIES['Medium'])

def validate_model_performance(metrics):
    """Check if model meets performance thresholds"""
    checks = {
        'accuracy': metrics.get('accuracy', 0) >= PERFORMANCE_THRESHOLDS['min_accuracy'],
        'precision': metrics.get('precision', 0) >= PERFORMANCE_THRESHOLDS['min_precision'],
        'recall': metrics.get('recall', 0) >= PERFORMANCE_THRESHOLDS['min_recall'],
        'f1_score': metrics.get('f1', 0) >= PERFORMANCE_THRESHOLDS['min_f1_score'],
    }
    return all(checks.values()), checks

# ============================================================================

if __name__ == "__main__":
    print("Configuration loaded successfully!")
    print(f"\nModel Parameters: {MODEL_CONFIG}")
    print(f"\nData Paths: {DATA_PATHS}")
    print(f"\nRisk Thresholds: {RISK_THRESHOLDS}")
