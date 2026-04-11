import xgboost as xgb
import pandas as pd
import numpy as np
import os
import pickle

class ModelManager:
    def __init__(self, model_path='models/nova_hft_model.json'):
        self.model_path = model_path
        self.model = None
        os.makedirs('models', exist_ok=True)

    def train(self, df):
        """
        Trains the XGBoost model on chronologically split tick data.
        """
        X = df[['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100', 'vol_imbalance']]
        y = df['target']
        
        # Chronological Split (Last 20% for validation)
        split_idx = int(len(df) * 0.8)
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            objective='binary:logistic',
            n_jobs=-1,
            tree_method='hist'
        )
        
        print("Training Nova HFT Model (XGBoost)...")
        self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        
        # Save model
        self.model.save_model(self.model_path)
        print(f"Model saved to {self.model_path}")

    def load(self):
        if os.path.exists(self.model_path):
            self.model = xgb.XGBClassifier()
            self.model.load_model(self.model_path)
            return True
        return False

    def predict_probability(self, features):
        """
        Returns the probability of the Profit target being hit.
        """
        if self.model is None:
            if not self.load():
                return 0.0
        
        prob = self.model.predict_proba(features)
        return prob[0][1] # Probability of Class 1
