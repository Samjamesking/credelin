"""
Credit Delinquency Prediction Web App - Random Forest
Streamlit-based interactive application for credit delinquency prediction
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from pathlib import Path
import warnings
import shap
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Credit Delinquency Predictor",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
            background-color: #0F172A;
            color: #F8FAFC;
        }
        .stMetric {
            background-color: #1E293B;
            padding: 1rem;
            border-radius: 0.5rem;
            color: #F8FAFC;
            border: 1px solid #3B82F6;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #F8FAFC !important;
        }
        p, span, div {
            color: #F8FAFC !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_artifacts():
    """Load trained model and encoders"""
    try:
        rf_model = joblib.load('credit_delinquency_rf_model.pkl')
        encoders = joblib.load('label_encoders.pkl')
        config = joblib.load('model_config.pkl')
        return rf_model, encoders, config
    except FileNotFoundError:
        st.error("❌ Model files not found. Please train the model first by running model_training.py")
        return None, None, None

@st.cache_resource
def create_shap_explainer(_rf_model):
    """Create SHAP explainer for the Random Forest model
    
    Note: Parameter prefixed with _ to exclude from hashing since it's already cached
    """
    try:
        explainer = shap.TreeExplainer(_rf_model)
        return explainer
    except Exception as e:
        return None

def preprocess_input(data, encoders, config):
    """Preprocess user input data"""
    data_processed = data.copy()
    
    # Encode categorical columns
    for col, encoder in encoders.items():
        if col in data_processed.columns:
            data_processed[col] = encoder.transform(data_processed[col])
    
    # Ensure all features are present
    for feature in config['feature_names']:
        if feature not in data_processed.columns:
            data_processed[feature] = 0
    
    # Select only the required features
    X = data_processed[config['feature_names']]
    
    return X

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability < 0.3:
        return "🟢 Low Risk", "#10B981"
    elif probability < 0.6:
        return "🟡 Medium Risk", "#3B82F6"
    else:
        return "🔴 High Risk", "#EF4444"

def dashboard(rf_model, encoders, config):
    """Dashboard page with model information"""
    st.header("📊 Model Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Random Forest",
            value="✓ Active",
            delta="100 Trees"
        )
    
    with col2:
        st.metric(
            label="Total Features",
            value=config['n_features']
        )
    
    st.markdown("---")
    
    st.subheader("📈 Feature Information")
    st.write(f"**Target Variable:** {config['target_column']}")
    st.write(f"**Features:** {len(config['feature_names'])}")
    
    with st.expander("View All Features"):
        features_df = pd.DataFrame({
            'Feature': config['feature_names'],
            'Index': range(len(config['feature_names']))
        })
        st.dataframe(features_df, use_container_width='stretch')
    
    st.markdown("---")
    
    st.subheader("ℹ️ About This Model")
    st.info("""
    ### Credit Delinquency Prediction - Random Forest Classifier
    
    This system uses a **Random Forest Classifier** to predict credit delinquency:
    
    #### Random Forest Classifier
    - **Advantages**: Handles non-linear relationships, robust to outliers, provides feature importance
    - **Configuration**: 100 trees, max_depth=15, balanced classes
    - **Performance**: Excellent accuracy and recall on credit delinquency prediction
    
    #### Key Features
    - Captures complex patterns and feature interactions
    - Resistant to overfitting through ensemble averaging
    - Provides interpretable feature importance rankings
    """)

def single_prediction(rf_model, encoders, config):
    """Single prediction page"""
    st.header("🔮 Single Credit Delinquency Prediction")
    
    st.markdown("---")
    
    # Create input form
    with st.form("prediction_form"):
        st.subheader("Enter Customer Information")
        
        # Display input fields based on actual features
        input_data = {}
        
        # Get categorical vs numeric features from encoders
        categorical_features = list(encoders.keys())
        numeric_features = [f for f in config['feature_names'] if f not in categorical_features]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Numeric inputs
            for feature in numeric_features[:len(numeric_features)//2]:
                input_data[feature] = st.number_input(
                    label=f"{feature}",
                    value=0.0,
                    step=0.01
                )
        
        with col2:
            # Numeric inputs (continued)
            for feature in numeric_features[len(numeric_features)//2:]:
                input_data[feature] = st.number_input(
                    label=f"{feature}",
                    value=0.0,
                    step=0.01
                )
        
        # Categorical inputs
        for feature in categorical_features:
            encoder = encoders[feature]
            options = list(encoder.classes_)
            input_data[feature] = st.selectbox(
                label=f"{feature}",
                options=options
            )
        
        # Submit button
        submitted = st.form_submit_button("📊 Make Prediction", use_container_width=True)
    
    if submitted:
        # Prepare data
        df_input = pd.DataFrame([input_data])
        
        # Preprocess
        X = preprocess_input(df_input, encoders, config)
        
        st.markdown("---")
        st.subheader("📋 Prediction Results")
        
        # Random Forest prediction
        rf_pred = rf_model.predict(X)[0]
        rf_proba = rf_model.predict_proba(X)[0]
        rf_delinquency_prob = rf_proba[1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            risk_label, risk_color = get_risk_level(rf_delinquency_prob)
            st.markdown(f"<h3 style='color: {risk_color};'>{risk_label}</h3>", unsafe_allow_html=True)
        with col2:
            st.metric("Delinquency Risk", f"{rf_delinquency_prob:.2%}")
        with col3:
            st.metric("Non-Delinquency", f"{(1-rf_delinquency_prob):.2%}")
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(
                x=['Non-Delinquent', 'Delinquent'],
                y=[1 - rf_delinquency_prob, rf_delinquency_prob],
                marker=dict(color=['#10B981', '#EF4444']),
                text=[f'{(1-rf_delinquency_prob):.2%}', f'{rf_delinquency_prob:.2%}'],
                textposition='auto',
            )
        ])
        fig.update_layout(
            title="Random Forest - Prediction Distribution",
            yaxis_title="Probability",
            showlegend=False,
            height=400,
            paper_bgcolor='#0F172A',
            plot_bgcolor='#1E293B',
            font=dict(color='#F8FAFC')
        )
        st.plotly_chart(fig, use_container_width='stretch')
        
        # ============================================
        # SHAP EXPLAINABILITY SECTION
        # ============================================
        st.markdown("---")
        st.subheader("🔍 Explainable AI - SHAP Analysis")
        
        # Create SHAP explainer
        explainer = create_shap_explainer(rf_model)
        
        if explainer is not None:
            try:
                # Calculate SHAP values for this prediction
                shap_values = explainer.shap_values(X)
                
                # For binary classification, take the positive class (delinquency)
                if isinstance(shap_values, list):
                    shap_values_delinq = shap_values[1]
                else:
                    shap_values_delinq = shap_values
                
                col_shap1, col_shap2 = st.columns(2)
                
                with col_shap1:
                    st.markdown("#### 📊 Global Feature Importance")
                    st.info(
                        "Shows which features are most important for the model overall, "
                        "based on average absolute SHAP values across all predictions."
                    )
                    
                    # Create global feature importance plot
                    try:
                        # Calculate mean absolute SHAP values for all features
                        feature_importance = np.abs(shap_values_delinq).mean(axis=0)
                        importance_df = pd.DataFrame({
                            'Feature': config['feature_names'],
                            'Importance': feature_importance
                        }).sort_values('Importance', ascending=False).head(10)
                        
                        fig_importance = go.Figure(data=[
                            go.Bar(
                                y=importance_df['Feature'],
                                x=importance_df['Importance'],
                                orientation='h',
                                marker=dict(color='#3B82F6')
                            )
                        ])
                        fig_importance.update_layout(
                            title="Top 10 Most Important Features",
                            xaxis_title="Mean |SHAP value|",
                            height=400,
                            paper_bgcolor='#0F172A',
                            plot_bgcolor='#1E293B',
                            font=dict(color='#F8FAFC'),
                            showlegend=False
                        )
                        st.plotly_chart(fig_importance, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not display global importance: {str(e)}")
                
                with col_shap2:
                    st.markdown("#### 🎯 Individual Prediction Explanation")
                    st.info(
                        "Shows which features pushed the prediction towards delinquency (red) "
                        "and which pushed it away (blue) for this specific customer."
                    )
                    
                    # Create individual prediction explanation
                    try:
                        # Get SHAP values for this instance
                        shap_vals_instance = shap_values_delinq[0]
                        
                        # Create dataframe for visualization
                        explanation_df = pd.DataFrame({
                            'Feature': config['feature_names'],
                            'SHAP Value': shap_vals_instance,
                            'Abs SHAP': np.abs(shap_vals_instance)
                        }).sort_values('Abs SHAP', ascending=False).head(10)
                        
                        # Determine colors: red for positive (towards delinquency), blue for negative
                        colors = ['#EF4444' if x > 0 else '#3B82F6' for x in explanation_df['SHAP Value']]
                        
                        fig_explain = go.Figure(data=[
                            go.Bar(
                                y=explanation_df['Feature'],
                                x=explanation_df['SHAP Value'],
                                orientation='h',
                                marker=dict(color=colors)
                            )
                        ])
                        fig_explain.update_layout(
                            title="Top 10 Features Affecting This Prediction",
                            xaxis_title="SHAP Value (Red=Towards Delinquency, Blue=Away from Delinquency)",
                            height=400,
                            paper_bgcolor='#0F172A',
                            plot_bgcolor='#1E293B',
                            font=dict(color='#F8FAFC'),
                            showlegend=False
                        )
                        st.plotly_chart(fig_explain, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not display prediction explanation: {str(e)}")
                
                # Detailed SHAP explanation table
                st.markdown("---")
                st.markdown("#### 📈 Detailed SHAP Values")
                
                try:
                    # Ensure SHAP values are 1D
                    shap_vals_flat = np.asarray(shap_values_delinq[0]).flatten()
                    input_vals_flat = np.asarray(X.iloc[0].values).flatten()
                    
                    # Ensure all arrays have the same length
                    n_features = min(len(shap_vals_flat), len(input_vals_flat), len(config['feature_names']))
                    feature_names_subset = config['feature_names'][:n_features]
                    
                    shap_explanation = pd.DataFrame({
                        'Feature': feature_names_subset,
                        'Input Value': input_vals_flat[:n_features],
                        'SHAP Value': shap_vals_flat[:n_features],
                        'Impact': ['Increases Risk' if float(x) > 0 else 'Decreases Risk' for x in shap_vals_flat[:n_features]],
                        'Abs Impact': np.abs(shap_vals_flat[:n_features])
                    }).sort_values('Abs Impact', ascending=False)
                    
                    st.dataframe(
                        shap_explanation.style.format({
                            'Input Value': '{:.4f}',
                            'SHAP Value': '{:.6f}',
                            'Abs Impact': '{:.6f}'
                        }),
                        use_container_width=True,
                        height=500
                    )
                except Exception as e:
                    st.warning(f"Could not display SHAP table: {str(e)}")
                    
            except Exception as e:
                st.error(f"Error calculating SHAP values: {str(e)}")
        else:
            st.warning("SHAP explainer could not be created. Proceeding with standard predictions only.")

def about():
    """About page"""
    st.header("ℹ️ About This Application")
    
    st.markdown("""
    ### Credit Delinquency Prediction System - Random Forest
    
    This application uses a **Random Forest Classifier** to predict credit delinquency.
    
    #### Random Forest Classifier
    **Configuration:**
    - 100 decision trees
    - Max depth: 15
    - Balanced class weights
    - Captures non-linear patterns and feature interactions
    
    **Key Features:**
    - Non-linear relationship modeling
    - Feature interaction handling
    - Automatic feature importance calculation
    - Robust to outliers and noise
    - Excellent performance on tabular data
    
    #### Usage Pages
    - **Dashboard**: View model configuration and feature information
    - **Single Prediction**: Enter customer data and get delinquency predictions
    - **About**: Information about the model and application
    
    #### Prediction Output
    Each prediction provides:
    1. **Risk Level**: Low (< 30%), Medium (30-60%), or High (> 60%)
    2. **Delinquency Probability**: Exact probability of credit delinquency
    3. **Non-Delinquency Probability**: Probability of no delinquency
    
    #### Business Applications
    - Credit risk assessment and scoring
    - Loan approval decisions
    - Portfolio risk management
    - Customer credit classification
    - Risk-based pricing and decision making
    
    #### Model Performance
    The Random Forest model has been trained on historical credit data to accurately
    predict customer delinquency risk based on their financial and demographic profile.
    
    ---
    **Version**: 1.0 (Random Forest)  
    **Status**: ✅ Production Ready  
    **Framework**: Streamlit + Scikit-learn
    """)

def main():
    # Header
    st.title("💳 Credit Delinquency Prediction System")
    st.markdown("**Random Forest Classifier**")
    st.markdown("---")
    
    # Load model
    rf_model, encoders, config = load_model_artifacts()
    
    if rf_model is None:
        st.stop()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Dashboard", "Single Prediction", "About"]
    )
    
    if page == "Dashboard":
        dashboard(rf_model, encoders, config)
    elif page == "Single Prediction":
        single_prediction(rf_model, encoders, config)
    else:
        about()

if __name__ == "__main__":
    main()

