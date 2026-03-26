"""
API Interface for Credit Delinquency Predictions
Enables programmatic access to the trained model
"""

import json
from typing import Dict, List, Tuple
import pandas as pd
import joblib
from model_training import CreditDelinquencyModel


class PredictionAPI:
    """API interface for model predictions"""
    
    def __init__(self):
        self.model = CreditDelinquencyModel()
        self.model.load_model(
            model_path='e:/New Model/credit_delinquency_model.pkl',
            encoder_path='e:/New Model/label_encoders.pkl'
        )
        self.is_ready = True
    
    def predict_single(self, customer_data: Dict) -> Dict:
        """
        Make single prediction from dictionary
        
        Args:
            customer_data: Dictionary with customer features
            
        Returns:
            Dictionary with prediction and probability
        """
        df = pd.DataFrame([customer_data])
        prediction, probability = self.model.predict(df)
        
        return {
            'success': True,
            'prediction': int(prediction[0]),
            'probability_non_delinquent': float(probability[0][0]),
            'probability_delinquent': float(probability[0][1]),
            'risk_level': self._get_risk_level(probability[0][1])
        }
    
    def predict_batch(self, customer_list: List[Dict]) -> List[Dict]:
        """
        Make batch predictions
        
        Args:
            customer_list: List of dictionaries with customer features
            
        Returns:
            List of prediction dictionaries
        """
        results = []
        for customer in customer_list:
            try:
                result = self.predict_single(customer)
                result['input'] = customer
            except Exception as e:
                result = {
                    'success': False,
                    'error': str(e),
                    'input': customer
                }
            results.append(result)
        
        return results
    
    def predict_from_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions from DataFrame
        
        Args:
            df: DataFrame with customer features
            
        Returns:
            DataFrame with original data plus predictions
        """
        predictions, probabilities = self.model.predict(df)
        
        result_df = df.copy()
        result_df['prediction'] = predictions
        result_df['probability_delinquent'] = probabilities[:, 1]
        result_df['probability_non_delinquent'] = probabilities[:, 0]
        result_df['risk_level'] = result_df['probability_delinquent'].apply(
            lambda x: self._get_risk_level(x)
        )
        
        return result_df
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        importance_dict = {}
        for feature, importance in zip(
            self.model.feature_names,
            self.model.model.feature_importances_
        ):
            importance_dict[feature] = float(importance)
        
        # Sort by importance
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        return {
            'model_type': 'RandomForestClassifier',
            'n_estimators': self.model.model.n_estimators,
            'max_depth': self.model.model.max_depth,
            'min_samples_split': self.model.model.min_samples_split,
            'min_samples_leaf': self.model.model.min_samples_leaf,
            'n_features': len(self.model.feature_names),
            'features': self.model.feature_names,
            'target': self.model.target_column
        }
    
    def _get_risk_level(self, probability: float) -> str:
        """Classify risk level based on probability"""
        if probability < 0.3:
            return 'Low'
        elif probability < 0.6:
            return 'Medium'
        else:
            return 'High'


# Example usage and testing
def test_api():
    """Test the API with sample data"""
    print("="*60)
    print("CREDIT DELINQUENCY PREDICTION API TEST")
    print("="*60)
    
    # Initialize API
    api = PredictionAPI()
    print("\n✓ API initialized successfully")
    
    # Get model info
    print("\n--- Model Information ---")
    model_info = api.get_model_info()
    print(json.dumps(model_info, indent=2))
    
    # Get feature importance
    print("\n--- Top 10 Most Important Features ---")
    importance = api.get_feature_importance()
    for i, (feature, score) in enumerate(list(importance.items())[:10], 1):
        print(f"{i}. {feature}: {score:.4f}")
    
    # Test single prediction
    print("\n--- Single Prediction Test ---")
    sample_customer = {}
    
    # Create sample data with all required features
    numeric_features = [f for f in model_info['features'] 
                       if f not in api.model.label_encoders.keys()]
    categorical_features = list(api.model.label_encoders.keys())
    
    # Fill with dummy data
    for feature in numeric_features:
        sample_customer[feature] = 50.0
    
    for feature in categorical_features:
        # Get first category from encoder
        encoder = api.model.label_encoders[feature]
        sample_customer[feature] = encoder.classes_[0]
    
    try:
        result = api.predict_single(sample_customer)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # Test batch prediction
    print("\n--- Batch Prediction Test ---")
    customers = [sample_customer for _ in range(3)]
    
    try:
        batch_results = api.predict_batch(customers)
        print(f"Processed {len(batch_results)} predictions")
        print(f"Success rate: {sum(1 for r in batch_results if r.get('success', False))}/{len(batch_results)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60)
    print("API TEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    test_api()
