import pandas as pd
import numpy as np
import os
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from config import MODELS_DIR

logger = logging.getLogger(__name__)

class AIFilter:
    def __init__(self, model_name="trade_probability_model.pkl", threshold=0.65):
        self.model_path = os.path.join(MODELS_DIR, model_name)
        self.threshold = threshold
        self.model = None
        self.is_trained = False
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.is_trained = True
                logger.info(f"Loaded AI Model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load AI model: {e}")
        else:
            logger.warning("No trained AI model found. Trading will either pause or bypass filter depending on config.")

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features for the ML model from the current market state.
        Features: RSI value, ATR value, trend strength (ADX), distance_from_ema, volatility (BB bandwidth)
        """
        features = pd.DataFrame()
        
        # We need at least one row
        if df is None or len(df) == 0:
            return features
            
        # We extract from the last row (current signal)
        current = df.iloc[-1]
        
        features['RSI'] = [current.get('RSI', 50)]
        features['ATR'] = [current.get('ATR', 0)]
        features['ADX'] = [current.get('ADX', 15)]
        
        # Distance from EMA 50 (normalized by price)
        ema50 = current.get('EMA_50', current['close'])
        features['dist_ema50'] = [(current['close'] - ema50) / ema50]
        
        features['volatility_bb'] = [current.get('BB_bandwidth', 0)]
        
        # Session time (hour of day)
        if isinstance(df.index, pd.DatetimeIndex):
            features['session_hour'] = [df.index[-1].hour]
        else:
            features['session_hour'] = [12]  # fallback
            
        return features

    def train(self, historical_trades_csv: str):
        """
        Trains the Random Forest model based on historical trades.
        The CSV requires the features columns + a 'success' column (1 or 0).
        """
        if not os.path.exists(historical_trades_csv):
            logger.error(f"Training data not found at {historical_trades_csv}")
            return False

        try:
            data = pd.read_csv(historical_trades_csv)
            # Ensure 'success' target column exists
            if 'success' not in data.columns:
                logger.error("The 'success' column is missing from training data.")
                return False
                
            X = data[['RSI', 'ATR', 'ADX', 'dist_ema50', 'volatility_bb', 'session_hour']]
            y = data['success']
            
            # Simple train-test split for evaluation
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
            self.model.fit(X_train, y_train)
            
            accuracy = self.model.score(X_test, y_test)
            logger.info(f"Model trained successfully. Test Accuracy: {accuracy*100:.2f}%")
            
            # Save the model
            joblib.dump(self.model, self.model_path)
            self.is_trained = True
            logger.info(f"Model saved to {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error during AI model training: {e}")
            return False

    def predict_probability(self, df: pd.DataFrame) -> float:
        """
        Returns the probability of success for the current market state.
        If model is not trained, it returns a 0.0 or a default bypass value.
        """
        if not self.is_trained or self.model is None:
            # If not trained, return 1.0 to bypass filter, or 0.0 to block trades.
            # Assuming we want to trade even before ML exists, we return 1.0, 
            # Or log a warning and let config dictate strict mode.
            # For strict adherence, we could return 0.0. Let's return 1.0 with a warning for practical boot-up.
            logger.debug("AI Model not trained. Passing signal by default.")
            return 1.0
            
        try:
            features = self.extract_features(df)
            # predict_proba returns array of probabilities for classes [0, 1]. We want class 1 (success).
            prob = self.model.predict_proba(features)[0][1]
            return float(prob)
        except Exception as e:
            logger.error(f"Error predicting probability: {e}")
            return 0.0

    def filter_signal(self, df: pd.DataFrame, signal: str) -> bool:
        """
        Returns True if the trade is approved by AI, False otherwise.
        """
        if signal == 'NO_TRADE':
            return False
            
        prob = self.predict_probability(df)
        if prob >= self.threshold:
            logger.info(f"AI Filter APPROVED trade ({signal}) with {prob*100:.1f}% probability.")
            return True
        else:
            logger.info(f"AI Filter REJECTED trade ({signal}). Probability {prob*100:.1f}% < {self.threshold*100}%.")
            return False
