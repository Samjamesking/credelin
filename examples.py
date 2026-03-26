"""
Example Usage Scripts
Demonstrates how to use the Credit Delinquency Prediction System
"""

import pandas as pd
from model_training import CreditDelinquencyModel
from prediction_api import PredictionAPI
import json


# =============================================================================
# EXAMPLE 1: Train Model from Scratch
# =============================================================================

def example_1_train_model():
    """Example: Train a new Random Forest model"""
    print("\n" + "="*70)
    print("EXAMPLE 1: TRAIN MODEL FROM SCRATCH")
    print("="*70)
    
    # Initialize model
    model = CreditDelinquencyModel()
    
    # Load data
    train_path = r'E:\New Model\train_u6lujuX_CVtuZ9i.xlsx'
    test_path = r'E:\New Model\test_Y3wMUE5_7gLdaTN.xlsx'
    
    train_df, test_df = model.load_data(train_path, test_path)
    
    # Train
    model.train(train_df)
    
    # Evaluate
    if test_df is not None:
        model.evaluate(test_df)
    
    # Save
    model.save_model()
    
    print("\n✓ Model training complete!")


# =============================================================================
# EXAMPLE 2: Load Trained Model and Make Single Prediction
# =============================================================================

def example_2_single_prediction():
    """Example: Load model and predict for a single customer"""
    print("\n" + "="*70)
    print("EXAMPLE 2: SINGLE PREDICTION")
    print("="*70)
    
    # Initialize API
    api = PredictionAPI()
    
    # Create sample customer data
    # NOTE: Adjust these features based on your actual dataset
    customer_data = {
        'Age': 35,
        'Income': 50000,
        'LoanAmount': 25000,
        'CreditScore': 720,
        'Employment': 'Employed',
        # Add more features as needed...
    }
    
    # Make prediction
    result = api.predict_single(customer_data)
    
    print("\nCustomer Data:")
    print(json.dumps(customer_data, indent=2))
    
    print("\nPrediction Result:")
    print(json.dumps(result, indent=2))
    
    # Interpret result
    if result['success']:
        prob = result['probability_delinquent']
        risk = result['risk_level']
        print(f"\n✓ Prediction: {risk} Risk ({prob:.1%} chance of delinquency)")
    else:
        print(f"\n✗ Error: {result.get('error', 'Unknown error')}")


# =============================================================================
# EXAMPLE 3: Batch Predictions from DataFrame
# =============================================================================

def example_3_batch_predictions():
    """Example: Make predictions for multiple customers"""
    print("\n" + "="*70)
    print("EXAMPLE 3: BATCH PREDICTIONS")
    print("="*70)
    
    # Initialize API
    api = PredictionAPI()
    
    # Load customer data
    customers_df = pd.read_excel(r'E:\New Model\test_Y3wMUE5_7gLdaTN.xlsx')
    
    print(f"\nProcessing {len(customers_df)} customers...")
    
    # Make predictions
    results_df = api.predict_from_dataframe(customers_df)
    
    # Display summary
    print("\nResults Summary:")
    print(f"Total: {len(results_df)}")
    print(f"Low Risk: {(results_df['risk_level'] == 'Low').sum()}")
    print(f"Medium Risk: {(results_df['risk_level'] == 'Medium').sum()}")
    print(f"High Risk: {(results_df['risk_level'] == 'High').sum()}")
    
    print("\nTop 10 Highest Risk Customers:")
    high_risk = results_df.nlargest(10, 'probability_delinquent')[
        ['probability_delinquent', 'risk_level']
    ]
    print(high_risk)
    
    # Save results
    output_path = r'E:\New Model\predictions_example.csv'
    results_df.to_csv(output_path, index=False)
    print(f"\n✓ Results saved to: {output_path}")


# =============================================================================
# EXAMPLE 4: Feature Importance Analysis
# =============================================================================

def example_4_feature_importance():
    """Example: Analyze which features matter most"""
    print("\n" + "="*70)
    print("EXAMPLE 4: FEATURE IMPORTANCE ANALYSIS")
    print("="*70)
    
    # Initialize API
    api = PredictionAPI()
    
    # Get feature importance
    importance = api.get_feature_importance()
    
    print("\nTop 15 Most Important Features:")
    print("-" * 50)
    
    for i, (feature, score) in enumerate(list(importance.items())[:15], 1):
        bar = "█" * int(score * 100)
        print(f"{i:2d}. {feature:25s} {score:6.4f} {bar}")
    
    print("\nInterpretation:")
    print("- Features at the top have the most influence on predictions")
    print("- Focus on these features for data quality and collection")


# =============================================================================
# EXAMPLE 5: Model Information
# =============================================================================

def example_5_model_info():
    """Example: Get model configuration and statistics"""
    print("\n" + "="*70)
    print("EXAMPLE 5: MODEL INFORMATION")
    print("="*70)
    
    # Initialize API
    api = PredictionAPI()
    
    # Get model info
    info = api.get_model_info()
    
    print("\nModel Configuration:")
    print(json.dumps(info, indent=2, default=str))


