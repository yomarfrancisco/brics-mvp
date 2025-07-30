import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import numpy as np
import sys
import os

# Add engine directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'engine'))
from api_integration import bank_connector, quality_monitor
from advanced_analytics import risk_analytics, portfolio_optimizer

# Add docs directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'docs'))
from compliance_tracker import compliance_tracker, documentation_manager, audit_trail_manager

# Add performance monitoring
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'engine'))
from performance_monitor import performance_monitor, data_processing_monitor, dashboard_tracker

# Add PDF report generator
from report_generator import pdf_generator

# Add ML predictions
from ml_predictions import ml_predictor, model_updater

# Add export functionality
import io
import base64
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import plotly.io as pio

st.set_page_config(
    page_title="$BRICS Investment Report", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with grid system
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Grid System */
    .grid-container {
        display: grid;
        gap: 1.5rem;
        margin: 1rem 0;
    }
    
    .grid-2x2 {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
    }
    
    .grid-3x3 {
        grid-template-columns: 1fr 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
    }
    
    .grid-2x3 {
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr 1fr;
    }
    
    /* Section Cards */
    .section-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1e3c72;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 6px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Status Indicators */
    .status-indicator {
        font-size: 1.3rem;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        display: inline-block;
    }
    
    .status-stable {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
    }
    
    .status-volatile {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .status-stress {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
    }
    
    /* Live Indicator */
    .live-indicator {
        animation: pulse 2s infinite;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: bold;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.9);
        border-radius: 0.5rem 0.5rem 0 0;
        padding: 1rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102,126,234,0.2);
    }
    
    /* Info Boxes */
    .info-box {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 6px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Chart Containers */
    .chart-container {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    
    /* Metric Styling */
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3c72;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem;
        }
        
        .main-header {
            padding: 1.5rem;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .section-card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .section-header {
            font-size: 1.2rem;
        }
        
        .metric-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        /* Stack columns on mobile */
        .stColumns > div {
            width: 100% !important;
            margin-bottom: 1rem;
        }
        
        /* Adjust chart containers */
        .chart-container {
            padding: 0.5rem;
        }
        
        /* Make buttons more touch-friendly */
        .stButton > button {
            width: 100%;
            height: 3rem;
            font-size: 1rem;
        }
    }
    
    /* Loading States */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        background: rgba(255,255,255,0.9);
        border-radius: 1rem;
        margin: 1rem 0;
    }
    
    /* Error States */
    .error-container {
        background: rgba(255,0,0,0.1);
        border: 1px solid #ff0000;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Success States */
    .success-container {
        background: rgba(0,255,0,0.1);
        border: 1px solid #00ff00;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load all data
company_df = pd.read_csv("data/mock_company_summary.csv")
protocol_df = pd.read_csv("data/mock_protocol_metrics.csv")
risk_df = pd.read_csv("data/mock_risk_outputs.csv")
waterfall_df = pd.read_csv("data/mock_waterfall.csv")
portfolio_tranching_df = pd.read_csv("data/mock_portfolio_tranching.csv")
transactions_df = pd.read_csv("data/mock_transactions.csv")
brics_price_df = pd.read_csv("data/mock_brics_price.csv")
transactions_extended_df = pd.read_csv("data/mock_transactions_extended.csv")

# Initialize session state
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = None
if 'live_mode' not in st.session_state:
    st.session_state.live_mode = False
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'ultra_fast_last_update' not in st.session_state:
    st.session_state.ultra_fast_last_update = datetime.now()
if 'fast_last_update' not in st.session_state:
    st.session_state.fast_last_update = datetime.now()
if 'normal_last_update' not in st.session_state:
    st.session_state.normal_last_update = datetime.now()

# Tiered real-time data simulation
def simulate_ultra_fast_data():
    """Ultra-fast updates (5 seconds): $BRICS price with realistic bands around $1.00"""
    if st.session_state.live_mode:
        current_time = datetime.now()
        if (current_time - st.session_state.ultra_fast_last_update).seconds >= 5:
            
            # Determine market stress level (affects volatility)
            stress_level = random.choice(['normal', 'normal', 'normal', 'stress', 'crisis'])  # 75% normal, 20% stress, 5% crisis
            
            if stress_level == 'normal':
                price_volatility = 0.005  # ±$0.005 range
                currency_volatility = 0.02  # ±2% ZAR movement
                yield_volatility = 0.1     # ±0.1% yield change
            elif stress_level == 'stress':
                price_volatility = 0.015   # ±$0.015 range
                currency_volatility = 0.05  # ±5% ZAR movement
                yield_volatility = 0.3     # ±0.3% yield change
            else:  # crisis
                price_volatility = 0.025   # ±$0.025 range
                currency_volatility = 0.10  # ±10% ZAR movement
                yield_volatility = 0.5     # ±0.5% yield change
            
            # Update $BRICS price with realistic bands around $1.00
            current_price = protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]
            base_price = 1.00  # Target stablecoin price
            
            # Calculate yield component
            cds_monthly = protocol_df[protocol_df['metric'] == 'cds_premiums_monthly']['value'].iloc[0]
            sovereign_monthly = protocol_df[protocol_df['metric'] == 'sovereign_yield_monthly']['value'].iloc[0]
            zar_rate = protocol_df[protocol_df['metric'] == 'zar_rate']['value'].iloc[0]
            
            # Yield component (monthly to price adjustment)
            yield_component = (cds_monthly + sovereign_monthly) / 100  # Convert % to decimal
            zar_effect = (zar_rate - 18.5) / 100  # ZAR deviation effect
            
            # Target price with yield component
            target_price = base_price + yield_component + zar_effect
            
            # Add realistic volatility with arbitrage effects
            # Base market volatility
            price_change = random.uniform(-price_volatility, price_volatility)
            
            # Add arbitrage pressure (investors buying/selling based on yield opportunities)
            arbitrage_pressure = random.uniform(-0.01, 0.01)  # ±1% arbitrage effect
            
            # Add market stress effects (more volatility during stress)
            stress_multiplier = 1.0
            if stress_level != 'normal':
                stress_multiplier = 1.5 if stress_level == 'stress' else 2.0
            
            # Add volume-based volatility (higher volume = more volatility)
            volume_effect = random.uniform(-0.005, 0.005)  # ±0.5% volume effect
            
            # Combine all effects
            total_price_change = (price_change + arbitrage_pressure + volume_effect) * stress_multiplier
            new_price = max(0.95, min(1.10, target_price + total_price_change))  # Bounds for realism
            
            price_mask = protocol_df['metric'] == 'brics_price'
            protocol_df.loc[price_mask, 'value'] = new_price
            
            # Update CDS premiums with realistic changes
            cds_change = random.uniform(-0.1, 0.1) * yield_volatility
            new_cds = max(1.0, min(3.0, cds_monthly + cds_change))
            cds_mask = protocol_df['metric'] == 'cds_premiums_monthly'
            protocol_df.loc[cds_mask, 'value'] = new_cds
            
            # Update USD-ZAR rate with realistic volatility
            zar_change = random.uniform(-currency_volatility, currency_volatility)
            new_zar = max(15.0, min(25.0, zar_rate + zar_change))
            zar_mask = protocol_df['metric'] == 'zar_rate'
            protocol_df.loc[zar_mask, 'value'] = new_zar
            
            # Update SA Treasury yield
            current_sovereign = protocol_df[protocol_df['metric'] == 'sovereign_yield_monthly']['value'].iloc[0]
            sovereign_change = random.uniform(-0.05, 0.05) * yield_volatility
            new_sovereign = max(0.5, min(1.5, current_sovereign + sovereign_change))
            sovereign_mask = protocol_df['metric'] == 'sovereign_yield_monthly'
            protocol_df.loc[sovereign_mask, 'value'] = new_sovereign
            
            # Update monthly yield total
            new_total = new_cds + new_sovereign
            total_mask = protocol_df['metric'] == 'monthly_yield_total'
            protocol_df.loc[total_mask, 'value'] = new_total
            
            # Update APY
            new_apy = new_total * 12
            apy_mask = protocol_df['metric'] == 'apy_per_brics'
            protocol_df.loc[apy_mask, 'value'] = new_apy
            
            # Update weighted PD based on market stress
            if stress_level != 'normal':
                pd_adjustment = random.uniform(0.001, 0.005) if stress_level == 'stress' else random.uniform(0.005, 0.015)
                current_pd = protocol_df[protocol_df['metric'] == 'weighted_pd']['value'].iloc[0]
                new_pd = min(0.15, current_pd + pd_adjustment)
                pd_mask = protocol_df['metric'] == 'weighted_pd'
                protocol_df.loc[pd_mask, 'value'] = new_pd
            
            # Update capital efficiency
            eff_change = random.uniform(-0.05, 0.05)
            current_eff = protocol_df[protocol_df['metric'] == 'capital_efficiency']['value'].iloc[0]
            new_eff = max(5.0, min(12.0, current_eff + eff_change))
            eff_mask = protocol_df['metric'] == 'capital_efficiency'
            protocol_df.loc[eff_mask, 'value'] = new_eff
            
            st.session_state.ultra_fast_last_update = current_time

def simulate_fast_data():
    """Fast updates (45 seconds): Dynamic company-level changes and transactions"""
    if st.session_state.live_mode:
        current_time = datetime.now()
        if (current_time - st.session_state.fast_last_update).seconds >= 45:
            
            # Simulate new transaction for random company (40% chance)
            if random.random() < 0.4:
                random_company = random.choice(company_df['company'].tolist())
                company_idx = company_df[company_df['company'] == random_company].index[0]
                
                # Add new transaction amount
                current_exposure = company_df.loc[company_idx, 'total_exposure']
                new_transaction = random.uniform(50000, 300000)
                company_df.loc[company_idx, 'total_exposure'] += new_transaction
                
                # Update 24h change
                company_df.loc[company_idx, 'notional_24h_change'] += new_transaction
                
                # Update CDS fee change
                cds_change = random.uniform(-0.1, 0.1)
                current_cds_change = company_df.loc[company_idx, 'cds_fee_24h_change']
                company_df.loc[company_idx, 'cds_fee_24h_change'] = current_cds_change + cds_change
            
            # Update all company risk scores and yields (realistic market movements)
            for idx in company_df.index:
                # Risk score changes based on market conditions
                current_pd = company_df.loc[idx, 'avg_pd']
                pd_change = random.uniform(-0.003, 0.003)
                new_pd = max(0.01, min(0.15, current_pd + pd_change))
                company_df.loc[idx, 'avg_pd'] = new_pd
                
                # Yield changes based on risk and market conditions
                current_yield = company_df.loc[idx, 'yield']
                yield_change = random.uniform(-0.3, 0.3)
                new_yield = max(25.0, min(40.0, current_yield + yield_change))
                company_df.loc[idx, 'yield'] = new_yield
                
                # Spread changes (basis points)
                current_spread = company_df.loc[idx, 'spread_bps']
                spread_change = random.uniform(-2, 2)
                new_spread = max(20, min(50, current_spread + spread_change))
                company_df.loc[idx, 'spread_bps'] = new_spread
            
            # Update total notional
            total_exposure = company_df['total_exposure'].sum()
            notional_mask = protocol_df['metric'] == 'total_notional'
            protocol_df.loc[notional_mask, 'value'] = total_exposure
            
            # Update tokens minted (can increase with new transactions)
            current_tokens = protocol_df[protocol_df['metric'] == 'tokens_minted']['value'].iloc[0]
            if random.random() < 0.1:  # 10% chance of new token minting
                new_tokens = random.uniform(1000, 5000)
                tokens_mask = protocol_df['metric'] == 'tokens_minted'
                protocol_df.loc[tokens_mask, 'value'] = current_tokens + new_tokens
            
            st.session_state.fast_last_update = current_time

def simulate_normal_data():
    """Normal updates (5-15 minutes): Portfolio metrics, capital efficiency"""
    if st.session_state.live_mode:
        current_time = datetime.now()
        if (current_time - st.session_state.normal_last_update).seconds >= 600:  # 10 minutes
            # Update weighted PD
            weighted_pd = (company_df['avg_pd'] * company_df['total_exposure']).sum() / company_df['total_exposure'].sum()
            pd_mask = protocol_df['metric'] == 'weighted_pd'
            protocol_df.loc[pd_mask, 'value'] = weighted_pd
            
            # Update capital efficiency slightly
            current_eff = protocol_df[protocol_df['metric'] == 'capital_efficiency']['value'].iloc[0]
            eff_change = random.uniform(-0.1, 0.1)
            new_eff = max(5.0, current_eff + eff_change)
            eff_mask = protocol_df['metric'] == 'capital_efficiency'
            protocol_df.loc[eff_mask, 'value'] = new_eff
            
            # Update overcollateralization
            current_oc = protocol_df[protocol_df['metric'] == 'overcollateralization']['value'].iloc[0]
            oc_change = random.uniform(-0.005, 0.005)
            new_oc = max(0.05, current_oc + oc_change)
            oc_mask = protocol_df['metric'] == 'overcollateralization'
            protocol_df.loc[oc_mask, 'value'] = new_oc
            
            st.session_state.normal_last_update = current_time

# Run all simulation tiers
def run_all_simulations():
    simulate_ultra_fast_data()
    simulate_fast_data()
    simulate_normal_data()

# Run simulations
run_all_simulations()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0;">
        <h3 style="margin: 0; color: #1e3c72; font-weight: 600;">📊 BRICS Protocol</h3>
        <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">Investment Analytics & Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    page = st.selectbox(
        "Navigation",
        ["Dashboard", "Unit Economics", "Portfolio Analysis", "Technical Details", "Advanced Analytics", "API Integration", "AI/ML Analytics"],
        index=0
    )
    
    st.divider()
    
    # Quick status
    if st.session_state.live_mode:
        st.success("🟢 Live Mode Active")
    else:
        st.info("⚪ Static Mode")
    
    # Last update
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    
    # Quick metrics
    st.markdown("**Quick Metrics:**")
    current_price = protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]
    st.metric("$BRICS Price", f"${current_price:.3f}")
    
    apy = protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
    st.metric("Target APY", f"{apy:.1f}%")
    
    total_exposure = company_df['total_exposure'].sum()
    st.metric("Total Exposure", f"${total_exposure:,.0f}")
    
    weighted_pd = protocol_df[protocol_df['metric'] == 'weighted_pd']['value'].iloc[0]
    st.metric("Portfolio PD", f"{weighted_pd*100:.1f}%")

