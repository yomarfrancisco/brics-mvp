import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import plotly.graph_objects as go
import plotly.express as px

class AdvancedRiskAnalytics:
    """Advanced risk analytics and modeling for $BRICS portfolio"""
    
    def __init__(self):
        self.correlation_matrix = None
        self.var_calculations = {}
        self.stress_scenarios = {}
        
    def calculate_correlations(self, company_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate correlation matrix between obligors"""
        # Create correlation matrix based on industry, credit rating, and exposure
        companies = company_df['company'].tolist()
        n_companies = len(companies)
        
        # Initialize correlation matrix
        corr_matrix = pd.DataFrame(index=companies, columns=companies)
        
        for i, company1 in enumerate(companies):
            for j, company2 in enumerate(companies):
                if i == j:
                    corr_matrix.loc[company1, company2] = 1.0
                else:
                    # Calculate correlation based on industry similarity and credit rating
                    industry1 = company_df[company_df['company'] == company1]['industry'].iloc[0]
                    industry2 = company_df[company_df['company'] == company2]['industry'].iloc[0]
                    rating1 = company_df[company_df['company'] == company1]['credit_rating'].iloc[0]
                    rating2 = company_df[company_df['company'] == company2]['credit_rating'].iloc[0]
                    
                    # Base correlation on industry similarity
                    if industry1 == industry2:
                        base_corr = random.uniform(0.3, 0.6)
                    else:
                        base_corr = random.uniform(0.1, 0.3)
                    
                    # Adjust for credit rating similarity
                    if rating1 == rating2:
                        base_corr += random.uniform(0.1, 0.2)
                    
                    corr_matrix.loc[company1, company2] = min(0.95, base_corr)
        
        self.correlation_matrix = corr_matrix
        return corr_matrix
    
    def calculate_var(self, company_df: pd.DataFrame, confidence_level: float = 0.95, time_horizon: int = 30) -> Dict:
        """Calculate Value at Risk for the portfolio"""
        # Calculate portfolio-level VaR
        total_exposure = company_df['total_exposure'].sum()
        weighted_pd = (company_df['avg_pd'] * company_df['total_exposure']).sum() / total_exposure
        
        # Simulate portfolio value changes
        num_simulations = 10000
        portfolio_changes = []
        
        for _ in range(num_simulations):
            # Simulate default events
            defaults = np.random.binomial(1, weighted_pd, len(company_df))
            loss = (company_df['total_exposure'] * defaults).sum()
            portfolio_changes.append(-loss)  # Negative for loss
        
        # Calculate VaR
        var_percentile = (1 - confidence_level) * 100
        var_value = np.percentile(portfolio_changes, var_percentile)
        
        # Calculate Expected Shortfall (Conditional VaR)
        tail_losses = [x for x in portfolio_changes if x <= var_value]
        expected_shortfall = np.mean(tail_losses) if tail_losses else var_value
        
        self.var_calculations = {
            'var_95': var_value,
            'expected_shortfall': expected_shortfall,
            'confidence_level': confidence_level,
            'time_horizon': time_horizon,
            'total_exposure': total_exposure,
            'weighted_pd': weighted_pd
        }
        
        return self.var_calculations
    
    def stress_test_scenarios(self, company_df: pd.DataFrame) -> Dict:
        """Run stress testing scenarios"""
        scenarios = {
            'severe_recession': {
                'description': 'Severe economic recession with 3x default rates',
                'pd_multiplier': 3.0,
                'recovery_rate': 0.3,
                'correlation_increase': 0.2
            },
            'industry_crisis': {
                'description': 'Automotive industry crisis (Ford, BMW, VW, Tata)',
                'pd_multiplier': 2.5,
                'recovery_rate': 0.4,
                'affected_industries': ['Automotive']
            },
            'sovereign_crisis': {
                'description': 'South African sovereign crisis affecting all obligors',
                'pd_multiplier': 2.0,
                'recovery_rate': 0.5,
                'correlation_increase': 0.3
            },
            'liquidity_crisis': {
                'description': 'Liquidity crisis with 50% recovery rate reduction',
                'pd_multiplier': 1.5,
                'recovery_rate': 0.25,
                'correlation_increase': 0.1
            }
        }
        
        stress_results = {}
        base_exposure = company_df['total_exposure'].sum()
        
        for scenario_name, scenario_params in scenarios.items():
            # Calculate stressed PDs
            stressed_pds = company_df['avg_pd'].copy()
            
            if 'affected_industries' in scenario_params:
                # Apply stress only to specific industries
                for industry in scenario_params['affected_industries']:
                    mask = company_df['industry'] == industry
                    stressed_pds[mask] *= scenario_params['pd_multiplier']
            else:
                # Apply stress to all obligors
                stressed_pds *= scenario_params['pd_multiplier']
            
            # Calculate expected losses
            expected_loss = (stressed_pds * company_df['total_exposure']).sum()
            recovery_amount = expected_loss * scenario_params['recovery_rate']
            net_loss = expected_loss - recovery_amount
            
            stress_results[scenario_name] = {
                'scenario': scenario_params['description'],
                'expected_loss': expected_loss,
                'recovery_amount': recovery_amount,
                'net_loss': net_loss,
                'loss_percentage': (net_loss / base_exposure) * 100,
                'stressed_pds': stressed_pds.tolist()
            }
        
        self.stress_scenarios = stress_results
        return stress_results
    
    def create_risk_heatmap(self, company_df: pd.DataFrame) -> go.Figure:
        """Create risk heatmap visualization"""
        # Create risk matrix based on PD and exposure
        risk_matrix = company_df[['company', 'avg_pd', 'total_exposure', 'industry']].copy()
        risk_matrix['risk_score'] = risk_matrix['avg_pd'] * (risk_matrix['total_exposure'] / risk_matrix['total_exposure'].sum())
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=risk_matrix['risk_score'].values.reshape(1, -1),
            x=risk_matrix['company'].values,
            y=['Risk Score'],
            colorscale='Reds',
            showscale=True,
            text=risk_matrix['risk_score'].round(4).values.reshape(1, -1),
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Portfolio Risk Heatmap",
            xaxis_title="Obligors",
            yaxis_title="Risk Metrics",
            height=300
        )
        
        return fig
    
    def calculate_concentration_risk(self, company_df: pd.DataFrame) -> Dict:
        """Calculate concentration risk metrics"""
        total_exposure = company_df['total_exposure'].sum()
        
        # Industry concentration
        industry_concentration = company_df.groupby('industry')['total_exposure'].sum() / total_exposure
        
        # Credit rating concentration
        rating_concentration = company_df.groupby('credit_rating')['total_exposure'].sum() / total_exposure
        
        # Top 5 obligor concentration
        top_5_concentration = company_df.nlargest(5, 'total_exposure')['total_exposure'].sum() / total_exposure
        
        # Herfindahl-Hirschman Index (HHI) for concentration
        exposure_shares = company_df['total_exposure'] / total_exposure
        hhi = (exposure_shares ** 2).sum()
        
        return {
            'industry_concentration': industry_concentration.to_dict(),
            'rating_concentration': rating_concentration.to_dict(),
            'top_5_concentration': top_5_concentration,
            'hhi': hhi,
            'concentration_risk_level': 'high' if hhi > 0.25 else 'medium' if hhi > 0.15 else 'low'
        }
    
    def generate_risk_report(self, company_df: pd.DataFrame) -> Dict:
        """Generate comprehensive risk report"""
        # Calculate all risk metrics
        correlations = self.calculate_correlations(company_df)
        var_results = self.calculate_var(company_df)
        stress_results = self.stress_test_scenarios(company_df)
        concentration_risk = self.calculate_concentration_risk(company_df)
        
        # Portfolio statistics
        portfolio_stats = {
            'total_exposure': company_df['total_exposure'].sum(),
            'number_of_obligors': len(company_df),
            'average_pd': company_df['avg_pd'].mean(),
            'weighted_pd': (company_df['avg_pd'] * company_df['total_exposure']).sum() / company_df['total_exposure'].sum(),
            'exposure_range': {
                'min': company_df['total_exposure'].min(),
                'max': company_df['total_exposure'].max(),
                'median': company_df['total_exposure'].median()
            }
        }
        
        return {
            'portfolio_stats': portfolio_stats,
            'correlation_matrix': correlations,
            'var_analysis': var_results,
            'stress_testing': stress_results,
            'concentration_risk': concentration_risk,
            'risk_summary': {
                'overall_risk_level': 'medium',
                'key_risks': [
                    'Industry concentration in Automotive sector',
                    'Geographic concentration in BRICS region',
                    'Credit rating distribution favors investment grade'
                ],
                'risk_mitigants': [
                    'Sovereign guarantee protection',
                    'Overcollateralization buffer',
                    'Diversified industry exposure'
                ]
            }
        }

class PortfolioOptimizer:
    """Portfolio optimization and rebalancing tools"""
    
    def __init__(self):
        self.optimization_history = []
    
    def optimize_portfolio(self, company_df: pd.DataFrame, target_metrics: Dict) -> Dict:
        """Optimize portfolio based on target metrics"""
        # Simulate portfolio optimization
        current_exposure = company_df['total_exposure'].sum()
        target_exposure = target_metrics.get('target_exposure', current_exposure)
        target_pd = target_metrics.get('target_pd', company_df['avg_pd'].mean())
        
        # Calculate optimal weights (simplified)
        optimal_weights = company_df['total_exposure'] / current_exposure
        
        # Adjust for target metrics
        pd_adjustments = (target_pd - company_df['avg_pd'].mean()) * 0.1
        optimal_weights = optimal_weights * (1 + pd_adjustments)
        optimal_weights = optimal_weights / optimal_weights.sum()  # Normalize
        
        # Calculate new exposures
        new_exposures = optimal_weights * target_exposure
        
        optimization_result = {
            'current_exposure': current_exposure,
            'target_exposure': target_exposure,
            'new_exposures': new_exposures.to_dict(),
            'exposure_changes': (new_exposures - company_df['total_exposure']).to_dict(),
            'target_metrics': target_metrics
        }
        
        self.optimization_history.append({
            'timestamp': datetime.now(),
            'result': optimization_result
        })
        
        return optimization_result

# Initialize global instances
risk_analytics = AdvancedRiskAnalytics()
portfolio_optimizer = PortfolioOptimizer() 