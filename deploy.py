#!/usr/bin/env python3
"""
BRICS MVP Deployment Script
Runs comprehensive tests and starts the dashboard
"""

import subprocess
import sys
import os
import time
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'scikit-learn',
        'plotly',
        'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        install_command = f"pip install {' '.join(missing_packages)}"
        if not run_command(install_command, "Installing missing packages"):
            return False
    
    return True

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running comprehensive test suite...")
    
    test_command = "python tests/test_dashboard.py"
    return run_command(test_command, "Running tests")

def check_data_files():
    """Check if all required data files exist"""
    print("\n📁 Checking data files...")
    
    required_files = [
        'data/mock_company_summary.csv',
        'data/mock_protocol_metrics.csv',
        'data/mock_brics_price.csv',
        'data/mock_risk_outputs.csv',
        'data/mock_waterfall.csv',
        'data/mock_portfolio_tranching.csv',
        'data/mock_transactions.csv',
        'data/mock_transactions_extended.csv'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - MISSING")
    
    if missing_files:
        print(f"\n⚠️ Missing data files: {', '.join(missing_files)}")
        return False
    
    return True

def start_dashboard():
    """Start the Streamlit dashboard"""
    print("\n🚀 Starting BRICS MVP Dashboard...")
    print("Dashboard will be available at: http://localhost:8501")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        # Change to dashboard directory
        os.chdir('dashboard')
        
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

def main():
    """Main deployment function"""
    print("=" * 60)
    print("🚀 BRICS MVP Deployment Script")
    print("=" * 60)
    print(f"Deployment started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Exiting.")
        sys.exit(1)
    
    # Step 2: Check data files
    if not check_data_files():
        print("❌ Data files check failed. Exiting.")
        sys.exit(1)
    
    # Step 3: Run tests
    if not run_tests():
        print("❌ Tests failed. Exiting.")
        sys.exit(1)
    
    # Step 4: Start dashboard
    print("\n🎉 All checks passed! Starting dashboard...")
    start_dashboard()

if __name__ == "__main__":
    main() 