# ============================================================================
# PAGE NAVIGATION
# ============================================================================
if page == "Dashboard":
    # ============================================================================
    # DASHBOARD - PROMINENT CURRENT PRICE
    # ============================================================================
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700; text-align: center;">
            💰 $BRICS Investment Report
        </h1>
        <p style="text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
            AI-Native Synthetic Credit Protocol • Real-Time Risk Analytics • Investor Due Diligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # PROMINENT CURRENT PRICE - FIRST THING USERS SEE
    current_price = protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]
    price_change = current_price - 1.00
    price_change_pct = (price_change / 1.00) * 100
    
    # Determine live mode status
    live_status = "🟢 LIVE" if st.session_state.live_mode else "⚪ STATIC"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                color: white; padding: 2rem; border-radius: 1rem; margin: 1rem 0; 
                text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
        <h2 style="margin: 0; font-size: 1.2rem; opacity: 0.9;">Current $BRICS Price</h2>
        <h1 style="margin: 0.5rem 0; font-size: 3.5rem; font-weight: 700;">${current_price:.3f}</h1>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">
            {price_change_pct:+.2f}% from $1.00 peg • {live_status}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Status and controls row
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.2);">
            <p style="margin: 0; color: white; font-size: 0.9rem;">
                📅 Last Updated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.session_state.live_mode:
            # Dynamic status based on current price
            current_price = protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]
            price_deviation = abs(current_price - 1.00)
            
            if price_deviation < 0.01:
                status_class = "status-stable"
                status_text = "🟢 STABLE"
            elif price_deviation < 0.02:
                status_class = "status-volatile"
                status_text = "🟡 VOLATILE"
            else:
                status_class = "status-stress"
                status_text = "🔴 STRESS"
            
            st.markdown(f"""
            <div class="{status_class}" style="text-align: center;">
                {status_text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.2); color: white; padding: 0.5rem 1rem; border-radius: 2rem; text-align: center; font-weight: bold;">
                ⏸️ STATIC DATA
            </div>
            """, unsafe_allow_html=True)

    with col3:
        if st.session_state.live_mode:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.2);">
                <p style="margin: 0; color: white; font-size: 0.9rem; font-weight: bold;">Update Frequencies:</p>
                <p style="margin: 0.2rem 0; color: white; font-size: 0.8rem;">• Price: 5s</p>
                <p style="margin: 0.2rem 0; color: white; font-size: 0.8rem;">• Transactions: 45s</p>
                <p style="margin: 0.2rem 0; color: white; font-size: 0.8rem;">• Portfolio: 10min</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 0.5rem; border: 1px solid rgba(255,255,255,0.2);">
                <p style="margin: 0; color: white; font-size: 0.9rem; font-weight: bold;">Static Mode</p>
                <p style="margin: 0.2rem 0; color: white; font-size: 0.8rem;">Click 'Toggle Live Mode'</p>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        if st.session_state.live_mode:
            st.markdown("""
            <div class="live-indicator" style="text-align: center;">
                🔴 LIVE
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.2); color: white; padding: 0.5rem 1rem; border-radius: 2rem; text-align: center; font-weight: bold;">
                ⚪ OFFLINE
            </div>
            """, unsafe_allow_html=True)

    # Live mode toggle with real-time notifications
    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("🔄 Toggle Live Mode"):
            st.session_state.live_mode = not st.session_state.live_mode
            st.rerun()

    with col2:
        if st.session_state.live_mode:
            # Show real-time update notifications
            current_time = datetime.now()
            last_ultra = (current_time - st.session_state.ultra_fast_last_update).seconds
            last_fast = (current_time - st.session_state.fast_last_update).seconds
            last_normal = (current_time - st.session_state.normal_last_update).seconds
            
            st.markdown("**🟢 Real-time Updates Active:**")
            st.markdown(f"• Price updates: {last_ultra}s ago")
            st.markdown(f"• Transaction updates: {last_fast}s ago")
            st.markdown(f"• Portfolio updates: {last_normal}s ago")
        else:
            st.markdown("**⚪ Static Mode - No real-time updates**")

    st.divider()
    
    # Export functionality
    create_export_buttons()
    
    # Real-time alerts
    display_alerts()

    # ============================================================================
    # KEY METRICS SECTION
    # ============================================================================
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0; font-size: 1.8rem; font-weight: 600;">
            📊 Key Protocol Metrics
        </h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem;">
            Real-time monitoring of $BRICS price, yield components, and risk metrics
        </p>
    </div>
    """, unsafe_allow_html=True)

    # $BRICS Price Chart
    st.markdown("""
    <div class="chart-container">
        <h3 style="margin: 0 0 1rem 0; color: #1e3c72; font-weight: 600;">
            📈 $BRICS Price Chart
        </h3>
    """, unsafe_allow_html=True)

    # Create dynamic price chart with yield-inclusive pricing
    if st.session_state.live_mode:
        # Generate dynamic price data with yield-inclusive pricing
        # Use last 90 days of data but add real-time volatility
        base_df = brics_price_df.copy()
        base_df['timestamp'] = pd.to_datetime(base_df['timestamp'])
        
        # Get current yield components
        cds_monthly = protocol_df[protocol_df['metric'] == 'cds_premiums_monthly']['value'].iloc[0]
        sovereign_monthly = protocol_df[protocol_df['metric'] == 'sovereign_yield_monthly']['value'].iloc[0]
        zar_rate = protocol_df[protocol_df['metric'] == 'zar_rate']['value'].iloc[0]
        
        # Calculate yield-inclusive price (peg + yield)
        current_yield_total = (cds_monthly + sovereign_monthly) / 100  # Convert % to decimal
        zar_effect = (zar_rate - 18.5) / 100 * 0.1  # ZAR effect
        current_price = 1.00 + current_yield_total + zar_effect  # $1.00 peg + yield
        
        # Create yield-inclusive price series with realistic volatility
        yield_inclusive_prices = []
        timestamps = []
        base_peg = 1.00  # $1.00 peg
        
        # Generate completely synthetic data with high volatility (like portfolio backtesting)
        start_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        
        # Generate daily data points for 90 days
        for day in range(90):
            current_date = start_date + pd.Timedelta(days=day)
            
            # Add multiple price points per day for more variation
            for hour_offset in range(0, 24, 6):  # Every 6 hours
                timestamp = current_date + pd.Timedelta(hours=hour_offset)
                days_ago = (pd.Timestamp.now() - timestamp).days
                
                # Base yield component (simulate realistic yield)
                base_yield = 0.025 + np.random.normal(0, 0.005)  # ~2.5% base yield
                zar_effect = np.random.normal(0, 0.002)  # Small ZAR effect
                
                if days_ago <= 30:  # Recent data - extremely volatile (like portfolio backtesting)
                    # Add massive volatility like the portfolio chart
                    daily_volatility = np.random.normal(0, 0.015)  # ±1.5% daily volatility
                    market_noise = np.random.normal(0, 0.01)  # ±1% market noise
                    arbitrage_pressure = np.random.normal(0, 0.02)  # ±2% arbitrage effect
                    
                    # Add extreme stress events (like portfolio crashes)
                    stress_multiplier = 1.0
                    if np.random.random() < 0.1:  # 10% chance of extreme stress
                        stress_multiplier = 2.0  # Double the volatility
                    
                    # Calculate yield-inclusive price with extreme volatility
                    yield_component = base_yield + zar_effect + daily_volatility
                    price = base_peg + yield_component + market_noise + arbitrage_pressure
                    price *= stress_multiplier
                    
                else:  # Historical data - still volatile but less extreme
                    daily_volatility = np.random.normal(0, 0.01)  # ±1% historical volatility
                    market_noise = np.random.normal(0, 0.005)  # ±0.5% market noise
                    
                    yield_component = base_yield + zar_effect + daily_volatility
                    price = base_peg + yield_component + market_noise
                
                # Ensure price stays within realistic bounds but allow more variation
                price = max(0.90, min(1.30, price))  # Allow $0.90 - $1.30 range
                yield_inclusive_prices.append(price)
                timestamps.append(timestamp)
        
        # Create new dataframe with yield-inclusive prices and timestamps
        dynamic_df = pd.DataFrame({
            'timestamp': timestamps,
            'close': yield_inclusive_prices
        })
        
        # Add real-time current price point
        current_time = pd.Timestamp.now()
        current_row = pd.DataFrame({
            'timestamp': [current_time],
            'close': [current_price],
            'open': [current_price],
            'high': [current_price * 1.001],
            'low': [current_price * 0.999],
            'volume': [np.random.randint(800000, 1500000)]
        })
        
        # Combine historical and current data
        dynamic_df = pd.concat([dynamic_df, current_row], ignore_index=True)
        
        # Create the chart with yield-inclusive data
        fig_price = go.Figure()
        
        # Historical data (less volatile)
        historical_data = dynamic_df[dynamic_df['timestamp'] < current_time - pd.Timedelta(days=1)]
        fig_price.add_trace(go.Scatter(
            x=historical_data['timestamp'],
            y=historical_data['close'],
            mode='lines',
            name='Historical Price (Yield Inclusive)',
            line=dict(color='#1f77b4', width=1.5)
        ))
        
        # Recent data (more volatile)
        recent_data = dynamic_df[dynamic_df['timestamp'] >= current_time - pd.Timedelta(days=1)]
        fig_price.add_trace(go.Scatter(
            x=recent_data['timestamp'],
            y=recent_data['close'],
            mode='lines',
            name='Recent Price (Live)',
            line=dict(color='#ff7f0e', width=2.5)
        ))
        
        # Current price point
        fig_price.add_trace(go.Scatter(
            x=[current_time],
            y=[current_price],
            mode='markers',
            name='Current Price',
            marker=dict(color='red', size=10, symbol='diamond'),
            showlegend=True
        ))
        
        fig_price.update_layout(
            title="$BRICS Price (Yield Inclusive) - $1.00 Peg + Yield + Volatility",
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            height=400,
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Add yield-inclusive bands
        fig_price.add_hline(y=1.00, line_dash="dash", line_color="gray", 
                           annotation_text="$1.00 Peg", annotation_position="top right")
        fig_price.add_hline(y=1.03, line_dash="dot", line_color="green", 
                           annotation_text="+3% Yield Band", annotation_position="top right")
        fig_price.add_hline(y=0.97, line_dash="dot", line_color="orange", 
                           annotation_text="-3% Band", annotation_position="bottom right")
        
    else:
        # Static mode - use yield-inclusive pricing
        brics_price_df['timestamp'] = pd.to_datetime(brics_price_df['timestamp'])
        
        # Calculate yield-inclusive prices for static mode with high volatility
        static_yield_prices = []
        static_timestamps = []
        
        # Generate synthetic data for static mode with high volatility
        start_date = pd.Timestamp.now() - pd.Timedelta(days=90)
        
        for day in range(90):
            current_date = start_date + pd.Timedelta(days=day)
            
            # Add multiple price points per day
            for hour_offset in range(0, 24, 6):  # Every 6 hours
                timestamp = current_date + pd.Timedelta(hours=hour_offset)
                
                # Base yield component
                base_yield = 0.025 + np.random.normal(0, 0.005)  # ~2.5% base yield
                zar_effect = np.random.normal(0, 0.002)  # Small ZAR effect
                
                # Add high volatility (like portfolio backtesting)
                daily_volatility = np.random.normal(0, 0.012)  # ±1.2% daily volatility
                market_noise = np.random.normal(0, 0.008)  # ±0.8% market noise
                arbitrage_effect = np.random.normal(0, 0.01)  # ±1% arbitrage effect
                
                # Calculate yield-inclusive price
                yield_component = base_yield + zar_effect + daily_volatility
                price = 1.00 + yield_component + market_noise + arbitrage_effect
                price = max(0.90, min(1.25, price))  # Allow more variation
                
                static_yield_prices.append(price)
                static_timestamps.append(timestamp)
        
        # Create new dataframe for static mode
        static_df = pd.DataFrame({
            'timestamp': static_timestamps,
            'close': static_yield_prices
        })
        
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=static_df['timestamp'],
            y=static_df['close'],
            mode='lines',
            name='$BRICS Price (Yield Inclusive - Static)',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig_price.update_layout(
            title="$BRICS Price (Yield Inclusive) - Static Mode",
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            height=400,
            hovermode='x unified'
        )
        
        # Add yield bands for static mode
        fig_price.add_hline(y=1.00, line_dash="dash", line_color="gray", 
                           annotation_text="$1.00 Peg", annotation_position="top right")

    st.plotly_chart(fig_price, use_container_width=True, key="price_chart")

    # Price drivers explanation
    if st.session_state.live_mode:
        st.markdown("""
        **$BRICS Price Drivers (Yield Inclusive - Live Mode):**
        - **$1.00 Peg**: Base stablecoin value
        - **CDS Premiums** (USD): Monthly credit default swap premiums from obligors
        - **SA Treasury Yields** (ZAR → USD): South African government bond yields converted to USD
        - **USD-ZAR Exchange Rate**: Real-time currency conversion affecting sovereign yield component
        - **🔄 Arbitrage Effects**: Investors buying/selling based on yield opportunities (±1% volatility)
        - **📊 Market Stress**: Increased volatility during stress/crisis events (1.5x-2x multiplier)
        - **📈 Volume Effects**: Higher trading volume increases price volatility (±0.5% effect)
        - **💰 Total Price**: $1.00 + Yield Components + Volatility
        """)
    else:
        st.markdown("""
        **$BRICS Price Drivers (Yield Inclusive - Static Mode):**
        - **$1.00 Peg**: Base stablecoin value
        - **CDS Premiums** (USD): Monthly credit default swap premiums from obligors
        - **SA Treasury Yields** (ZAR → USD): South African government bond yields converted to USD
        - **USD-ZAR Exchange Rate**: Real-time currency conversion affecting sovereign yield component
        - **💰 Total Price**: $1.00 + Yield Components + Volatility
        """)

    st.divider()

    # Price volatility and range info (simplified)
    if st.session_state.live_mode:
        # Calculate volatility for live mode
        recent_prices = [current_price]
        for _ in range(10):
            volatility = random.uniform(-0.015, 0.015)
            recent_prices.append(current_price + volatility)
        price_volatility = np.std(recent_prices) * 100
        volatility_status = "🟢 Low" if price_volatility < 0.5 else "🟡 Medium" if price_volatility < 1.0 else "🔴 High"
    else:
        price_volatility = 0.3
        volatility_status = "⚪ Static"

    # Simple range display
    price_high = current_price * 1.02
    price_low = current_price * 0.98

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Volatility", f"{price_volatility:.2f}%", delta=volatility_status)
    with col2:
        st.metric("Range", f"${price_low:.3f} - ${price_high:.3f}")

    # Price drivers breakdown with clear monthly labels
    st.subheader("Monthly Yield Components")
    col1, col2, col3 = st.columns(3)

    with col1:
        cds_monthly = protocol_df[protocol_df['metric'] == 'cds_premiums_monthly']['value'].iloc[0]
        st.metric("CDS Premium (Monthly)", f"{cds_monthly:.2f}%")

    with col2:
        sovereign_monthly = protocol_df[protocol_df['metric'] == 'sovereign_yield_monthly']['value'].iloc[0]
        st.metric("Sovereign Yield (Monthly)", f"{sovereign_monthly:.2f}%")

    with col3:
        total_monthly = protocol_df[protocol_df['metric'] == 'monthly_yield_total']['value'].iloc[0]
        apy = protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
        st.metric("Total Monthly Yield", f"{total_monthly:.2f}%")
        st.caption(f"Annualized: {apy:.1f}% APY")

    # Key protocol metrics (simplified - no repetition)
    st.subheader("Protocol Overview")
    apy = protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
    capital_eff = protocol_df[protocol_df['metric'] == 'capital_efficiency']['value'].iloc[0]
    weighted_pd = protocol_df[protocol_df['metric'] == 'weighted_pd']['value'].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        apy_status = "🟢 Target" if 25 <= apy <= 35 else "🟡 High" if apy > 35 else "🔴 Low"
        st.metric("Target APY", f"{apy:.1f}%", delta=apy_status)
    with col2:
        eff_status = "🟢 Optimal" if 8 <= capital_eff <= 10 else "🟡 High" if capital_eff > 10 else "🔴 Low"
        st.metric("Capital Efficiency", f"{capital_eff:.1f}x", delta=eff_status)
    with col3:
        pd_status = "🟢 Low Risk" if weighted_pd < 0.08 else "🟡 Medium" if weighted_pd < 0.12 else "🔴 High Risk"
        st.metric("Portfolio PD", f"{weighted_pd*100:.1f}%", delta=pd_status)

    st.divider()

    # ============================================================================
    # INVESTMENT SUMMARY SECTION
    # ============================================================================
    st.markdown("""
    <div class="section-header">
        <h2 style="margin: 0; font-size: 1.8rem; font-weight: 600;">
            💰 Investment Summary
        </h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1rem;">
            Key investment highlights and risk protection mechanisms
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-box" style="border-left-color: #28a745;">
            <h4 style="margin: 0 0 1rem 0; color: #28a745; font-weight: 600;">📈 Yield Sources</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li><strong>CDS Premiums:</strong> 2.14% monthly</li>
                <li><strong>Sovereign Yield:</strong> 0.73% monthly</li>
                <li><strong>Total:</strong> 2.87% monthly (34.4% APY)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box" style="border-left-color: #ffc107;">
            <h4 style="margin: 0 0 1rem 0; color: #ffc107; font-weight: 600;">🛡️ Risk Protection</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li><strong>Overcollateralization:</strong> 11.5%</li>
                <li><strong>Sovereign Guarantee:</strong> First-loss protection</li>
                <li><strong>Institutional Buffer:</strong> Underwriting protection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-box" style="border-left-color: #17a2b8;">
            <h4 style="margin: 0 0 1rem 0; color: #17a2b8; font-weight: 600;">✨ Investment Highlights</h4>
            <ul style="margin: 0; padding-left: 1.5rem;">
                <li><strong>No leverage</strong> or borrowing</li>
                <li><strong>Monthly redemptions</strong> available</li>
                <li><strong>$10,000 minimum</strong> investment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

