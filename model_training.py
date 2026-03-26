"""
Credit Delinquency Prediction - Model Training
Trains Random Forest classifier on credit delinquency data
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (classification_report, confusion_matrix, 
                             roc_auc_score, roc_curve, accuracy_score,
                             precision_score, recall_score, f1_score)
import joblib
import warnings
warnings.filterwarnings('ignore')


class CreditDelinquencyModel:
    """Random Forest classifier for credit delinquency prediction"""
    
    def __init__(self):
        self.rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=4,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        self.label_encoders = {}
        self.feature_names = None
        self.target_column = None
        
    def load_data(self, train_path, test_path=None):
        """Load training and test datasets"""
        print(f"Loading training data from {train_path}...")
        train_df = pd.read_excel(train_path)
        print(f"Training data shape: {train_df.shape}")
        
        if test_path:
            print(f"Loading test data from {test_path}...")
            test_df = pd.read_excel(test_path)
            print(f"Test data shape: {test_df.shape}")
            return train_df, test_df
        
        return train_df, None
    
    def preprocess_data(self, df, fit=True):
        """Preprocess features and handle missing values"""
        df_processed = df.copy()
        
        # Handle missing values
        print("\nHandling missing values...")
        numeric_cols = df_processed.select_dtypes(include=[np.number]).columns
        categorical_cols = df_processed.select_dtypes(include=['object']).columns
        
        # Fill numeric columns with median
        for col in numeric_cols:
            if df_processed[col].isnull().sum() > 0:
                df_processed[col].fillna(df_processed[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        for col in categorical_cols:
            if df_processed[col].isnull().sum() > 0:
                df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
        
        # Encode categorical variables (skip ID columns)
        print("Encoding categorical features...")
        for col in categorical_cols:
            # Skip ID columns - they shouldn't be encoded for prediction
            if 'id' in col.lower():
                continue
                
            # Convert to string to handle mixed types
            df_processed[col] = df_processed[col].astype(str)
            
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col])
            else:
                # Handle unknown categories by replacing with most common class
                try:
                    df_processed[col] = self.label_encoders[col].transform(df_processed[col])
                except ValueError as e:
                    # If unknown category, replace with first known class
                    known_classes = set(self.label_encoders[col].classes_)
                    df_processed[col] = df_processed[col].apply(
                        lambda x: x if x in known_classes else self.label_encoders[col].classes_[0]
                    )
                    df_processed[col] = self.label_encoders[col].transform(df_processed[col])
        
        return df_processed
    
    def train(self, train_df, target_column='target'):
        """Train Random Forest model"""
        print("\n" + "="*60)
        print("CREDIT DELINQUENCY PREDICTION - MODEL TRAINING")
        print("="*60)
        
        self.target_column = target_column
        
        # Preprocess data
        train_processed = self.preprocess_data(train_df, fit=True)
        
        # Separate features and target
        if target_column not in train_processed.columns:
            print(f"Target column '{target_column}' not found. Using last column as target.")
            target_column = train_processed.columns[-1]
            self.target_column = target_column
        
        # Drop ID columns as they shouldn't be features
        columns_to_drop = [col for col in train_processed.columns if 'id' in col.lower() or col == target_column]
        X = train_processed.drop(columns=columns_to_drop)
        y = train_processed[target_column]
        
        self.feature_names = X.columns.tolist()
        
        print(f"\nFeatures: {self.feature_names}")
        print(f"Target: {target_column}")
        print(f"Class distribution:\n{y.value_counts()}")
        
        # Train Random Forest
        print("\n" + "-"*60)
        print("TRAINING RANDOM FOREST")
        print("-"*60)
        self.rf_model.fit(X, y)
        
        y_pred = self.rf_model.predict(X)
        y_pred_proba = self.rf_model.predict_proba(X)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, average='weighted'),
            'recall': recall_score(y, y_pred, average='weighted'),
            'f1': f1_score(y, y_pred, average='weighted'),
        }
        
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-Score: {metrics['f1']:.4f}")
        
        try:
            metrics['roc_auc'] = roc_auc_score(y, y_pred_proba)
            print(f"ROC-AUC Score: {metrics['roc_auc']:.4f}")
        except:
            print("ROC-AUC Score: N/A")
        
        # Feature importance
        print("\nTop 10 Most Important Features:")
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for idx, row in feature_importance.head(10).iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")
        
        return self
    
    def evaluate(self, test_df):
        """Evaluate model on test data"""
        print("\n" + "="*60)
        print("MODEL EVALUATION ON TEST DATA")
        print("="*60)
        
        # Preprocess test data
        test_processed = self.preprocess_data(test_df, fit=False)
        
        # Separate features and target (drop ID columns)
        columns_to_drop = [col for col in test_processed.columns if 'id' in col.lower()]
        if self.target_column in test_processed.columns:
            columns_to_drop.append(self.target_column)
        
        X_test = test_processed.drop(columns=columns_to_drop)
        y_test = test_processed[self.target_column] if self.target_column in test_processed.columns else None
        
        print(f"\nTest set size: {len(X_test)}")
        if y_test is not None:
            print(f"Class distribution:\n{y_test.value_counts()}")
        
        if y_test is not None:
            print("\n" + "-"*60)
            print("TEST RESULTS")
            print("-"*60)
            y_pred = self.rf_model.predict(X_test)
            y_pred_proba = self.rf_model.predict_proba(X_test)[:, 1]
            
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted'),
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1': f1_score(y_test, y_pred, average='weighted'),
            }
            
            print(f"Accuracy: {metrics['accuracy']:.4f}")
            print(f"Precision: {metrics['precision']:.4f}")
            print(f"Recall: {metrics['recall']:.4f}")
            print(f"F1-Score: {metrics['f1']:.4f}")
            
            try:
                metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
                print(f"ROC-AUC Score: {metrics['roc_auc']:.4f}")
            except:
                print("ROC-AUC Score: N/A")
            
            print("\nConfusion Matrix:")
            print(confusion_matrix(y_test, y_pred))
            
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))
            
            return {
                'accuracy': metrics['accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1': metrics['f1'],
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba,
                'y_test': y_test
            }
        else:
            print("\nNo target column found in test data - predictions only.")
            y_pred = self.rf_model.predict(X_test)
            y_pred_proba = self.rf_model.predict_proba(X_test)[:, 1]
            return {
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
    
    def save_model(self, rf_path='credit_delinquency_rf_model.pkl',
                   encoder_path='label_encoders.pkl'):
        """Save trained model and encoders"""
        joblib.dump(self.rf_model, rf_path)
        joblib.dump(self.label_encoders, encoder_path)
        
        # Save feature names and target column
        config = {
            'feature_names': self.feature_names,
            'target_column': self.target_column,
            'n_features': len(self.feature_names)
        }
        joblib.dump(config, 'model_config.pkl')
        
        print(f"\nRandom Forest model saved to {rf_path}")
        print(f"Encoders saved to {encoder_path}")
        print(f"Config saved to model_config.pkl")
    
    def predict(self, X, model_type='rf'):
        """Make predictions"""
        return self.rf_model.predict(X)


if __name__ == "__main__":
    # Paths to data
    TRAIN_DATA_PATH = 'e:/New Model/train.xlsx'
    TEST_DATA_PATH = 'e:/New Model/test.xlsx'
    
    # Create and train model
    model = CreditDelinquencyModel()
    
    # Load data
    train_df, test_df = model.load_data(TRAIN_DATA_PATH, TEST_DATA_PATH)
    
    # Train model
    model.train(train_df)
    
    # Evaluate on test data if available
    if test_df is not None:
        model.evaluate(test_df)
    
    # Save model
    model.save_model(
        rf_path='e:/New Model/credit_delinquency_rf_model.pkl',
        encoder_path='e:/New Model/label_encoders.pkl'
    )
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
