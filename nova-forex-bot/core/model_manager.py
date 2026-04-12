import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import os
import pickle

class ModelManager:
    def __init__(self, xgb_path='models/nova_xgb.json', rf_path='models/nova_rf.pkl'):
        self.xgb_path = xgb_path
        self.rf_path = rf_path
        self.model_xgb = None
        self.model_rf = None
        os.makedirs('models', exist_ok=True)

    def train(self, df):
        """
        Trains both XGBoost and Random Forest models for the Dual-Ensemble.
        """
        X = df[['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100', 'rsi_50', 'bb_zscore']]
        y = df['target']
        
        # Chronological Split (Last 20% for validation)
        split_idx = int(len(df) * 0.8)
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        print("Training Ensemble Model A: XGBoost...")
        self.model_xgb = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            objective='binary:logistic',
            n_jobs=-1,
            tree_method='hist'
        )
        self.model_xgb.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        self.model_xgb.save_model(self.xgb_path)
        
        print("Training Ensemble Model B: Random Forest...")
        self.model_rf = RandomForestClassifier(
            n_estimators=50,
            max_depth=6,
            n_jobs=-1,
            random_state=42
        )
        self.model_rf.fit(X_train, y_train)
        with open(self.rf_path, 'wb') as f:
            pickle.dump(self.model_rf, f)
            
        print("Dual-Ensemble Brain synchronization complete.")

    def load(self):
        if os.path.exists(self.xgb_path) and os.path.exists(self.rf_path):
            self.model_xgb = xgb.XGBClassifier()
            self.model_xgb.load_model(self.xgb_path)
            
            with open(self.rf_path, 'rb') as f:
                self.model_rf = pickle.load(f)
            return True
        return False

    def predict_probability(self, features):
        """
        Returns the Soft-Voted probability from BOTH hemispheres.
        """
        if self.model_xgb is None or self.model_rf is None:
            if not self.load():
                return 0.0
        
        # Get probability from both models
        prob_xgb = self.model_xgb.predict_proba(features)[0][1]
        prob_rf = self.model_rf.predict_proba(features)[0][1]
        
        # Soft Voting (Average)
        return (prob_xgb + prob_rf) / 2.0