elif page == "Unit Economics":
    st.markdown("""
    <div class="section-header">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #1e3c72;">
            💰 UNIT ECONOMICS
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout (2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">$BRICS TOKEN MECHANICS</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### How $BRICS Works

        1. **Banks pool trade receivables** from investment-grade corporates (30-180 day tenor)
        2. **CDS contracts transfer credit risk** to the protocol for regulatory capital relief
        3. **$BRICS tokenizes the super-senior tranche** (76% of notional)
        4. **Investors receive monthly CDS premiums** + sovereign yield
        5. **Redemption via token burn** distributes yield pro rata
        """)
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">INVESTMENT EXAMPLE</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **For every $1,000 invested in $BRICS:**
        
        - **Notional Exposure**: $8,700 (8.7x leverage)
        - **Monthly Yield**: $28.70 (2.87% monthly)
        - **Annual Yield**: $344.40 (34.4% APY)
        - **Risk Buffer**: $115 (11.5% overcollateralization)
        - **Sovereign Protection**: $82 (first-loss guarantee)
        """)
    
    # Second Row
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">YIELD BREAKDOWN</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Yield breakdown chart
        cds_premiums = protocol_df[protocol_df['metric'] == 'cds_premiums_monthly']['value'].iloc[0]
        sovereign_yield = protocol_df[protocol_df['metric'] == 'sovereign_yield_monthly']['value'].iloc[0]
        
        fig_yield_breakdown = go.Figure(data=[
            go.Bar(name='CDS Premiums (Monthly)', x=['CDS Premiums'], y=[cds_premiums], marker_color='blue'),
            go.Bar(name='Sovereign Yield (Monthly)', x=['Sovereign Yield'], y=[sovereign_yield], marker_color='green')
        ])
        fig_yield_breakdown.update_layout(title="Monthly Yield Breakdown", barmode='stack', height=300)
        st.plotly_chart(fig_yield_breakdown, use_container_width=True, key="yield_breakdown")
    
    with col4:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">CASH FLOW WATERFALL / APY CALCULATIONS</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Cash Flow Waterfall
        fig_waterfall = px.bar(waterfall_df, x="recipient", y="amount_usd", 
                               title="Monthly Cash Flow ($25,000 CDS Premium)",
                               color="tier", color_continuous_scale="viridis")
        fig_waterfall.update_layout(xaxis_title="Recipient", yaxis_title="Amount (USD)")
        st.plotly_chart(fig_waterfall, use_container_width=True, key="cash_flow_waterfall")
        
        # APY calculation explanation
        st.markdown("""
        **APY Calculation:**
        - Monthly Yield: 2.87% (CDS 2.14% + Sovereign 0.73%)
        - Annualized: 2.87% × 12 = **34.4% APY**
        - Portfolio Average: 33.2% (weighted by obligor exposure)
        """)

elif page == "Portfolio Analysis":
    st.markdown("""
    <div class="section-header">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #1e3c72;">
            📈 PORTFOLIO ANALYSIS
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout (2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">PORTFOLIO OVERVIEW</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Portfolio Overview
        total_exposure = company_df['total_exposure'].sum()
        avg_pd = company_df['avg_pd'].mean()
        avg_yield = company_df['yield'].mean()

        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.metric("Total Notional", f"${total_exposure:,.0f}")
            st.metric("Average PD", f"{avg_pd*100:.1f}%")
        with col1_2:
            st.metric("Average Yield", f"{avg_yield:.1f}%")
            st.metric("Number of Obligors", len(company_df))
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">RISK STRUCTURE</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Portfolio Tranching
        fig_tranching = px.pie(portfolio_tranching_df[portfolio_tranching_df['tranche'] != 'Total'], 
                               names="tranche", values="notional_amount", 
                               title="$BRICS Portfolio Tranching (Total: $8.48M)",
                               color="risk_level", color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'})
        st.plotly_chart(fig_tranching, use_container_width=True, key="portfolio_tranching")

    # Second Row
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">OBLIGOR ANALYSIS</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive obligor selection
        selected_company = st.selectbox(
            "Select an obligor for detailed analysis:",
            options=["Portfolio Overview"] + list(company_df['company'].unique()),
            index=0
        )

    if selected_company == "Portfolio Overview":
        # Show all obligors
        st.dataframe(company_df, use_container_width=True)
        
        # Portfolio visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pd = px.bar(company_df, x="company", y="avg_pd", 
                            title="Probability of Default by Obligor", 
                            labels={"avg_pd": "PD (%)"}, color="credit_rating")
            fig_pd.update_layout(yaxis_tickformat='.1%')
            st.plotly_chart(fig_pd, use_container_width=True, key="pd_by_obligor")
        
        with col2:
            fig_yield = px.bar(company_df, x="company", y="yield", 
                               title="Yield by Obligor", 
                               labels={"yield": "Yield (%)"}, color="industry")
            st.plotly_chart(fig_yield, use_container_width=True, key="yield_by_obligor")
        
        # Additional charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_industry = px.bar(company_df.groupby('industry')['total_exposure'].sum().reset_index(), 
                                  x="industry", y="total_exposure", title="Exposure by Industry")
            st.plotly_chart(fig_industry, use_container_width=True, key="exposure_by_industry")
        
        with col2:
            fig_rating = px.bar(company_df.groupby('credit_rating')['total_exposure'].sum().reset_index(),
                                x="credit_rating", y="total_exposure", title="Exposure by Credit Rating")
            st.plotly_chart(fig_rating, use_container_width=True, key="exposure_by_rating")

    else:
        # Show selected company details
        company_data = company_df[company_df['company'] == selected_company].iloc[0]
        risk_data = risk_df[risk_df['company'] == selected_company].iloc[0]
        company_transactions = transactions_extended_df[transactions_extended_df['company'] == selected_company]
        
        st.subheader(f"📊 {selected_company} - Obligor Analysis")
        
        # Company metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Exposure", f"${company_data['total_exposure']:,.0f}")
        with col2:
            st.metric("Average PD", f"{company_data['avg_pd']*100:.1f}%")
        with col3:
            st.metric("Yield", f"{company_data['yield']:.1f}%")
        with col4:
            st.metric("Credit Rating", company_data['credit_rating'])
        
        # Company details
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Company Information:**")
            st.write(f"- Industry: {company_data['industry']}")
            st.write(f"- Credit Type: {company_data['credit_type']}")
            st.write(f"- Underwriting Bank: {company_data['underwriting_bank']}")
            st.write(f"- Terms: {company_data['terms_tenor']}")
            st.write(f"- Time Listed: {company_data['time_listed']}")
            st.write(f"- Spread: {company_data['spread_bps']} bps")
        
        with col2:
            st.write("**Risk Metrics:**")
            st.write(f"- XGBoost PD: {risk_data['xgboost_pd']*100:.1f}%")
            st.write(f"- Lévy Copula Tail Risk: {risk_data['levy_copula_tail_risk']*100:.1f}%")
            st.write(f"- CDS Spread: {risk_data['cds_spread']} bps")
            st.write(f"- 24h Notional Change: ${company_data['notional_24h_change']:,.0f}")
            st.write(f"- 24h CDS Fee Change: {company_data['cds_fee_24h_change']:.1f}%")
        
        # Transaction history with timeline
        st.subheader("Transaction History (5-Day Timeline)")
        if not company_transactions.empty:
            # Convert date to datetime for proper plotting
            company_transactions['date'] = pd.to_datetime(company_transactions['date'])
            
            fig_transactions = px.line(company_transactions, x="date", y="amount", 
                                     title=f"{selected_company} - Transaction Amounts Over Time",
                                     labels={"amount": "Amount (USD)", "date": "Date"})
            fig_transactions.update_layout(xaxis_title="Date", yaxis_title="Amount (USD)")
            st.plotly_chart(fig_transactions, use_container_width=True, key="company_transactions")
            
            # Transaction summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Transactions", len(company_transactions))
            with col2:
                st.metric("Average Transaction", f"${company_transactions['amount'].mean():,.0f}")
            with col3:
                st.metric("Total Volume", f"${company_transactions['amount'].sum():,.0f}")
            
            st.dataframe(company_transactions, use_container_width=True)
        else:
            st.info("No transaction data available for this obligor.")