# =============================================================================
# EXAMPLE 6: Custom Batch Processing
# =============================================================================

def example_6_custom_batch():
    """Example: Process custom customer list"""
    print("\n" + "="*70)
    print("EXAMPLE 6: CUSTOM BATCH PROCESSING")
    print("="*70)
    
    # Initialize API
    api = PredictionAPI()
    
    # Create custom customer list
    customers = [
        {
            'Age': 25, 'Income': 30000, 'LoanAmount': 15000,
            'CreditScore': 600, 'Employment': 'Employed'
        },
        {
            'Age': 45, 'Income': 80000, 'LoanAmount': 50000,
            'CreditScore': 750, 'Employment': 'Employed'
        },
        {
            'Age': 35, 'Income': 45000, 'LoanAmount': 30000,
            'CreditScore': 700, 'Employment': 'Self-Employed'
        },
    ]
    
    print(f"\nProcessing {len(customers)} customers...")
    
    # Make predictions
    results = api.predict_batch(customers)
    
    # Display results
    print("\nPrediction Results:")
    for i, result in enumerate(results, 1):
        if result['success']:
            print(f"\nCustomer {i}:")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Delinquency Probability: {result['probability_delinquent']:.2%}")
        else:
            print(f"\nCustomer {i}: ✗ {result.get('error', 'Error')}")


# =============================================================================
# EXAMPLE 7: Comparison Analysis
# =============================================================================

def example_7_comparison():
    """Example: Compare predictions across different scenarios"""
    print("\n" + "="*70)
    print("EXAMPLE 7: COMPARISON ANALYSIS")
    print("="*70)
    
    api = PredictionAPI()
    
    # Define scenarios
    scenarios = {
        'Low Income, Low Credit Score': {
            'Age': 28, 'Income': 25000, 'LoanAmount': 10000,
            'CreditScore': 550, 'Employment': 'Employed'
        },
        'High Income, High Credit Score': {
            'Age': 28, 'Income': 100000, 'LoanAmount': 50000,
            'CreditScore': 800, 'Employment': 'Employed'
        },
        'Mid Range, Average Profile': {
            'Age': 28, 'Income': 50000, 'LoanAmount': 25000,
            'CreditScore': 700, 'Employment': 'Employed'
        },
    }
    
    print("\nScenario Comparison (Age 28, employed):\n")
    print(f"{'Scenario':<40} {'Probability':<15} {'Risk Level':<12}")
    print("-" * 70)
    
    for scenario_name, data in scenarios.items():
        result = api.predict_single(data)
        if result['success']:
            prob = result['probability_delinquent']
            risk = result['risk_level']
            print(f"{scenario_name:<40} {prob:>8.1%}         {risk:<12}")


# =============================================================================
# EXAMPLE 8: Export Model Predictions to Excel
# =============================================================================

def example_8_export_to_excel():
    """Example: Export predictions to Excel with formatting"""
    print("\n" + "="*70)
    print("EXAMPLE 8: EXPORT TO EXCEL")
    print("="*70)
    
    api = PredictionAPI()
    
    # Load test data
    test_df = pd.read_excel(r'E:\New Model\test_Y3wMUE5_7gLdaTN.xlsx')
    
    # Make predictions
    results_df = api.predict_from_dataframe(test_df)
    
    # Create Excel file
    output_path = r'E:\New Model\predictions_formatted.xlsx'
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        results_df.to_excel(writer, sheet_name='Predictions', index=False)
    
    print(f"✓ Predictions exported to: {output_path}")
    print(f"  Total rows: {len(results_df)}")
    print(f"  Columns: {list(results_df.columns)[:5]}... (and more)")


# =============================================================================
# MAIN - RUN ALL EXAMPLES (Choose which ones to run)
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CREDIT DELINQUENCY PREDICTION - USAGE EXAMPLES")
    print("="*70)
    print("\nSelect which examples to run:\n")
    print("1. Train Model from Scratch")
    print("2. Single Prediction")
    print("3. Batch Predictions")
    print("4. Feature Importance Analysis")
    print("5. Model Information")
    print("6. Custom Batch Processing")
    print("7. Comparison Analysis")
    print("8. Export to Excel")
    print("9. Run All Examples\n")
    
    choice = input("Enter your choice (1-9) [default: 9]: ").strip() or "9"
    
    try:
        if choice == "1":
            example_1_train_model()
        elif choice == "2":
            example_2_single_prediction()
        elif choice == "3":
            example_3_batch_predictions()
        elif choice == "4":
            example_4_feature_importance()
        elif choice == "5":
            example_5_model_info()
        elif choice == "6":
            example_6_custom_batch()
        elif choice == "7":
            example_7_comparison()
        elif choice == "8":
            example_8_export_to_excel()
        elif choice == "9":
            print("\nRunning all examples...\n")
            example_5_model_info()
            example_4_feature_importance()
            example_2_single_prediction()
            example_6_custom_batch()
            example_7_comparison()
        else:
            print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("Make sure you have:")
        print("  1. Run 'pip install -r requirements.txt'")
        print("  2. Run 'python model_training.py' to train the model first")
