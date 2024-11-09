import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model, save_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from glob import glob
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DiningHallPredictor:
    def __init__(self, model_dir='ml_models', data_dir='data'):
        """Initialize predictor with model and data directories"""
        self.dining_halls = ['Dana', 'Roberts', 'Foss']
        self.sequence_length = 6
        self.models = {}
        self.scalers = {}
        self.model_dir = model_dir
        self.data_dir = data_dir
        
        # Create required directories if they don't exist
        for directory in [model_dir, data_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
            
        # Try to load existing models
        self.load_saved_models()

    def load_saved_models(self):
        """Load pre-trained models if they exist"""
        for hall in self.dining_halls:
            model_path = os.path.join(self.model_dir, f'{hall.lower()}_model')
            scaler_path = os.path.join(self.model_dir, f'{hall.lower()}_scaler.npy')
            
            try:
                if os.path.exists(model_path) and os.path.exists(scaler_path):
                    self.models[hall] = load_model(model_path)
                    self.scalers[hall] = np.load(scaler_path, allow_pickle=True).item()
                    logger.info(f"Loaded saved model for {hall}")
            except Exception as e:
                logger.error(f"Error loading model for {hall}: {str(e)}")

    def save_models(self):
        """Save trained models and scalers"""
        for hall in self.dining_halls:
            if hall in self.models and hall in self.scalers:
                try:
                    model_path = os.path.join(self.model_dir, f'{hall.lower()}_model')
                    scaler_path = os.path.join(self.model_dir, f'{hall.lower()}_scaler.npy')
                    
                    self.models[hall].save(model_path)
                    np.save(scaler_path, self.scalers[hall])
                    logger.info(f"Saved model for {hall}")
                except Exception as e:
                    logger.error(f"Error saving model for {hall}: {str(e)}")

    def load_data(self, csv_pattern='October-*.csv'):
        """Load and combine data from multiple CSV files"""
        # Update the path to look in the data directory
        data_path = os.path.join(self.data_dir, csv_pattern)
        logger.info(f"Loading data from pattern: {data_path}")
        
        csv_files = glob(data_path)
        logger.info(f"Found {len(csv_files)} CSV files: {csv_files}")
        
        if len(csv_files) == 0:
            raise ValueError(f"No CSV files found in {self.data_dir} matching pattern {csv_pattern}")
        
        # Initialize the all_data list
        all_data = []  
        
        for file in csv_files:
            try:
                with open(file, 'r') as f:
                    lines = f.readlines()
                
                records = []
                for line in lines:
                    if 'Grand Total' in line:
                        continue
                    
                    parts = [p.strip() for p in line.split(',') if p.strip()]
                    for i in range(0, len(parts)-2, 3):
                        try:
                            datetime_str = parts[i]
                            location = parts[i+1]
                            count = int(parts[i+2])
                            
                            if location in self.dining_halls:
                                dt = pd.to_datetime(datetime_str, format='%m/%d/%y %H:%M')
                                records.append({
                                    'datetime': dt,
                                    'location': location,
                                    'count': count
                                })
                        except (ValueError, IndexError):
                            continue
                
                if records:
                    df = pd.DataFrame(records)
                    all_data.append(df)
                
            except Exception as e:
                logger.error(f"Error processing {file}: {str(e)}")
                continue
        
        if not all_data:
            raise ValueError("No data was successfully loaded from any CSV file")
        
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Add features
        combined_df['day_of_week'] = combined_df['datetime'].dt.dayofweek
        combined_df['hour'] = combined_df['datetime'].dt.hour
        combined_df['minute'] = combined_df['datetime'].dt.minute
        combined_df['is_weekend'] = combined_df['datetime'].dt.dayofweek >= 5
        
        return combined_df.sort_values('datetime')

    def prepare_sequences(self, data):
        """Create sequences for LSTM model"""
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:(i + self.sequence_length)])
            y.append(data[i + self.sequence_length])
        return np.array(X), np.array(y)

    def build_model(self, input_shape):
        """Build LSTM model"""
        model = Sequential([
            LSTM(64, activation='relu', input_shape=input_shape, return_sequences=True),
            Dropout(0.2),
            LSTM(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train_models(self, df, save=True):
        """Train models with option to save"""
        logger.info("Starting model training")
        
        for hall in self.dining_halls:
            try:
                logger.info(f"Training model for {hall}")
                
                # Filter data
                hall_data = df[df['location'] == hall].copy()
                if len(hall_data) == 0:
                    logger.warning(f"No data found for {hall}")
                    continue
                
                # Prepare features
                features = pd.DataFrame({
                    'count': hall_data['count'],
                    'hour': hall_data['hour'],
                    'minute': hall_data['minute'],
                    'day_of_week': hall_data['day_of_week'],
                    'is_weekend': hall_data['is_weekend'].astype(int)
                })
                
                # Scale features
                scaler = MinMaxScaler()
                scaled_data = scaler.fit_transform(features)
                
                # Create sequences
                X, y = self.prepare_sequences(scaled_data)
                
                # Split data and train
                train_size = int(len(X) * 0.8)
                X_train = X[:train_size]
                y_train = y[:train_size]
                
                model = self.build_model((self.sequence_length, X.shape[2]))
                
                model.fit(
                    X_train, y_train[:, 0],
                    epochs=50,
                    batch_size=32,
                    validation_split=0.2,
                    verbose=0
                )
                
                # Store model and scaler
                self.models[hall] = model
                self.scalers[hall] = scaler
                
                if save:
                    self.save_models()
                
                logger.info(f"Successfully trained model for {hall}")
                
            except Exception as e:
                logger.error(f"Error training model for {hall}: {str(e)}")
                continue

    def predict_wait_times(self, current_time, location):
        """
        Predict wait times based on dining hall swipe data.
        """
        try:
            # Validate inputs
            if location not in self.dining_halls:
                logger.error(f"Invalid location: {location}")
                return None
                    
            if location not in self.models or location not in self.scalers:
                logger.error(f"No model available for {location}")
                return None
            
            # Operating hours check (7 AM to 8 PM)
            if current_time.hour < 7 or current_time.hour >= 20:
                logger.info(f"{location} is closed at {current_time.hour}:00")
                return {
                    'status': 'closed',
                    'message': 'Dining hall is currently closed'
                }
            
            # Create feature vector for prediction
            features = pd.DataFrame({
                'count': [0],  # Placeholder for scaling
                'hour': [current_time.hour],
                'minute': [current_time.minute],
                'day_of_week': [current_time.weekday()],
                'is_weekend': [current_time.weekday() >= 5]
            })
            
            # Scale features using saved scaler
            scaled_features = self.scalers[location].transform(features)
            
            # Make prediction
            prediction = self.models[location].predict(
                np.array([scaled_features] * self.sequence_length).reshape(1, self.sequence_length, -1),
                verbose=0
            )
            
            # Get predicted number of swipes for next 15-minute interval
            predicted_swipes = int(max(0, self.scalers[location].inverse_transform(
                np.hstack((prediction, scaled_features[0, 1:].reshape(1, -1)))
            )[0, 0]))
            
            # Calculate swipes per minute
            swipes_per_minute = predicted_swipes / 15
            
            # Calculate wait time based on traffic level
            if swipes_per_minute > 2.67:  # >40 swipes per 15 min (high traffic)
                wait_time = (predicted_swipes * 10) / 60  # 10 seconds per swipe
                busyness_level = 'High'
            elif swipes_per_minute > 1.33:  # 20-40 swipes per 15 min (medium traffic)
                wait_time = (predicted_swipes * 7) / 60  # 7 seconds per swipe
                busyness_level = 'Medium'
            else:  # <20 swipes per 15 min (low traffic)
                wait_time = (predicted_swipes * 5) / 60  # 5 seconds per swipe
                busyness_level = 'Low'
            
            # Add small random variation (±10%) to make predictions more realistic
            variation = np.random.uniform(0.9, 1.1)
            wait_time = round(wait_time * variation, 1)
            
            # Cap maximum wait at 15 minutes
            wait_time = min(wait_time, 15)
            
            # Log prediction details
            logger.info(
                f"Prediction for {location}:\n"
                f"Time: {current_time.strftime('%H:%M')}\n"
                f"Predicted swipes/15min: {predicted_swipes}\n"
                f"Swipes per minute: {swipes_per_minute:.2f}\n"
                f"Wait time: {wait_time} minutes\n"
                f"Traffic level: {busyness_level}"
            )
            
            # Return prediction data
            return {
                'predicted_count': predicted_swipes,  # Number of swipes in next 15 min
                'wait_time_minutes': wait_time,
                'swipes_per_minute': round(swipes_per_minute, 2),
                'busyness_level': busyness_level,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error predicting for {location}: {str(e)}")
            return None
        
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get the directory containing this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # Initialize predictor with paths relative to the script location
        predictor = DiningHallPredictor(
            model_dir=os.path.join(base_dir, 'models'),
            data_dir=os.path.join(base_dir, 'data')
        )
        
        # Check if we have saved models
        if not any(predictor.models):
            logger.info("No saved models found, training new models...")
            df = predictor.load_data('October-*.csv')
            predictor.train_models(df, save=True)
        
        # Make a test prediction
        current_time = datetime.now()
        for hall in predictor.dining_halls:
            prediction = predictor.predict_wait_times(current_time, hall)
            if prediction:
                logger.info(f"Test prediction for {hall}: {prediction}")
            else:
                logger.error(f"Could not generate prediction for {hall}")
                
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