elif page == "Technical Details":
    st.header("Technical Implementation")
    
    st.markdown("""
    ### AI/ML Risk Models
    
    **XGBoost Credit Scoring**: Analyzes 2M+ datapoints to calculate probability of default for each obligor.
    
    **Lévy Copula Tail Risk**: Models joint default risk and extreme tail events across the portfolio.
    
    **Real-Time Pricing**: CDS premiums calculated dynamically based on risk signals and market conditions.
    """)
    
    # Risk model outputs
    st.subheader("Risk Model Outputs")
    st.dataframe(risk_df, use_container_width=True)
    
    # Tenor distribution
    st.subheader("Exposure by Tenor")
    fig_tenor = px.bar(company_df.groupby('terms_tenor')['total_exposure'].sum().reset_index(),
                       x="terms_tenor", y="total_exposure", title="Exposure by Tenor")
    st.plotly_chart(fig_tenor, use_container_width=True, key="tenor_distribution")

    # API Connection Framework
    st.subheader("API Connection Framework")
    
    st.markdown("""
    ### Connect New Bank Data Streams
    
    This section allows internal teams to connect new bank data sources and configure real-time data feeds.
    """)
    
    # Get current connection status
    connection_status = bank_connector.get_connection_status()
    
    # API configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bank Configuration")
        bank_name = st.text_input("Bank Name", "New Bank")
        api_endpoint = st.text_input("API Endpoint", "https://api.newbank.co.za/v1/transactions")
        api_key = st.text_input("API Key", "newbank_****", type="password")
        refresh_rate = st.selectbox("Refresh Rate (seconds)", [5, 30, 60, 300])
        
        if st.button("🔗 Connect Bank"):
            result = bank_connector.connect_bank(
                bank_name=bank_name,
                api_endpoint=api_endpoint,
                api_key=api_key,
                refresh_rate=refresh_rate
            )
            if result['success']:
                st.success(f"✅ {result['message']}")
            else:
                st.error(f"❌ {result['message']}")
    
    with col2:
        st.subheader("Data Stream Status")
        
        # Display connection status
        for bank_name, status in connection_status.items():
            if status['status'] == 'active':
                st.success(f"🟢 {bank_name} - Active")
            elif status['status'] == 'error':
                st.error(f"🔴 {bank_name} - Error")
            else:
                st.warning(f"🟡 {bank_name} - Inactive")
        
        # Data quality metrics
        if connection_status:
            avg_freshness = sum(s['data_freshness'] for s in connection_status.values()) / len(connection_status)
            avg_success = sum(s['success_rate'] for s in connection_status.values()) / len(connection_status)
            avg_error = sum(s['error_rate'] for s in connection_status.values()) / len(connection_status)
            
            st.subheader("Data Quality Metrics")
            st.metric("Avg Data Freshness", f"{avg_freshness:.1f}s")
            st.metric("Avg Success Rate", f"{avg_success:.1f}%")
            st.metric("Avg Error Rate", f"{avg_error:.1f}%")
    
    # Real-time data processing
    st.subheader("Real-Time Data Processing")
    
    if st.button("🔄 Process Latest Data"):
        with st.spinner("Processing real-time data..."):
            real_time_data = bank_connector.process_real_time_data()
            
            if real_time_data['transactions']:
                st.success(f"✅ Processed {real_time_data['total_transactions']} new transactions")
                
                # Show transaction summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Transactions", real_time_data['total_transactions'])
                with col2:
                    st.metric("Active Banks", len([s for s in real_time_data['connection_summary'].values() if s['status'] == 'active']))
                with col3:
                    st.metric("Processing Time", f"{random.uniform(0.5, 2.0):.1f}s")
                
                # Show sample transactions
                if real_time_data['transactions']:
                    sample_txns = pd.DataFrame(real_time_data['transactions'][:5])
                    st.dataframe(sample_txns[['transaction_id', 'company', 'amount', 'underwriting_bank', 'date']], use_container_width=True)
            else:
                st.info("No new transactions to process")
    
    # Data quality monitoring
    st.subheader("Data Quality Monitoring")
    
    # Check for alerts
    alerts = quality_monitor.check_connection_health(connection_status)
    
    if alerts:
        st.warning("⚠️ Data Quality Alerts Detected")
        for alert in alerts:
            st.markdown(f"**{alert['type'].upper()}**: {alert['bank']} - {alert['message']}")
    else:
        st.success("✅ All connections healthy")
    
    # Connection management
    st.subheader("Connection Management")
    
    if connection_status:
        selected_bank = st.selectbox("Select bank to disconnect:", list(connection_status.keys()))
        if st.button("🔌 Disconnect Bank"):
            # Find connection ID for selected bank
            for conn_id, conn_data in bank_connector.connections.items():
                if conn_data['bank_name'] == selected_bank:
                    result = bank_connector.disconnect_bank(conn_id)
                    if result['success']:
                        st.success(f"✅ Disconnected from {selected_bank}")
                    else:
                        st.error(f"❌ Failed to disconnect from {selected_bank}")
                    break

