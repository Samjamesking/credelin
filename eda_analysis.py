"""
Data Analysis and Exploratory Data Analysis (EDA) Tools
For understanding the credit delinquency dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class DataAnalyzer:
    """Analyze credit delinquency data"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load dataset"""
        print(f"Loading data from {self.filepath}...")
        if self.filepath.endswith('.xlsx') or self.filepath.endswith('.xls'):
            self.df = pd.read_excel(self.filepath)
        else:
            self.df = pd.read_csv(self.filepath)
        print(f"✓ Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
    
    def basic_statistics(self):
        """Print basic statistics"""
        print("\n" + "="*60)
        print("BASIC STATISTICS")
        print("="*60)
        
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"Memory Usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\n--- Data Types ---")
        print(self.df.dtypes)
        
        print("\n--- Missing Values ---")
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0])
        else:
            print("No missing values found ✓")
        
        print("\n--- Duplicate Rows ---")
        duplicates = self.df.duplicated().sum()
        print(f"Duplicate rows: {duplicates}")
        
        print("\n--- Column Summary ---")
        for col in self.df.columns:
            print(f"\n{col}:")
            print(f"  Type: {self.df[col].dtype}")
            print(f"  Unique values: {self.df[col].nunique()}")
            if self.df[col].dtype in ['int64', 'float64']:
                print(f"  Range: [{self.df[col].min()}, {self.df[col].max()}]")
                print(f"  Mean: {self.df[col].mean():.2f}, Std: {self.df[col].std():.2f}")
            else:
                print(f"  Top values: {self.df[col].value_counts().head(3).to_dict()}")
    
    def numeric_statistics(self):
        """Descriptive statistics for numeric columns"""
        print("\n" + "="*60)
        print("NUMERIC STATISTICS")
        print("="*60)
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) > 0:
            print("\n" + numeric_df.describe().to_string())
        else:
            print("No numeric columns found")
    
    def categorical_analysis(self):
        """Analyze categorical columns"""
        print("\n" + "="*60)
        print("CATEGORICAL ANALYSIS")
        print("="*60)
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        if len(categorical_cols) == 0:
            print("No categorical columns found")
            return
        
        for col in categorical_cols:
            print(f"\n{col}:")
            vc = self.df[col].value_counts()
            print(vc)
            print(f"Percentage distribution:")
            print(self.df[col].value_counts(normalize=True) * 100)
    
    def target_analysis(self):
        """Analyze target variable (last column)"""
        print("\n" + "="*60)
        print("TARGET VARIABLE ANALYSIS")
        print("="*60)
        
        target_col = self.df.iloc[:, -1]
        print(f"\nTarget Column: {self.df.columns[-1]}")
        print(f"Type: {target_col.dtype}")
        print(f"\nClass Distribution:")
        print(target_col.value_counts())
        print(f"\nClass Distribution (%):")
        print((target_col.value_counts() / len(target_col) * 100).round(2))
        
        # Check for imbalance
        counts = target_col.value_counts()
        if len(counts) == 2:
            ratio = counts.max() / counts.min()
            print(f"\nClass Imbalance Ratio: {ratio:.2f}:1")
            if ratio > 5:
                print("⚠️  High class imbalance detected! Consider using class_weight='balanced'")
    
    def correlation_analysis(self):
        """Analyze feature correlations"""
        print("\n" + "="*60)
        print("CORRELATION ANALYSIS")
        print("="*60)
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            print("Less than 2 numeric columns - skipping correlation analysis")
            return
        
        corr_matrix = numeric_df.corr()
        
        print("\nHigh Correlations with Target (last column):")
        if len(numeric_df.columns) > 1:
            target_corr = corr_matrix.iloc[:, -1].sort_values(ascending=False)
            print(target_corr)
        
        print("\nFeature Correlations (top 10 pairs):")
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Var1': corr_matrix.columns[i],
                    'Var2': corr_matrix.columns[j],
                    'Correlation': corr_matrix.iloc[i, j]
                })
        
        corr_pairs_sorted = sorted(corr_pairs, key=lambda x: abs(x['Correlation']), reverse=True)
        for pair in corr_pairs_sorted[:10]:
            print(f"{pair['Var1']} <-> {pair['Var2']}: {pair['Correlation']:.4f}")
    
    def outlier_detection(self):
        """Detect outliers in numeric columns"""
        print("\n" + "="*60)
        print("OUTLIER DETECTION")
        print("="*60)
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) == 0:
            print("No numeric columns found")
            return
        
        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = numeric_df[(numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)]
            
            if len(outliers) > 0:
                print(f"\n{col}: {len(outliers)} outliers detected ({len(outliers)/len(numeric_df)*100:.2f}%)")
                print(f"  Bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    
    def data_quality_report(self):
        """Generate comprehensive data quality report"""
        print("\n" + "="*60)
        print("DATA QUALITY REPORT")
        print("="*60)
        
        # Completeness
        completeness = (1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        print(f"\n✓ Completeness: {completeness:.2f}%")
        
        # Uniqueness
        print(f"✓ Unique Rows: {len(self.df) - self.df.duplicated().sum()} / {len(self.df)}")
        
        # Consistency
        print(f"✓ Columns: {len(self.df.columns)}")
        print(f"✓ Rows: {len(self.df)}")
        
        # Information
        print(f"\n✓ Numeric Columns: {len(self.df.select_dtypes(include=[np.number]).columns)}")
        print(f"✓ Categorical Columns: {len(self.df.select_dtypes(include=['object']).columns)}")
        
        print("\n✓ Dataset appears valid for modeling!")


def run_eda(filepath):
    """Run complete exploratory data analysis"""
    analyzer = DataAnalyzer(filepath)
    
    analyzer.basic_statistics()
    analyzer.numeric_statistics()
    analyzer.categorical_analysis()
    analyzer.target_analysis()
    analyzer.correlation_analysis()
    analyzer.outlier_detection()
    analyzer.data_quality_report()
    
    print("\n" + "="*60)
    print("EDA COMPLETE")
    print("="*60)


if __name__ == "__main__":
    # Analyze training dataset
    print("\n📊 ANALYZING TRAINING DATASET")
    run_eda(r'E:\New Model\train_u6lujuX_CVtuZ9i.xlsx')
    
    # Analyze test dataset
    print("\n\n📊 ANALYZING TEST DATASET")
    run_eda(r'E:\New Model\test_Y3wMUE5_7gLdaTN.xlsx')
