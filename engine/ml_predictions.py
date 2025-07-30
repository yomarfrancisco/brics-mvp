import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Tuple
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

class MLPredictor:
    """Advanced ML predictions for credit risk and yield forecasting"""
    
    def __init__(self):
        self.models = {}
        self.model_metrics = {}
        self.prediction_history = []
        self.feature_importance = {}
        
        # Model configurations
        self.model_configs = {
            'credit_risk': {
                'model_type': 'RandomForestRegressor',
                'features': ['avg_pd', 'total_exposure', 'yield', 'spread_bps', 'time_listed_days'],
                'target': 'xgboost_pd',
                'update_frequency': 24  # hours
            },
            'yield_forecast': {
                'model_type': 'RandomForestRegressor', 
                'features': ['cds_spread', 'sovereign_yield', 'currency_rate', 'market_stress'],
                'target': 'predicted_yield',
                'update_frequency': 12  # hours
            },
            'default_probability': {
                'model_type': 'RandomForestRegressor',
                'features': ['credit_rating_score', 'industry_risk', 'geographic_risk', 'tenor_risk'],
                'target': 'default_prob',
                'update_frequency': 6  # hours
            }
        }
    
    def prepare_features(self, company_df: pd.DataFrame, protocol_df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for ML models"""
        features_df = company_df.copy()
        
        # Add derived features
        features_df['time_listed_days'] = features_df['time_listed'].str.extract('(\d+)').astype(float)
        features_df['credit_rating_score'] = features_df['credit_rating'].map({
            'A+': 1.0, 'A': 0.9, 'A-': 0.8, 'BBB+': 0.7, 'BBB': 0.6, 'BB+': 0.5, 'BB': 0.4
        })
        features_df['industry_risk'] = features_df['industry'].map({
            'Technology': 0.3, 'Automotive': 0.6, 'Manufacturing': 0.5, 'Retail': 0.4, 'Energy': 0.7
        })
        features_df['geographic_risk'] = 0.5  # Base risk for BRICS region
        features_df['tenor_risk'] = features_df['terms_tenor'].str.extract('(\d+)').astype(float) / 365
        
        # Add protocol-level features
        protocol_features = {}
        for _, row in protocol_df.iterrows():
            protocol_features[row['metric']] = row['value']
        
        for col in features_df.columns:
            if col not in ['company', 'industry', 'credit_rating', 'terms_tenor', 'time_listed']:
                features_df[f'{col}_normalized'] = (features_df[col] - features_df[col].mean()) / features_df[col].std()
        
        return features_df
    
    def train_credit_risk_model(self, company_df: pd.DataFrame, risk_df: pd.DataFrame) -> Dict:
        """Train credit risk prediction model"""
        features_df = self.prepare_features(company_df, risk_df)
        
        # Merge with risk data
        model_data = features_df.merge(risk_df[['company', 'xgboost_pd']], on='company')
        
        # Prepare features and target
        feature_cols = self.model_configs['credit_risk']['features']
        X = model_data[feature_cols].fillna(0)
        y = model_data['xgboost_pd']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Store model and metrics
        self.models['credit_risk'] = model
        self.model_metrics['credit_risk'] = {
            'mse': mse,
            'r2': r2,
            'feature_importance': dict(zip(feature_cols, model.feature_importances_))
        }
        
        return {
            'model_trained': True,
            'mse': mse,
            'r2': r2,
            'feature_importance': self.model_metrics['credit_risk']['feature_importance']
        }
    
    def predict_credit_risk(self, company_data: Dict) -> Dict:
        """Predict credit risk for a company"""
        if 'credit_risk' not in self.models:
            return {'error': 'Model not trained'}
        
        model = self.models['credit_risk']
        features = []
        
        # Prepare features in same order as training
        feature_cols = self.model_configs['credit_risk']['features']
        for col in feature_cols:
            if col in company_data:
                features.append(company_data[col])
            else:
                features.append(0)  # Default value
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        # Calculate confidence interval (simplified)
        confidence = 0.95 - (prediction * 0.3)  # Higher risk = lower confidence
        
        return {
            'predicted_pd': prediction,
            'confidence': max(0.5, confidence),
            'risk_level': 'High' if prediction > 0.05 else 'Medium' if prediction > 0.02 else 'Low'
        }
    
    def train_yield_forecast_model(self, historical_data: pd.DataFrame) -> Dict:
        """Train yield forecasting model"""
        # Simulate historical yield data
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
        yield_data = []
        
        for date in dates:
            base_yield = 0.30  # 30% base APY
            market_stress = np.random.normal(0, 0.05)  # Market volatility
            seasonal_factor = 0.02 * np.sin(2 * np.pi * date.dayofyear / 365)  # Seasonal pattern
            
            yield_data.append({
                'date': date,
                'cds_spread': np.random.uniform(100, 200),
                'sovereign_yield': np.random.uniform(0.05, 0.08),
                'currency_rate': np.random.uniform(15, 18),
                'market_stress': market_stress,
                'actual_yield': base_yield + market_stress + seasonal_factor
            })
        
        yield_df = pd.DataFrame(yield_data)
        
        # Prepare features
        feature_cols = self.model_configs['yield_forecast']['features']
        X = yield_df[feature_cols]
        y = yield_df['actual_yield']
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # Evaluate
        y_pred = model.predict(X)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        self.models['yield_forecast'] = model
        self.model_metrics['yield_forecast'] = {
            'mse': mse,
            'r2': r2,
            'feature_importance': dict(zip(feature_cols, model.feature_importances_))
        }
        
        return {
            'model_trained': True,
            'mse': mse,
            'r2': r2,
            'historical_data': yield_df
        }
    
    def forecast_yield(self, days_ahead: int = 30) -> Dict:
        """Forecast yield for next N days"""
        if 'yield_forecast' not in self.models:
            return {'error': 'Model not trained'}
        
        model = self.models['yield_forecast']
        forecasts = []
        
        # Generate future feature values
        for day in range(days_ahead):
            future_date = datetime.now() + timedelta(days=day)
            
            # Simulate future market conditions
            features = {
                'cds_spread': np.random.uniform(100, 200),
                'sovereign_yield': np.random.uniform(0.05, 0.08),
                'currency_rate': np.random.uniform(15, 18),
                'market_stress': np.random.normal(0, 0.05)
            }
            
            # Make prediction
            prediction = model.predict([list(features.values())])[0]
            
            forecasts.append({
                'date': future_date,
                'predicted_yield': prediction,
                'confidence': 0.9 - (day * 0.01)  # Decreasing confidence over time
            })
        
        return {
            'forecasts': forecasts,
            'avg_forecast': np.mean([f['predicted_yield'] for f in forecasts]),
            'forecast_range': (min([f['predicted_yield'] for f in forecasts]), 
                             max([f['predicted_yield'] for f in forecasts]))
        }
    
    def backtest_portfolio(self, company_df: pd.DataFrame, historical_period: int = 90) -> Dict:
        """Backtest portfolio performance over historical period"""
        # Simulate historical portfolio data
        dates = pd.date_range(start=datetime.now() - timedelta(days=historical_period), 
                            end=datetime.now(), freq='D')
        
        backtest_results = []
        initial_value = 1000000  # $1M initial investment
        current_value = initial_value
        
        for date in dates:
            # Simulate daily returns
            daily_return = np.random.normal(0.001, 0.005)  # 0.1% daily return with volatility
            current_value *= (1 + daily_return)
            
            # Simulate some defaults
            if np.random.random() < 0.001:  # 0.1% daily default probability
                default_loss = np.random.uniform(0.02, 0.05)  # 2-5% loss on default
                current_value *= (1 - default_loss)
            
            backtest_results.append({
                'date': date,
                'portfolio_value': current_value,
                'daily_return': daily_return,
                'cumulative_return': (current_value - initial_value) / initial_value
            })
        
        backtest_df = pd.DataFrame(backtest_results)
        
        # Calculate performance metrics
        total_return = (current_value - initial_value) / initial_value
        volatility = backtest_df['daily_return'].std() * np.sqrt(252)  # Annualized
        sharpe_ratio = (backtest_df['daily_return'].mean() * 252) / volatility if volatility > 0 else 0
        max_drawdown = (backtest_df['portfolio_value'] / backtest_df['portfolio_value'].cummax() - 1).min()
        
        return {
            'total_return': total_return,
            'annualized_return': total_return * (365 / historical_period),
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'historical_data': backtest_df
        }
    
    def generate_ml_report(self, company_df: pd.DataFrame, protocol_df: pd.DataFrame) -> Dict:
        """Generate comprehensive ML analytics report"""
        # Train models
        risk_df = pd.read_csv('data/mock_risk_outputs.csv')
        credit_risk_result = self.train_credit_risk_model(company_df, risk_df)
        yield_forecast_result = self.train_yield_forecast_model(pd.DataFrame())
        
        # Generate predictions
        yield_forecast = self.forecast_yield(30)
        backtest_result = self.backtest_portfolio(company_df, 90)
        
        # Model performance summary
        model_performance = {}
        for model_name, metrics in self.model_metrics.items():
            model_performance[model_name] = {
                'r2_score': metrics['r2'],
                'mse': metrics['mse'],
                'feature_importance': metrics['feature_importance']
            }
        
        return {
            'model_performance': model_performance,
            'yield_forecast': yield_forecast,
            'backtest_results': backtest_result,
            'credit_risk_analysis': credit_risk_result,
            'report_date': datetime.now().isoformat()
        }

class RealTimeModelUpdater:
    """Manages real-time model updates and performance monitoring"""
    
    def __init__(self):
        self.update_schedule = {}
        self.model_versions = {}
        self.performance_tracking = {}
    
    def schedule_model_update(self, model_name: str, frequency_hours: int):
        """Schedule regular model updates"""
        self.update_schedule[model_name] = {
            'frequency_hours': frequency_hours,
            'last_update': datetime.now(),
            'next_update': datetime.now() + timedelta(hours=frequency_hours)
        }
    
    def check_for_updates(self) -> List[str]:
        """Check which models need updating"""
        models_to_update = []
        
        for model_name, schedule in self.update_schedule.items():
            if datetime.now() >= schedule['next_update']:
                models_to_update.append(model_name)
        
        return models_to_update
    
    def update_model_performance(self, model_name: str, new_metrics: Dict):
        """Track model performance over time"""
        if model_name not in self.performance_tracking:
            self.performance_tracking[model_name] = []
        
        self.performance_tracking[model_name].append({
            'timestamp': datetime.now(),
            'metrics': new_metrics
        })
    
    def get_model_health_report(self) -> Dict:
        """Generate model health report"""
        health_report = {
            'total_models': len(self.update_schedule),
            'models_needing_update': len(self.check_for_updates()),
            'model_performance': {}
        }
        
        for model_name in self.update_schedule.keys():
            if model_name in self.performance_tracking:
                recent_metrics = self.performance_tracking[model_name][-1]['metrics']
                health_report['model_performance'][model_name] = {
                    'r2_score': recent_metrics.get('r2', 0),
                    'last_update': self.update_schedule[model_name]['last_update'].isoformat(),
                    'next_update': self.update_schedule[model_name]['next_update'].isoformat()
                }
        
        return health_report

# Initialize global instances
ml_predictor = MLPredictor()
model_updater = RealTimeModelUpdater() 