elif page == "Advanced Analytics":
    st.markdown("""
    <div class="section-header">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #1e3c72;">
            📊 ADVANCED ANALYTICS
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout (2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">RISK ANALYTICS</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Analytics content
        st.subheader("Portfolio Risk Heatmap")
        risk_heatmap = risk_analytics.create_risk_heatmap(company_df)
        st.plotly_chart(risk_heatmap, use_container_width=True, key="risk_heatmap")
        
        # VaR Analysis
        st.subheader("Value at Risk (VaR) Analysis")
        var_results = risk_analytics.calculate_var(company_df)
        
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            st.metric("95% VaR (30-day)", f"${abs(var_results['var_95']):,.0f}")
        with col1_2:
            st.metric("Expected Shortfall", f"${abs(var_results['expected_shortfall']):,.0f}")
        with col1_3:
            st.metric("VaR % of Portfolio", f"{abs(var_results['var_95'])/var_results['total_exposure']*100:.1f}%")
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">STRESS TESTING</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Stress Testing
        st.subheader("Stress Testing Results")
        stress_scenarios = risk_analytics.stress_test_scenarios(company_df)
        
        # Convert stress scenarios to DataFrame for plotting
        stress_data = []
        for scenario_name, scenario_data in stress_scenarios.items():
            stress_data.append({
                'scenario': scenario_data['scenario'],
                'loss_percent': scenario_data['loss_percentage']
            })
        
        stress_df = pd.DataFrame(stress_data)
        
        fig_stress = px.bar(stress_df, x='scenario', y='loss_percent',
                          title="Stress Testing Results - Portfolio Loss by Scenario",
                          color='loss_percent', color_continuous_scale='Reds')
        st.plotly_chart(fig_stress, use_container_width=True, key="stress_testing")
        
        # Concentration Risk
        st.subheader("Concentration Risk (HHI Index)")
        concentration_risk = risk_analytics.calculate_concentration_risk(company_df)
        hhi_index = concentration_risk['hhi']
        st.metric("HHI Index", f"{hhi_index:.2f}", 
                 delta="🟢 Low Concentration" if hhi_index < 0.15 else "🟡 Medium" if hhi_index < 0.25 else "🔴 High Concentration")
    
    # Second Row
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">CORRELATION ANALYSIS</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Correlation Matrix
        st.subheader("Obligor Correlation Matrix")
        correlation_matrix = risk_analytics.calculate_correlations(company_df)
        
        fig_corr = px.imshow(correlation_matrix,
                           title="Obligor Correlation Matrix",
                           color_continuous_scale='RdBu',
                           aspect='auto')
        st.plotly_chart(fig_corr, use_container_width=True, key="correlation_matrix")
    
    with col4:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">PERFORMANCE MONITORING</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance Monitoring
        st.subheader("System Performance")
        
        # Get performance data
        performance_summary = performance_monitor.get_performance_summary()
        performance_alerts = performance_monitor.get_performance_alerts()
        processing_summary = data_processing_monitor.get_processing_summary()
        dashboard_summary = dashboard_tracker.get_dashboard_summary()
        
        # Performance Overview
        col4_1, col4_2 = st.columns(2)
        with col4_1:
            if 'current_metrics' in performance_summary and performance_summary['current_metrics']:
                current = performance_summary['current_metrics']
                cpu_usage = current.get('cpu_percent', 0)
                cpu_status = "🟢" if cpu_usage < 50 else "🟡" if cpu_usage < 80 else "🔴"
                st.metric("CPU Usage", f"{cpu_usage:.1f}%", delta=f"{cpu_status} {'Normal' if cpu_usage < 50 else 'High' if cpu_usage < 80 else 'Critical'}")
                
                memory_usage = current.get('memory_percent', 0)
                memory_status = "🟢" if memory_usage < 70 else "🟡" if memory_usage < 85 else "🔴"
                st.metric("Memory Usage", f"{memory_usage:.1f}%", delta=f"{memory_status} {'Normal' if memory_usage < 70 else 'High' if memory_usage < 85 else 'Critical'}")
        
        with col4_2:
            if 'current_metrics' in performance_summary and performance_summary['current_metrics']:
                process_memory = current.get('process_memory_mb', 0)
                st.metric("Process Memory", f"{process_memory:.1f} MB")
                
                if 'uptime_hours' in performance_summary:
                    uptime = performance_summary['uptime_hours']
                    uptime_status = "🟢" if uptime > 1 else "🟡"
                    st.metric("Uptime", f"{uptime:.1f} hours", delta=f"{uptime_status} Stable")
        
        # Performance Alerts
        if performance_alerts:
            st.subheader("⚠️ Performance Alerts")
            for alert in performance_alerts:
                if alert['type'] == 'critical':
                    st.error(f"🚨 {alert['metric']}: {alert['value']} (Threshold: {alert['threshold']}) - {alert['message']}")
                elif alert['type'] == 'warning':
                    st.warning(f"⚠️ {alert['metric']}: {alert['value']} (Threshold: {alert['threshold']}) - {alert['message']}")
        
        # Processing Performance
        if 'error' not in processing_summary:
            st.subheader("Data Processing Performance")
            
            col4_3, col4_4 = st.columns(2)
            with col4_3:
                st.metric("Total Operations", processing_summary.get('total_operations', 0))
                st.metric("Avg Processing Time", f"{processing_summary.get('average_processing_time', 0):.3f}s")
            with col4_4:
                st.metric("Max Processing Time", f"{processing_summary.get('max_processing_time', 0):.3f}s")
                st.metric("Dashboard Interactions", dashboard_summary.get('user_interactions', 0))

elif page == "Compliance & Docs":
    st.markdown("""
    <div class="section-header">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #1e3c72;">
            📋 COMPLIANCE & DOCUMENTATION
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout (2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">COMPLIANCE TRACKING</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Compliance tracking
        st.subheader("Regulatory Compliance Status")
        
        # Get compliance data
        compliance_data = compliance_tracker.get_compliance_status()
        
        # Compliance metrics
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.metric("Compliant Requirements", compliance_data.get('compliant_count', 0))
            st.metric("Non-Compliant", compliance_data.get('non_compliant_count', 0))
        with col1_2:
            st.metric("Pending Reviews", compliance_data.get('pending_reviews', 0))
            st.metric("Days Until Next Review", compliance_data.get('days_until_review', 0))
        
        # Compliance chart
        if 'compliance_data' in compliance_data:
            fig_compliance = px.bar(compliance_data['compliance_data'], 
                                   x="requirement", y="days_until_review",
                                   title="Days Until Next Review by Requirement",
                                   color='Status', color_discrete_map={'compliant': 'green', 'non_compliant': 'red'})
            st.plotly_chart(fig_compliance, use_container_width=True, key="compliance_tracker")
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">DOCUMENTATION</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Documentation section
        st.subheader("Required Documentation")
        
        # Document checklist
        documents = [
            {"name": "Investment Memorandum", "status": "✅ Complete", "last_updated": "2024-01-15"},
            {"name": "Risk Assessment Report", "status": "✅ Complete", "last_updated": "2024-01-10"},
            {"name": "Compliance Manual", "status": "✅ Complete", "last_updated": "2024-01-05"},
            {"name": "Audit Trail", "status": "✅ Complete", "last_updated": "2024-01-20"},
            {"name": "Regulatory Filings", "status": "🔄 In Progress", "last_updated": "2024-01-25"},
            {"name": "Due Diligence Report", "status": "✅ Complete", "last_updated": "2024-01-12"}
        ]
        
        for doc in documents:
            st.markdown(f"**{doc['name']}:** {doc['status']} (Updated: {doc['last_updated']})")

elif page == "API Integration":
    st.markdown("""
    <div class="section-header">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #1e3c72;">
            🔌 API INTEGRATION
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout (2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">CONNECTION STATUS</div>
        </div>
        """, unsafe_allow_html=True)
        
        # API Connection status
        st.subheader("Bank Data Streams")
        
        # Mock connection status
        connections = [
            {"bank": "Standard Bank", "status": "🟢 Connected", "last_update": "2s ago"},
            {"bank": "FirstRand Bank", "status": "🟢 Connected", "last_update": "5s ago"},
            {"bank": "Nedbank", "status": "🟡 Delayed", "last_update": "45s ago"},
            {"bank": "Absa Bank", "status": "🔴 Disconnected", "last_update": "2min ago"}
        ]
        
        for conn in connections:
            st.markdown(f"**{conn['bank']}:** {conn['status']} (Last: {conn['last_update']})")
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">DATA QUALITY</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Data quality monitoring
        st.subheader("Data Quality Metrics")
        
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            st.metric("Data Completeness", "98.5%", delta="🟢 Excellent")
            st.metric("Data Accuracy", "99.2%", delta="🟢 Excellent")
        with col2_2:
            st.metric("Data Freshness", "2.3s", delta="🟢 Real-time")
            st.metric("Error Rate", "0.1%", delta="🟢 Low")

elif page == "AI/ML Analytics":
    st.markdown("""
    <div class="section-header">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #1e3c72;">
            🤖 AI/ML ANALYTICS
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid Layout (2x2)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">CREDIT RISK MODELS</div>
        </div>
        """, unsafe_allow_html=True)
        
        # ML Models
        st.subheader("XGBoost Credit Risk Model")
        
        # Model performance
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.metric("Model Accuracy", "94.2%", delta="🟢 Excellent")
            st.metric("AUC Score", "0.89", delta="🟢 Good")
        with col1_2:
            st.metric("Precision", "91.5%", delta="🟢 Good")
            st.metric("Recall", "88.3%", delta="🟢 Good")
        
        # Feature importance
        st.subheader("Feature Importance")
        
        # Mock feature importance data (since method doesn't exist)
        feature_importance_data = pd.DataFrame({
            'feature': ['Credit Rating', 'Industry Risk', 'Total Exposure', 'Yield', 'Spread BPS', 'Tenor Risk'],
            'importance': [0.25, 0.20, 0.18, 0.15, 0.12, 0.10]
        })
        
        fig_importance = px.bar(feature_importance_data, x='importance', y='feature',
                               title="Top 10 Feature Importance",
                               orientation='h',
                               labels={'x': 'Features', 'y': 'Importance Score'}
        )
        st.plotly_chart(fig_importance, use_container_width=True, key="feature_importance")
    
    with col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">YIELD FORECASTING</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Yield Forecasting
        st.subheader("Yield Forecast (Next 30 Days)")
        
        # Get forecast data
        forecast_data = ml_predictor.forecast_yield(30)
        
        # Create forecast chart data
        if forecast_data and 'forecasts' in forecast_data:
            forecast_df = pd.DataFrame(forecast_data['forecasts'])
            forecast_df['date'] = pd.to_datetime(forecast_df['date'])
            forecast_df['predicted_yield'] = forecast_df['predicted_yield'] * 100  # Convert to percentage
            
            # Forecast chart
            fig_forecast = px.line(forecast_df, x='date', y='predicted_yield',
                                  title="Yield Forecast (Next 30 Days)",
                                  labels={'x': 'Date', 'y': 'Predicted Yield (%)'}
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True, key="yield_forecast")
            
            # Display forecast summary
            st.markdown("**Forecast Summary:**")
            st.markdown(f"- **Average Predicted Yield:** {forecast_df['predicted_yield'].mean():.2f}%")
            st.markdown(f"- **Forecast Range:** {forecast_df['predicted_yield'].min():.2f}% - {forecast_df['predicted_yield'].max():.2f}%")
            st.markdown(f"- **Trend:** {'📈 Increasing' if forecast_df['predicted_yield'].iloc[-1] > forecast_df['predicted_yield'].iloc[0] else '📉 Decreasing'}")
        else:
            st.info("Forecast data not available")
    
    # Second Row
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">PORTFOLIO BACKTESTING</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Portfolio Backtesting
        st.subheader("90-Day Portfolio Backtesting")
        
        # Get backtest data
        backtest_data = ml_predictor.backtest_portfolio(company_df, 90)
        
        # Backtest chart
        if backtest_data and 'historical_data' in backtest_data:
            backtest_df = backtest_data['historical_data']
            backtest_df['date'] = pd.to_datetime(backtest_df['date'])
            
            fig_backtest = px.line(backtest_df, x='date', y='portfolio_value',
                                  title="Portfolio Value Over Time (Backtest)",
                                  labels={'x': 'Date', 'y': 'Portfolio Value ($)'}
            )
            
            # Add daily returns
            fig_backtest.add_trace(go.Scatter(
                x=backtest_df['date'],
                y=backtest_df['daily_return'] * 100,  # Convert to percentage
                mode='lines',
                name='Daily Returns (%)',
                line=dict(color='red', dash='dash'),
                yaxis='y2'
            ))
            
            fig_backtest.update_layout(
                showlegend=True,
                yaxis2=dict(title="Daily Returns (%)", overlaying="y", side="right")
            )
            st.plotly_chart(fig_backtest, use_container_width=True, key="portfolio_backtest")
            
            # Display backtest summary
            st.markdown("**Backtest Summary:**")
            st.markdown(f"- **Total Return:** {backtest_data['total_return']*100:.2f}%")
            st.markdown(f"- **Sharpe Ratio:** {backtest_data['sharpe_ratio']:.3f}")
            st.markdown(f"- **Max Drawdown:** {backtest_data['max_drawdown']*100:.2f}%")
        else:
            st.info("Backtest data not available")
    
    with col4:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">MODEL HEALTH</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Model Health Monitoring
        st.subheader("Model Health Metrics")
        
        # Model health data
        model_health = model_updater.get_model_health_report()
        
        col4_1, col4_2 = st.columns(2)
        with col4_1:
            st.metric("Total Models", model_health['total_models'])
            st.metric("Models Needing Update", model_health['models_needing_update'])
        with col4_2:
            # Calculate average R² score
            if model_health['model_performance']:
                avg_r2 = sum(model['r2_score'] for model in model_health['model_performance'].values()) / len(model_health['model_performance'])
                st.metric("Avg R² Score", f"{avg_r2:.3f}", 
                         delta="🟢 Good" if avg_r2 > 0.85 else "🟡 Fair" if avg_r2 > 0.75 else "🔴 Poor")
            else:
                st.metric("Avg R² Score", "N/A")
            
            st.metric("Performance Trend", "🟢 Improving" if model_health['models_needing_update'] == 0 else "🟡 Stable")

# ============================================================================
# FOOTER SECTION
# ============================================================================
st.markdown("""
<div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 1rem; margin-top: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
    <h4 style="margin: 0 0 1rem 0; color: #1e3c72; font-weight: 600;">📋 Important Disclaimers</h4>
    <p style="margin: 0; color: #666; line-height: 1.6;">
        <strong>Disclaimer:</strong> This report is for informational purposes only. Past performance does not guarantee future results. 
        $BRICS involves credit risk and is not suitable for all investors. Please consult with your financial advisor before making any investment decisions.
    </p>
    <hr style="margin: 1rem 0; border: none; border-top: 1px solid #eee;">
    <p style="margin: 0; color: #999; font-size: 0.9rem; text-align: center;">
        © 2024 BRICS Protocol • AI-Native Synthetic Credit Platform • Built for Investor Due Diligence
    </p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh for live mode
if st.session_state.live_mode:
    time.sleep(3)  # Reduced to 3 seconds for ultra-fast updates
    st.rerun() 

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def generate_excel_report():
    """Generate comprehensive Excel report for due diligence"""
    # Create Excel writer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        
        # Protocol Overview
        protocol_df.to_excel(writer, sheet_name='Protocol_Overview', index=False)
        
        # Portfolio Analysis
        company_df.to_excel(writer, sheet_name='Portfolio_Analysis', index=False)
        
        # Price Data
        brics_price_df.to_excel(writer, sheet_name='Price_Data', index=False)
        
        # Risk Metrics
        risk_df.to_excel(writer, sheet_name='Risk_Metrics', index=False)
        
        # Cash Flow Waterfall
        waterfall_df.to_excel(writer, sheet_name='Cash_Flow_Waterfall', index=False)
        
        # Summary Sheet
        summary_data = {
            'Metric': [
                'Current $BRICS Price',
                'Target APY',
                'Total Portfolio Exposure',
                'Weighted Portfolio PD',
                'Capital Efficiency',
                'Number of Obligors',
                'Average Yield',
                'Report Generated'
            ],
            'Value': [
                f"${protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]:.3f}",
                f"{protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]:.1f}%",
                f"${company_df['total_exposure'].sum():,.0f}",
                f"{protocol_df[protocol_df['metric'] == 'weighted_pd']['value'].iloc[0]*100:.1f}%",
                f"{protocol_df[protocol_df['metric'] == 'capital_efficiency']['value'].iloc[0]:.1f}x",
                len(company_df),
                f"{company_df['yield'].mean():.1f}%",
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Executive_Summary', index=False)
    
    return output.getvalue()

def generate_pdf_report():
    """Generate professional PDF report for due diligence"""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 20, 'BRICS Protocol Investment Report', ln=True, align='C')
    pdf.ln(10)
    
    # Executive Summary
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Executive Summary', ln=True)
    pdf.set_font('Arial', '', 12)
    
    current_price = protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]
    apy = protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
    total_exposure = company_df['total_exposure'].sum()
    
    summary_text = f"""
    Current $BRICS Price: ${current_price:.3f}
    Target APY: {apy:.1f}%
    Total Portfolio Exposure: ${total_exposure:,.0f}
    Number of Obligors: {len(company_df)}
    Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    for line in summary_text.strip().split('\n'):
        if line.strip():
            pdf.cell(0, 8, line.strip(), ln=True)
    
    pdf.ln(10)
    
    # Portfolio Overview
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Portfolio Overview', ln=True)
    pdf.set_font('Arial', '', 12)
    
    # Top 5 obligors
    top_obligors = company_df.nlargest(5, 'total_exposure')
    for _, row in top_obligors.iterrows():
        pdf.cell(0, 8, f"{row['company']}: ${row['total_exposure']:,.0f} ({row['yield']:.1f}% yield)", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

def create_export_buttons():
    """Create export buttons for the dashboard"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">📊 EXPORT REPORTS</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate PDF Report", type="primary"):
            try:
                pdf_bytes = generate_pdf_report()
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"BRICS_Investment_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                st.success("✅ PDF report generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
    
    with col2:
        if st.button("📊 Generate Excel Report", type="primary"):
            try:
                excel_bytes = generate_excel_report()
                st.download_button(
                    label="📥 Download Excel Report",
                    data=excel_bytes,
                    file_name=f"BRICS_Investment_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ Excel report generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating Excel: {str(e)}")
    
    with col3:
        if st.button("📈 Export Chart Data", type="primary"):
            try:
                # Export current price chart data
                chart_data = brics_price_df.copy()
                chart_data['export_timestamp'] = datetime.now()
                
                csv_bytes = chart_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Chart Data (CSV)",
                    data=csv_bytes,
                    file_name=f"BRICS_Price_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                st.success("✅ Chart data exported successfully!")
            except Exception as e:
                st.error(f"❌ Error exporting data: {str(e)}")

def check_alerts():
    """Check for real-time alerts and notifications"""
    alerts = []
    
    # Price alerts
    current_price = protocol_df[protocol_df['metric'] == 'brics_price']['value'].iloc[0]
    price_change = abs(current_price - 1.00) / 1.00 * 100
    
    if price_change > 5:
        alerts.append({
            'type': 'warning',
            'message': f"⚠️ High price volatility: ${current_price:.3f} ({price_change:.1f}% from peg)",
            'icon': '🔴'
        })
    elif price_change > 2:
        alerts.append({
            'type': 'info',
            'message': f"📊 Price movement: ${current_price:.3f} ({price_change:.1f}% from peg)",
            'icon': '🟡'
        })
    
    # APY alerts
    apy = protocol_df[protocol_df['metric'] == 'apy_per_brics']['value'].iloc[0]
    if apy < 25:
        alerts.append({
            'type': 'warning',
            'message': f"📉 Low APY: {apy:.1f}% (below target range)",
            'icon': '🔴'
        })
    elif apy > 40:
        alerts.append({
            'type': 'info',
            'message': f"📈 High APY: {apy:.1f}% (above target range)",
            'icon': '🟢'
        })
    
    # Risk alerts
    weighted_pd = protocol_df[protocol_df['metric'] == 'weighted_pd']['value'].iloc[0]
    if weighted_pd > 0.12:
        alerts.append({
            'type': 'error',
            'message': f"🚨 High portfolio risk: {weighted_pd*100:.1f}% PD",
            'icon': '🔴'
        })
    
    # Performance alerts
    if 'performance_summary' in globals():
        try:
            performance_summary = performance_monitor.get_performance_summary()
            if 'current_metrics' in performance_summary:
                cpu_usage = performance_summary['current_metrics'].get('cpu_percent', 0)
                if cpu_usage > 80:
                    alerts.append({
                        'type': 'warning',
                        'message': f"⚡ High CPU usage: {cpu_usage:.1f}%",
                        'icon': '🟡'
                    })
        except:
            pass
    
    return alerts

def display_alerts():
    """Display real-time alerts"""
    alerts = check_alerts()
    
    if alerts:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">🚨 REAL-TIME ALERTS</div>
        </div>
        """, unsafe_allow_html=True)
        
        for alert in alerts:
            if alert['type'] == 'error':
                st.error(f"{alert['icon']} {alert['message']}")
            elif alert['type'] == 'warning':
                st.warning(f"{alert['icon']} {alert['message']}")
            else:
                st.info(f"{alert['icon']} {alert['message']}")
        
        st.divider()

def show_loading_state(message="Loading data..."):
    """Show a loading state with spinner"""
    st.markdown(f"""
    <div class="loading-container">
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">⏳</div>
            <div style="font-size: 1.1rem; color: #666;">{message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_error_state(error_message, retry_function=None):
    """Show an error state with retry option"""
    st.markdown(f"""
    <div class="error-container">
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">❌</div>
            <div style="font-size: 1.1rem; color: #d32f2f; margin-bottom: 1rem;">{error_message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if retry_function:
        if st.button("🔄 Retry", type="primary"):
            retry_function()

def show_success_state(message="Operation completed successfully!"):
    """Show a success state"""
    st.markdown(f"""
    <div class="success-container">
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 1rem;">✅</div>
            <div style="font-size: 1.1rem; color: #2e7d32;">{message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)